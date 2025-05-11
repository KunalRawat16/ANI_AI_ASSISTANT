import asyncio
import json
import os
import threading
import time
import logging
import gc
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from queue import Queue
from threading import Lock
from dotenv import dotenv_values

# Import your application modules
from Frontend.GUI import (
    GraphicalUserInterface,
    SetAssistantStatus,
    ShowTextToScreen,
    TempDirectoryPath,
    SetMicrophoneStatus,
    AnswerModifier,
    QueryModifier,
    GetMicrophoneStatus,
    GetAssistantStatus
)
from Backend.Model import FirstLayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.SpeechToText import SpeechRecognition
from Backend.Chatbot import ChatBot
from Backend.TextToSpeech import TextToSpeech

# ========================
# Configuration & Setup
# ========================
env_vars = dotenv_values('.env')
Username = env_vars.get('username')
Assistantname = env_vars.get('Assistantname')
DefaultMessage = f'''{{username}}: Hello {{Assistantname}}, How are you?
{{Assistantname}}: Welcome {{username}}. I am doing well. How may I help you?'''
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

# Initialize logging
logging.basicConfig(
    filename='app_performance.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Thread-safe resources
executor = ThreadPoolExecutor(max_workers=4)
task_queue = Queue(maxsize=50)
gui_lock = Lock()
api_semaphore = asyncio.Semaphore(5)  # Limit concurrent API calls

# ========================
# Async File Operations
# ========================
async def async_file_write(path, content, encoding='utf-8'):
    """Thread-safe asynchronous file write."""
    with gui_lock:
        with open(path, 'w', encoding=encoding) as file:
            file.write(content)

async def async_file_read(path, encoding='utf-8'):
    """Thread-safe asynchronous file read."""
    with gui_lock:
        with open(path, 'r', encoding=encoding) as file:
            return file.read()

# ========================
# Core Application Functions
# ========================
async def ShowDefaultChatIfNoChats():
    """Initialize default chat if empty."""
    try:
        content = await async_file_read(r'Data\ChatLog.json')
        if len(content) < 5:
            await asyncio.gather(
                async_file_write(TempDirectoryPath('Database.data'), ""),
                async_file_write(TempDirectoryPath('Responses.data'), DefaultMessage)
            )
    except Exception as e:
        logging.error(f"ShowDefaultChatIfNoChats error: {e}")

async def ReadChatLogJson():
    """Safely read chat log JSON."""
    try:
        content = await async_file_read(r'Data\ChatLog.json')
        return json.loads(content)
    except Exception as e:
        logging.error(f"ReadChatLogJson error: {e}")
        return []

async def ChatLogIntegration():
    """Process and format chat log data."""
    try:
        json_data = await ReadChatLogJson()
        formatted_chatlog = ""
        
        for entry in json_data:
            if entry["role"] == "user":
                formatted_chatlog += f'User: {entry["content"]}\n'
            elif entry["role"] == "assistant":
                formatted_chatlog += f'Assistant: {entry["content"]}\n'
        
        formatted_chatlog = formatted_chatlog.replace("Assistant", Assistantname + " ")
        await async_file_write(TempDirectoryPath('Database.data'), AnswerModifier(formatted_chatlog))
    except Exception as e:
        logging.error(f"ChatLogIntegration error: {e}")

async def ShowChatsOnGUI():
    """Update GUI with latest chats."""
    try:
        data = await async_file_read(TempDirectoryPath('Database.data'))
        if len(str(data)) > 0:
            lines = data.split('\n')
            result = '\n'.join(lines)
            await async_file_write(TempDirectoryPath('Responses.data'), result)
    except Exception as e:
        logging.error(f"ShowChatsOnGUI error: {e}")

async def InitialExecution():
    """Initialize application state."""
    SetMicrophoneStatus("False")
    ShowTextToScreen("")
    await ShowDefaultChatIfNoChats()
    await ChatLogIntegration()
    await ShowChatsOnGUI()

# ========================
# Task Execution & Automation
# ========================
async def execute_task(decision):
    """Execute automation tasks with timeout."""
    try:
        await asyncio.wait_for(
            Automation(list(decision)).run(),
            timeout=30.0
        )
    except TimeoutError:
        logging.warning("Task execution timed out")
    except Exception as e:
        logging.error(f"Task execution failed: {e}")

async def robust_search(query, max_retries=3):
    """Search with retry mechanism."""
    for attempt in range(max_retries):
        try:
            async with api_semaphore:  # Rate limiting
                return await asyncio.get_event_loop().run_in_executor(
                    executor, RealtimeSearchEngine, QueryModifier(query)
                )
        except Exception as e:
            wait_time = 2 ** attempt  # Exponential backoff
            logging.warning(f"Search retry {attempt+1}/{max_retries} in {wait_time}s...")
            await asyncio.sleep(wait_time)
    return "Sorry, I couldn't fetch the data right now."

# ========================
# Main Execution Logic
# ========================
async def MainExecution():
    """Core application logic with comprehensive error handling."""
    try:
        TaskExecution = False
        SetAssistantStatus("Listening...")
        
        # Speech recognition with timeout
        try:
            Query = await asyncio.wait_for(
                asyncio.get_event_loop().run_in_executor(executor, SpeechRecognition),
                timeout=10.0
            )
        except TimeoutError:
            SetAssistantStatus("Timeout: Didn't hear anything")
            return False
        
        with gui_lock:
            ShowTextToScreen(f"{Username}: {Query}")
        
        SetAssistantStatus("Thinking...")
        
        # Model decision with timeout
        try:
            Decision = await asyncio.wait_for(
                asyncio.get_event_loop().run_in_executor(executor, FirstLayerDMM, Query),
                timeout=15.0
            )
        except TimeoutError:
            SetAssistantStatus("Timeout: Thinking took too long")
            return False

        logging.info(f"Decision: {Decision}")

        G = any(i for i in Decision if i.startswith("general"))
        R = any(i for i in Decision if i.startswith("realtime"))

        Merged_query = " and ".join(
            ["".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
        )

        # Handle automation tasks
        for queries in Decision:
            if not TaskExecution and any(queries.startswith(func) for func in Functions):
                asyncio.create_task(execute_task(Decision))
                TaskExecution = True

        # Process decision types
        if G and R:
            SetAssistantStatus("Searching...")
            Answer = await robust_search(Merged_query)
            with gui_lock:
                ShowTextToScreen(f"{Assistantname}: {Answer}")
            SetAssistantStatus("Answering...")
            await asyncio.get_event_loop().run_in_executor(
                executor, TextToSpeech, Answer
            )
            return True
        
        for Queries in Decision:
            if "general" in Queries:
                SetAssistantStatus("Thinking...")
                QueryFinal = Queries.replace("general", "")
                Answer = await asyncio.get_event_loop().run_in_executor(
                    executor, ChatBot, QueryModifier(QueryFinal)
                )
                with gui_lock:
                    ShowTextToScreen(f"{Assistantname}: {Answer}")
                SetAssistantStatus("Answering...")
                await asyncio.get_event_loop().run_in_executor(
                    executor, TextToSpeech, Answer
                )
                return True
            
            elif "realtime" in Queries:
                SetAssistantStatus("Searching...")
                QueryFinal = Queries.replace("realtime", "")
                Answer = await robust_search(QueryFinal)
                with gui_lock:
                    ShowTextToScreen(f"{Assistantname}: {Answer}")
                SetAssistantStatus("Answering...")
                await asyncio.get_event_loop().run_in_executor(
                    executor, TextToSpeech, Answer
                )
                return True
            
            elif "exit" in Queries:
                QueryFinal = "Okay, Bye!"
                Answer = await asyncio.get_event_loop().run_in_executor(
                    executor, ChatBot, QueryModifier(QueryFinal)
                )
                with gui_lock:
                    ShowTextToScreen(f"{Assistantname}: {Answer}")
                SetAssistantStatus("Answering...")
                await asyncio.get_event_loop().run_in_executor(
                    executor, TextToSpeech, Answer
                )
                os._exit(0)
                
    except Exception as e:
        logging.error(f"MainExecution error: {e}")
        SetAssistantStatus("Available...")
        return False
    finally:
        gc.collect()  # Clean up memory

# ========================
# Thread Management
# ========================
async def FirstThread():
    """Main worker thread with improved stability."""
    while True:
        try:
            CurrentStatus = GetMicrophoneStatus()
            
            if CurrentStatus == "True":
                await MainExecution()
            else:
                AIStatus = GetAssistantStatus()
                if "Available..." not in AIStatus:
                    SetAssistantStatus("Available...")
                await asyncio.sleep(0.1)
                
        except Exception as e:
            logging.error(f"FirstThread error: {e}")
            SetAssistantStatus("Available...")
            await asyncio.sleep(1)

def worker():
    """Background task processor."""
    while True:
        task = task_queue.get()
        try:
            task()
        except Exception as e:
            logging.error(f"Task failed: {e}")
        finally:
            task_queue.task_done()

def run_async_thread():
    """Run the async event loop in a dedicated thread."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(FirstThread())

# ========================
# Application Entry Point
# ========================
if __name__ == "__main__":
    # Initialize background workers
    for _ in range(4):  # 4 worker threads
        threading.Thread(target=worker, daemon=True).start()

    # Initialize application
    asyncio.run(InitialExecution())
    
    # Start async worker thread
    worker_thread = threading.Thread(target=run_async_thread, daemon=True)
    worker_thread.start()
    
    # Run GUI in main thread
    try:
        GraphicalUserInterface()
    except Exception as e:
        logging.critical(f"GUI crashed: {e}")
    finally:
        os._exit(1)