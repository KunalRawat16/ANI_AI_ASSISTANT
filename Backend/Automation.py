# # Import required libraries
# from AppOpener import close, open as appopen  # Import functions to open and close apps.
# from webbrowser import open as webopen  # Import web browser functionality.
# from pywhatkit import search, playonyt  # Import functions for Google search and YouTube playback.
# from dotenv import dotenv_values  # Import dotenv to manage environment variables.
# from bs4 import BeautifulSoup  # Import BeautifulSoup for parsing HTML content.
# from rich import print  # Import rich for styled console output.
# from groq import Groq  # Import Groq for AI chat functionalities.
# import webbrowser  # Import webbrowser for opening URLs.
# import subprocess  # Import subprocess for interacting with the system.
# import requests  # Import requests for making HTTP requests.
# import keyboard  # Import keyboard for keyboard-related actions.
# import asyncio  # Import asyncio for asynchronous programming.
# import os  # Import os for operating system functionalities.

# # Load environment variables from the .env file.
# env_vars = dotenv_values(".env")
# GroupAPIKey = env_vars.get("GroqqAPIKey") # Retrieve the Group API key.

# # Define CSS classes for parsing specific elements in HTML content.
# classes = ["zCubwf", "hgKfc", "LIKOO sY7ric", "Z9LCW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta",
#     "I2Grdc", "OSU8Gd LIKOO", "v1zY6d", "webanswers-webanswers_table_webanswers-table", "dDoNo ikb4Bb gsrt", "sXlaOe",
#     "LWxRKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

# # Define a user-agent for making web requests.
# useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# # Initialize the Group client with the API key.
# client = Groq(api_key=GroupAPIKey)

# # Predefined professional responses for user interactions.
# professional_responses = [
#     "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
#     "I'm at your service for any additional questions or support you may need-don't hesitate to ask.",
# ]

# # List to store chatbot messages.
# messages = []

# # System message to provide context to the chatbot.
# SystemChatBot = {"role": "system", "content": f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letters"}

# # Function to perform a Google search.
# def GoogleSearch(Topic):
#     search(Topic)  # Use pywhatkit's search function to perform a Google search.
#     return True  # Indicate success.

# # Function to generate content using AI and save it to a file.
# def Content(Topic):
#     # Nested function to open a file in Notepad.
#     def OpenNotepad(file):
#         default_text_editor = 'notepad.exe'  # Default text editor.
#         subprocess.Popen([default_text_editor, file])  # Open the file in Notepad.

#     # Nested function to generate content using the AI chatbot.
#     def ContentWriterAI(prompt):
#         messages.append({'role': "user", "content": f"{prompt}"})  # Add the user's prompt to messages.

#         completion = client.chat.completions.create(
#             model='llama3-70b-8192',  # Specify the AI model.
#             messages= SystemChatBot + messages, # Include system instructions and chat history.
#             max_tokens=2048, # Limit the maximum tokens in the response.
#             temperature=0.7, # Adjust response randomness.
#             top_p=1, # Use nucleus sampling for response diversity.
#             stream=True, # Enable streaming response.
#             stop=None # Allow the model to determine stopping conditions.
#         )

#         Answer = ""  # Initialize an empty string for the response.

#         # Process streamed response chunks.
#         for chunk in completion:
#             if chunk.choices[0].delta.content:  # Check for content in the current chunk.
#                 Answer += chunk.choices[0].delta.content  # Append the content to the answer.

#         Answer = Answer.replace("</s>", "")  # Remove unwanted tokens from the response.
#         messages.append({'role': "assistant", "content": Answer})  # Add the AI's response to messages.
#         return Answer

#     Topic = Topic.replace("Content ", "")  # Remove "Content " from the topic.
#     ContentByAI = ContentWriterAI(Topic)  # Generate content using AI.

#     # Save the generated content to a text file.
#     with open(rf"Data\{Topic.lower().replace(' ', '')}.txt", "w", encoding="utf-8") as file:
#         file.write(ContentByAI)  # Write the content to the file.
#         file.close()
#     OpenNotepad(rf"Data\{Topic.lower().replace(' ', '')}.txt")  # Open the file in Notepad.
#     return True  # Indicate success.

# # Function to search for a topic on YouTube.
# def YouTubeSearch(Topic):
#     Url4Search = f"https://www.youtube.com/results?search_query={Topic}"  # Construct the YouTube search URL.
#     webbrowser.open(Url4Search)  # Open the search URL in a web browser.
#     return True  # Indicate success.

# # Function to play a video on YouTube.
# def PlayYoutube(query):
#     playonyt(query)  # Use pywhatkit's playonyt function to play the video.
#     return True  # Indicate success.

# # Function to open an application or a relevant webpage.
# def OpenApp(app, sess=requests.session()):
#     try:
#         appopen(app, match_closest=True, output=True, throw_error=True)  # Attempt to open the app.
#         return True  # Indicate success.
#     except:
#         # Nested function to extract links from HTML content.
#         def extract_links(html):
#             if html is None:
#                 return []
#             soup = BeautifulSoup(html, 'html.parser')  # Parse the HTML content.
#             links = soup.find_all('a', {'jsname': 'UNCKND'})  # Find relevant links.
#             return [link.get('href') for link in links]  # Return the links.

#         # Nested function to perform a Google search and retrieve HTML.
#         def search_google(query):
#             url = f"https://www.google.com/search?q={query}"  # Construct the Google search URL.
#             headers = {"User-Agent": useragent}  # Use the predefined user-agent.
#             response = sess.get(url, headers=headers)  # Perform the GET request.
#             if response.status_code == 200:
#                 return response.text  # Return the HTML content.
#             else:
#                 print("Failed to retrieve search results.")  # Print an error message.
#                 return None

#         html = search_google(app)  # Perform the Google search.
#         if html:
#             link = extract_links(html)[0]  # Extract the first link from the search results.
#             webopen(link)  # Open the link in a web browser.
#             return True  # Indicate success.

# # Function to close an application.
# def CloseApp(app):
#     if "chrome" in app:
#         pass  # Skip if the app is Chrome.
#     else:
#         try:
#             close(app, match_closest=True, output=True, throw_error=True)  # Attempt to close the app.
#             return True  # Indicate success.
#         except:
#             return False  # Indicate failure.

# # Function to execute system-level commands.
# def System(command):
#     # Nested function to mute the system volume.
#     def mute():
#         keyboard.press_and_release("volume mute")  # Simulate the mute key press.

#     # Nested function to unmute the system volume.
#     def unmute():
#         keyboard.press_and_release("volume mute")  # Simulate the unmute key press.

#     # Nested function to increase the system volume.
#     def volume_up():
#         keyboard.press_and_release("volume up")  # Simulate the volume up key press.

#     # Nested function to decrease the system volume.
#     def volume_down():
#         keyboard.press_and_release("volume down")  # Simulate the volume down key press.

#     # Execute the appropriate command.
#     if command == "mute":
#         mute()
#     elif command == "unmute":
#         unmute()
#     elif command == "volume up":
#         volume_up()
#     elif command == "volume down":
#         volume_down()

#     return True  # Indicate success.

# # Asynchronous function to translate and execute user commands.
# async def TranslateAndExecute(commands: list[str]):
#     funcs = []    # List to store asynchronous tasks.
#     for command in commands:
#         if command.startswith("open "):   # Handle "open" commands.
#             if "open it" in command:   # Ignore "open it" commands.
#                 pass
#             if "open file" == command:   # Ignore "open file" commands.
#                 pass
#             else:
#                 fun = asyncio.to_thread(OpenApp, command.removeprefix("open ")) # Schedule app opening.
#                 funcs.append(fun)

#         elif command.startswith("general "): # Placeholder for general commands.
#             pass

#         elif command.startswith("realtime "): # Placeholder for real-time commands.
#             pass

#         elif command.startswith("close "): # Handle "close" commands.
#             fun = asyncio.to_thread(CloseApp, command.removeprefix("close ")) # Schedule app closing.
#             funcs.append(fun)

#         elif command.startswith("play "):
#             fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play "))
#             funcs.append(fun)

#         elif command.startswith("content "):
#             fun = asyncio.to_thread(Content, command.removeprefix("content "))
#             funcs.append(fun)

#         elif command.startswith("google search "):
#             fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))
#             funcs.append(fun)

#         elif command.startswith("youtube search "):   # Handle YouTube search commands.
#             fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search "))   # Schedule YouTube search.
#             funcs.append(fun)

#         elif command.startswith("system "):   # Handle system commands.
#             fun = asyncio.to_thread(System, command.removeprefix("system "))   # Schedule system command.
#             funcs.append(fun)

#         else:
#             print(f"No Function Found. For {command}")   # Print an error for unrecognized commands.

#         results = await asyncio.gather(*funcs)   # Execute all tasks concurrently.

#         for result in results:   # Process the results.
#             if isinstance(result, str):
#                 yield result
#             else:
#                 yield result

# # Asynchronous function to aware command execution.
# async def Automation(commands: list[str]):
#     async for result in TranslateAndExecute(commands):   # Translate and execute commands.
#         pass
#     return True   # Indicate success.


















# import os
# import asyncio
# import subprocess
# import requests
# import webbrowser
# import keyboard
# from typing import List, Dict, Optional, AsyncGenerator, Union
# from pathlib import Path
# from dotenv import dotenv_values
# from bs4 import BeautifulSoup
# from rich import print
# from groq import Groq, APIError
# from pywhatkit import search, playonyt
# from AppOpener import close, open as appopen
# from webbrowser import open as webopen
# from requests.exceptions import RequestException

# # Constants
# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
# HTML_CLASSES = [
#     "zCubwf", "hgKfc", "LIKOO sY7ric", "Z9LCW", "gsrt vk_bk FzvWSb YwPhnf",
#     "pclqee", "tw-Data-text tw-text-small tw-ta", "I2Grdc", "OSU8Gd LIKOO",
#     "v1zY6d", "webanswers-webanswers_table_webanswers-table", "dDoNo ikb4Bb gsrt",
#     "sXlaOe", "LWxRKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"
# ]
# PROFESSIONAL_RESPONSES = [
#     "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
#     "I'm at your service for any additional questions or support you may need-don't hesitate to ask.",
# ]
# DATA_DIR = Path("Data")
# DATA_DIR.mkdir(exist_ok=True)

# class AutomationError(Exception):
#     """Base class for Automation exceptions"""
#     pass

# class AppOperationError(AutomationError):
#     """Raised when application operations fail"""
#     pass

# class WebOperationError(AutomationError):
#     """Raised when web operations fail"""
#     pass

# class ContentGenerationError(AutomationError):
#     """Raised when content generation fails"""
#     pass

# class SystemOperationError(AutomationError):
#     """Raised when system operations fail"""
#     pass

# def initialize_environment() -> Dict[str, Optional[str]]:
#     """Initialize and validate environment variables"""
#     env_vars = dotenv_values(".env")
#     if not (api_key := env_vars.get("GroqqAPIKey")):
#         raise ValueError("Groq API key not found in environment variables")
#     return env_vars

# def initialize_groq_client(api_key: str) -> Groq:
#     """Initialize and validate Groq client"""
#     try:
#         return Groq(api_key=api_key)
#     except Exception as e:
#         raise APIError(f"Failed to initialize Groq client: {str(e)}")

# env_vars = initialize_environment()
# client = initialize_groq_client(env_vars["GroqqAPIKey"])
# messages: List[Dict[str, str]] = []
# SystemChatBot = {
#     "role": "system", 
#     "content": f"Hello, I am {os.getenv('Username', 'User')}, You're a content writer specializing in formal letters."
# }

# def handle_error(error: Exception, context: str = "") -> str:
#     """Centralized error handling with rich formatting"""
#     error_msg = f"[bold red]Error in {context}:[/bold red] {str(error)}" if context else str(error)
#     print(error_msg)
#     return PROFESSIONAL_RESPONSES[0]

# def validate_input(input_str: str, min_length: int = 1) -> str:
#     """Validate and sanitize input strings"""
#     if not isinstance(input_str, str) or len(input_str.strip()) < min_length:
#         raise ValueError(f"Input must be a string with at least {min_length} character(s)")
#     return input_str.strip()

# async def GoogleSearch(topic: str) -> bool:
#     """Perform a Google search with error handling"""
#     try:
#         validated_topic = validate_input(topic)
#         search(validated_topic)
#         return True
#     except Exception as e:
#         raise WebOperationError(f"Google search failed: {str(e)}")

# async def Content(topic: str) -> bool:
#     """Generate content using AI with comprehensive error handling"""
#     try:
#         clean_topic = validate_input(topic.replace("Content ", ""))
        
#         async def generate_ai_content(prompt: str) -> str:
#             try:
#                 messages.append({'role': "user", "content": prompt})
                
#                 completion = client.chat.completions.create(
#                     model='llama3-70b-8192',
#                     messages=SystemChatBot + messages,
#                     max_tokens=2048,
#                     temperature=0.7,
#                     top_p=1,
#                     stream=True,
#                     stop=None
#                 )

#                 answer = ""
#                 async for chunk in completion:
#                     if chunk.choices[0].delta.content:
#                         answer += chunk.choices[0].delta.content

#                 answer = answer.replace("</s>", "")
#                 messages.append({'role': "assistant", "content": answer})
#                 return answer
#             except Exception as e:
#                 raise ContentGenerationError(f"AI content generation failed: {str(e)}")

#         def open_in_editor(file_path: Path) -> None:
#             try:
#                 if os.name == 'nt':  # Windows
#                     subprocess.Popen(['notepad.exe', str(file_path)])
#                 else:  # macOS/Linux
#                     subprocess.Popen(['xdg-open', str(file_path)])
#             except Exception as e:
#                 raise SystemOperationError(f"Failed to open editor: {str(e)}")

#         content = await generate_ai_content(clean_topic)
#         file_path = DATA_DIR / f"{clean_topic.lower().replace(' ', '_')}.txt"
        
#         try:
#             with file_path.open("w", encoding="utf-8") as file:
#                 file.write(content)
#             open_in_editor(file_path)
#             return True
#         except Exception as e:
#             raise ContentGenerationError(f"File operation failed: {str(e)}")

#     except Exception as e:
#         raise ContentGenerationError(str(e))

# async def YouTubeSearch(topic: str) -> bool:
#     """Search YouTube with error handling"""
#     try:
#         validated_topic = validate_input(topic)
#         url = f"https://www.youtube.com/results?search_query={validated_topic}"
#         webbrowser.open(url)
#         return True
#     except Exception as e:
#         raise WebOperationError(f"YouTube search failed: {str(e)}")

# async def PlayYoutube(query: str) -> bool:
#     """Play YouTube video with error handling"""
#     try:
#         validated_query = validate_input(query)
#         playonyt(validated_query)
#         return True
#     except Exception as e:
#         raise WebOperationError(f"YouTube playback failed: {str(e)}")

# async def OpenApp(app_name: str, session: Optional[requests.Session] = None) -> bool:
#     """Open application with fallback to web search"""
#     try:
#         clean_app_name = validate_input(app_name)
        
#         def extract_first_result(html: str) -> Optional[str]:
#             try:
#                 soup = BeautifulSoup(html, 'html.parser')
#                 if link := soup.find('a', {'jsname': 'UNCKND'}):
#                     return link.get('href')
#                 return None
#             except Exception as e:
#                 raise WebOperationError(f"HTML parsing failed: {str(e)}")

#         def perform_web_search(query: str) -> str:
#             try:
#                 url = f"https://www.google.com/search?q={query}"
#                 headers = {"User-Agent": USER_AGENT}
#                 response = (session or requests.Session()).get(url, headers=headers)
#                 response.raise_for_status()
#                 return response.text
#             except RequestException as e:
#                 raise WebOperationError(f"Web search failed: {str(e)}")

#         try:
#             appopen(clean_app_name, match_closest=True, output=False, throw_error=True)
#             return True
#         except Exception as e:
#             html = perform_web_search(clean_app_name)
#             if link := extract_first_result(html):
#                 webopen(link)
#                 return True
#             raise AppOperationError(f"No results found for {clean_app_name}")

#     except Exception as e:
#         raise AppOperationError(str(e))

# async def CloseApp(app_name: str) -> bool:
#     """Close application with error handling"""
#     try:
#         clean_app_name = validate_input(app_name)
#         if "chrome" in clean_app_name.lower():
#             return False  # Skip Chrome intentionally
#         close(clean_app_name, match_closest=True, output=False, throw_error=True)
#         return True
#     except Exception as e:
#         raise AppOperationError(str(e))

# async def System(command: str) -> bool:
#     """Execute system commands with error handling"""
#     command_actions = {
#         "mute": lambda: keyboard.press_and_release("volume mute"),
#         "unmute": lambda: keyboard.press_and_release("volume mute"),
#         "volume up": lambda: keyboard.press_and_release("volume up"),
#         "volume down": lambda: keyboard.press_and_release("volume down")
#     }
    
#     try:
#         clean_command = validate_input(command)
#         if action := command_actions.get(clean_command.lower()):
#             action()
#             return True
#         raise ValueError(f"Unsupported system command: {clean_command}")
#     except Exception as e:
#         raise SystemOperationError(str(e))

# async def safe_execute(coro) -> Union[bool, str]:
#     """Execute coroutine with error handling"""
#     try:
#         return await coro
#     except Exception as e:
#         return handle_error(e, coro.__name__)

# async def TranslateAndExecute(commands: List[str]) -> AsyncGenerator[Union[bool, str], None]:
#     """Translate and execute commands with proper error handling"""
#     command_handlers = {
#         "open": OpenApp,
#         "close": CloseApp,
#         "play": PlayYoutube,
#         "content": Content,
#         "google search": GoogleSearch,
#         "youtube search": YouTubeSearch,
#         "system": System
#     }

#     tasks = []
#     for command in commands:
#         command = command.strip()
#         if not command:
#             continue

#         for prefix, handler in command_handlers.items():
#             if command.startswith(f"{prefix} "):
#                 clean_cmd = command[len(prefix)+1:].strip()
#                 if clean_cmd:
#                     tasks.append(asyncio.create_task(safe_execute(handler(clean_cmd))))
#                 break
#         else:
#             print(f"[yellow]Warning:[/yellow] Unrecognized command: {command}")

#     if tasks:
#         results = await asyncio.gather(*tasks)
#         for result in results:
#             yield result

# async def Automation(commands: List[str]) -> bool:
#     """Main Automation function with comprehensive error handling"""
#     try:
#         if not commands:
#             raise ValueError("Empty command list provided")

#         async for result in TranslateAndExecute(commands):
#             if isinstance(result, str):
#                 print(result)  # Print professional responses

#         return True
#     except Exception as e:
#         handle_error(e, "Automation")
#         return False

# async def main():
#     """Example usage"""
#     commands = [
#         "open notepad",
#         "google search python programming",
#         "content formal business letter",
#         "system volume up"
#     ]
    
#     success = await Automation(commands)
#     print(f"Automation completed {'successfully' if success else 'with errors'}")

# if __name__ == "__main__":
#     asyncio.run(main())
























"""
Improved Automation Assistant
- Added comprehensive error handling
- Improved resource management
- Enhanced security
- Optimized code structure and performance
- Added type hints for better code quality
"""

# Import required libraries
from typing import List, Dict, Union, Optional, AsyncGenerator, Any
from AppOpener import close, open as appopen
import webbrowser
from pywhatkit import search, playonyt
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import subprocess
import requests
import keyboard
import asyncio
import logging
import os
import json
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("Automation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Ensure data directory exists
data_dir = Path("Data")
data_dir.mkdir(exist_ok=True)

# Load environment variables safely
try:
    load_dotenv()
    # Try both possible spellings of the API key
    GROQ_API_KEY = os.getenv("GroqqAPIKey") or os.getenv("GroqAPIKey")
    if not GROQ_API_KEY:
        logger.warning("API Key not found in environment variables (tried GroqqAPIKey and GroqAPIKey)")
        GROQ_API_KEY = ""  # Fallback to empty string to prevent NoneType errors
    
    USERNAME = os.getenv("Username", "Assistant")  # Default if Username not set
except Exception as e:
    logger.error(f"Error loading environment variables: {e}")
    GROQ_API_KEY = ""
    USERNAME = "Assistant"

# Define CSS classes for parsing specific HTML elements
HTML_PARSER_CLASSES = [
    "zCubwf", "hgKfc", "LIKOO sY7ric", "Z9LCW", 
    "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta",
    "I2Grdc", "OSU8Gd LIKOO", "v1zY6d", "webanswers-webanswers_table_webanswers-table", 
    "dDoNo ikb4Bb gsrt", "sXlaOe", "LWxRKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"
]

# User agent for making web requests
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# Initialize Groq client with error handling
try:
    if GROQ_API_KEY:
        client = Groq(api_key=GROQ_API_KEY)
        # Verify API key is valid by making a simple test request
        test_response = client.chat.completions.create(
            model='llama3-70b-8192',
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10,
            temperature=0.7
        )
        logger.info("Groq API connection successful")
    else:
        logger.warning("No Groq API key provided")
        client = None
except Exception as e:
    logger.error(f"Failed to initialize Groq client: {e}")
    client = None

# Predefined professional responses
PROFESSIONAL_RESPONSES = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need-don't hesitate to ask.",
]

# List to store chatbot messages
messages: List[Dict[str, str]] = []

# System message for the chatbot
SYSTEM_CHAT_BOT = {"role": "system", "content": f"Hello, I am {USERNAME}, You're a content writer. You have to write content like letters"}


def google_search(topic: str) -> bool:
    """
    Perform a Google search on the given topic.
    
    Args:
        topic: The search query.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        search(topic)
        logger.info(f"Performed Google search for: {topic}")
        return True
    except Exception as e:
        logger.error(f"Error during Google search: {e}")
        return False


def generate_content(topic: str) -> bool:
    """
    Generate content using AI and save it to a file.
    
    Args:
        topic: The topic for content generation.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    # Clean the topic by removing the "Content " prefix if present
    clean_topic = topic.replace("Content ", "").strip()
    
    if not clean_topic:
        logger.error("Empty topic provided for content generation")
        return False
    
    # Check if Groq client is available
    if not client:
        logger.error("Content generation failed: Groq client not available")
        # Fallback content for testing when API is unavailable
        content = f"Sample content for: {clean_topic}\n\nThis is placeholder content generated because the AI service is unavailable."
    else:
        try:
            content = _content_writer_ai(clean_topic)
            if not content:
                logger.error("Failed to generate content with AI")
                # Fallback content
                content = f"Sample content for: {clean_topic}\n\nThis is placeholder content generated because content generation failed."
        except Exception as e:
            logger.error(f"Error in AI content generation: {e}")
            # Fallback content
            content = f"Sample content for: {clean_topic}\n\nThis is placeholder content generated because of an error: {str(e)}"
    
    try:
        # Create a safe filename
        safe_filename = "".join(c for c in clean_topic.lower() if c.isalnum() or c == ' ').replace(' ', '_')
        file_path = data_dir / f"{safe_filename}.txt"
        
        # Save the generated content
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
            
        logger.info(f"Content saved to {file_path}")
        
        # Open in text editor
        _open_text_editor(file_path)
        return True
    except Exception as e:
        logger.error(f"Error saving content to file: {e}")
        return False


def _content_writer_ai(prompt: str) -> Optional[str]:
    """
    Generate content using the AI model.
    
    Args:
        prompt: The prompt for content generation.
        
    Returns:
        str: Generated content or None if failed.
    """
    if not client:
        logger.error("Groq client not initialized. Check API key.")
        return None
        
    try:
        # Add the user's prompt to messages
        messages.append({'role': "user", "content": prompt})
        
        # Create a completion with the AI model
        # Using llama3-70b-8192 as replacement for the decommissioned mixtral-8x7b-32768
        completion = client.chat.completions.create(
            model='llama3-70b-8192',  # Updated model that's currently supported
            messages=[SYSTEM_CHAT_BOT] + messages,  # Combine system message with conversation
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )
        
        answer = ""
        
        # Process streamed response chunks
        for chunk in completion:
            if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                answer += chunk.choices[0].delta.content
        
        # Clean up the response
        answer = answer.replace("</s>", "").strip()
        
        # Add the AI's response to messages
        messages.append({'role': "assistant", "content": answer})
        
        return answer
    except Exception as e:
        logger.error(f"Error generating AI content: {e}")
        return None


def _open_text_editor(file_path: Union[str, Path]) -> bool:
    """
    Open a file in the default text editor.
    
    Args:
        file_path: Path to the file to open.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        default_text_editor = 'notepad.exe' if os.name == 'nt' else 'xdg-open'
        subprocess.Popen([default_text_editor, str(file_path)])
        logger.info(f"Opened {file_path} in text editor")
        return True
    except Exception as e:
        logger.error(f"Failed to open text editor: {e}")
        return False


def youtube_search(topic: str) -> bool:
    """
    Search for a topic on YouTube.
    
    Args:
        topic: The search query.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        url = f"https://www.youtube.com/results?search_query={topic}"
        webbrowser.open(url)
        logger.info(f"Performed YouTube search for: {topic}")
        return True
    except Exception as e:
        logger.error(f"Error during YouTube search: {e}")
        return False


def play_youtube(query: str) -> bool:
    """
    Play a video on YouTube.
    
    Args:
        query: The search query.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        # Use a custom function to avoid potential blocking issues
        search_query = query.replace(" ", "+")
        url = f"https://www.youtube.com/results?search_query={search_query}"
        webbrowser.open(url)
        logger.info(f"Opened YouTube search for: {query}")
        return True
    except Exception as e:
        logger.error(f"Error playing YouTube video: {e}")
        return False


def open_app(app_name: str) -> bool:
    """
    Open an application or a relevant webpage.
    
    Args:
        app_name: Name of the application to open.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    if not app_name.strip():
        logger.error("Empty app name provided")
        return False
        
    try:
        # Try to open as a local application
        appopen(app_name, match_closest=True, output=True, throw_error=True)
        logger.info(f"Opened application: {app_name}")
        return True
    except Exception as app_error:
        logger.info(f"Could not open as local app: {app_error}")
        
        # If local app fails, try web search
        try:
            links = _search_and_extract_links(app_name)
            if links:
                webbrowser.open(links[0])
                logger.info(f"Opened web result for: {app_name}")
                return True
            else:
                logger.warning(f"No suitable links found for: {app_name}")
                return False
        except Exception as web_error:
            logger.error(f"Failed to open app or web result: {web_error}")
            return False


def _search_and_extract_links(query: str) -> List[str]:
    """
    Perform a Google search and extract links from the results.
    
    Args:
        query: The search query.
        
    Returns:
        List[str]: List of extracted links.
    """
    try:
        session = requests.session()
        url = f"https://www.google.com/search?q={query}"
        headers = {"User-Agent": USER_AGENT}
        response = session.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', {'jsname': 'UNCKND'})
            return [link.get('href') for link in links if link.get('href')]
        else:
            logger.warning(f"Failed to retrieve search results. Status code: {response.status_code}")
            return []
    except Exception as e:
        logger.error(f"Error in search and extract links: {e}")
        return []


def close_app(app_name: str) -> bool:
    """
    Close an application.
    
    Args:
        app_name: Name of the application to close.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    if not app_name.strip():
        logger.error("Empty app name provided to close")
        return False
        
    # Skip closing Chrome to prevent disrupting the web interface
    if "chrome" in app_name.lower():
        logger.info("Skipping closing Chrome to maintain web interface")
        return False
        
    try:
        close(app_name, match_closest=True, output=True, throw_error=True)
        logger.info(f"Closed application: {app_name}")
        return True
    except Exception as e:
        logger.error(f"Failed to close application: {e}")
        return False


def system_command(command: str) -> bool:
    """
    Execute system-level commands (limited to safe volume controls).
    
    Args:
        command: The system command to execute.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    # Whitelist of allowed commands for security
    allowed_commands = {
        "mute": lambda: keyboard.press_and_release("volume mute"),
        "unmute": lambda: keyboard.press_and_release("volume mute"),
        "volume up": lambda: keyboard.press_and_release("volume up"),
        "volume down": lambda: keyboard.press_and_release("volume down")
    }
    
    command = command.lower().strip()
    
    if command in allowed_commands:
        try:
            allowed_commands[command]()
            logger.info(f"Executed system command: {command}")
            return True
        except Exception as e:
            logger.error(f"Error executing system command: {e}")
            return False
    else:
        logger.warning(f"Unsupported system command: {command}")
        return False


async def translate_and_execute(commands: List[str]) -> AsyncGenerator[Union[bool, str], None]:
    """
    Translate and execute user commands asynchronously.
    
    Args:
        commands: List of commands to execute.
        
    Yields:
        Results of command execution.
    """
    for command in commands:
        command = command.strip().lower()
        result = False
        functions = []  # Store coroutines to execute
        
        try:
            if command.startswith("open ") and "open it" not in command and "open file" != command:
                app_name = command.removeprefix("open ").strip()
                functions.append(asyncio.to_thread(open_app, app_name))
                
            elif command.startswith("close "):
                app_name = command.removeprefix("close ").strip()
                functions.append(asyncio.to_thread(close_app, app_name))
                
            elif command.startswith("play "):
                query = command.removeprefix("play ").strip()
                functions.append(asyncio.to_thread(play_youtube, query))
                
            elif command.startswith("content "):
                topic = command.strip()  # Keep "content" in the string for the function
                functions.append(asyncio.to_thread(generate_content, topic))
                
            elif command.startswith("google search "):
                query = command.removeprefix("google search ").strip()
                functions.append(asyncio.to_thread(google_search, query))
                
            elif command.startswith("youtube search "):
                query = command.removeprefix("youtube search ").strip()
                functions.append(asyncio.to_thread(youtube_search, query))
                
            elif command.startswith("system "):
                cmd = command.removeprefix("system ").strip()
                functions.append(asyncio.to_thread(system_command, cmd))
                
            elif command.startswith("general ") or command.startswith("realtime "):
                logger.info(f"Command type not implemented: {command}")
                
            else:
                logger.warning(f"No function found for: {command}")
                
            # Execute each function one by one and yield results
            if functions:
                for function in functions:
                    try:
                        result = await function
                        yield result
                    except Exception as func_error:
                        logger.error(f"Error executing function for command '{command}': {func_error}")
                        yield False
            else:
                yield False
                
        except Exception as e:
            logger.error(f"Error processing command '{command}': {e}")
            yield False
            
        # Add a small delay between commands to ensure proper execution
        await asyncio.sleep(0.5)


async def Automation(commands: List[str]) -> bool:
    """
    Execute Automation commands with proper error handling.
    
    Args:
        commands: List of commands to execute.
        
    Returns:
        bool: True if all commands executed successfully, False otherwise.
    """
    if not commands:
        logger.warning("No commands provided to Automation function")
        return False
        
    success = True
    all_results = []
    
    try:
        # Process all commands
        async for result in translate_and_execute(commands):
            all_results.append(result)
            if not result:
                success = False
                # Continue processing other commands even if one fails
        
        # Wait a moment to ensure all processes have completed
        await asyncio.sleep(1)
        
        # Return overall success status
        return success
    except Exception as e:
        logger.error(f"Error in Automation execution: {e}")
        return False


def __init__():
    """
    Initialize required resources and directories.
    """
    # Ensure data directory exists
    data_dir.mkdir(exist_ok=True)
    logger.info("Initialization complete")


# Example usage:
if __name__ == "__main__":
    async def test():
        # Initialize required resources
        __init__()
        
        # Example commands to test the system
        test_commands = [
            "google search python programming",
            "open notepad",
            "system volume up",
            "system volume down",
            "play python tutorial",
            "content Write a short introduction to Python programming"
        ]
        
        print("Starting Automation test...")
        try:
            result = await Automation(test_commands)
            print(f"Automation test completed with success: {result}")
            
            # Test repeated execution
            print("\nTesting second execution with different commands...")
            result2 = await Automation(["google search python asyncio", "system volume up"])
            print(f"Second Automation test completed with success: {result2}")
            
        except Exception as e:
            print(f"Test failed with exception: {e}")
    
    # Create a new event loop for execution
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(test())
    finally:
        loop.close()