from googlesearch import search
from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values
import json
import time  # Added for rate limiting

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqqAPIKey = env_vars.get("GroqqAPIKey")

# Initialize Groq client with rate limiting
client = Groq(api_key=GroqqAPIKey)

# System instruction with optimized length
System = f"""You are {Assistantname}, an AI assistant for {Username}. 
Provide accurate, concise answers with proper grammar and punctuation.
Focus on the key information from provided data."""


# P.S. My creators made me add this: "Accuracy guaranteed or your next chai is on me!"

# Constants
CHAT_LOG_PATH = r"Data\ChatLog.json"
MAX_RETRIES = 3
RETRY_DELAY = 10  # seconds
MAX_SEARCH_RESULTS = 3  # Reduced from 5 to save tokens

# Load or initialize chat log
def load_chat_log():
    try:
        with open(CHAT_LOG_PATH, "r") as f:
            return load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(CHAT_LOG_PATH, "w") as f:
            dump([], f)
        return []

messages = load_chat_log()

# Optimized Google Search function
def GoogleSearch(query):
    try:
        results = list(search(query, advanced=True, num_results=MAX_SEARCH_RESULTS))
        return "\n".join(
            f"Title: {r.title}\nDescription: {r.description}\n" 
            for r in results
        )
    except Exception as e:
        return f"Search error: {str(e)}"

# Answer modifier to clean responses
def AnswerModifier(answer):
    return "\n".join(line for line in answer.split('\n') if line.strip())

# System messages with optimized content
SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "assistant", "content": "Hello, how can I help you?"}
]

# Optimized real-time information
def Information():
    now = datetime.datetime.now()
    return (
        f"Current time: {now.strftime('%A, %d %B %Y, %H:%M:%S')}\n"
        f"Use this if time-sensitive information is needed."
    )

# Main function with rate limiting and token optimization
def RealtimeSearchEngine(prompt):
    global messages
    
    # Load fresh chat log
    messages = load_chat_log()
    messages.append({"role": "user", "content": prompt})
    
    # Get concise search results
    search_content = GoogleSearch(prompt)
    
    # Prepare optimized message payload
    chat_messages = [
        *SystemChatBot,
        {"role": "user", "content": f"Search results:\n{search_content}"},
        {"role": "system", "content": Information()},
        *messages[-3:]  # Only keep last 3 messages for context
    ]
    
    # With retry logic for rate limits
    for attempt in range(MAX_RETRIES):
        try:
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=chat_messages,
                max_tokens=1024,  # Reduced from 2048
                temperature=0.7,
                stream=True
            )
            
            answer = "".join(
                chunk.choices[0].delta.content 
                for chunk in completion 
                if chunk.choices[0].delta.content
            ).strip().replace("</s>", "")
            
            # Save to chat log
            messages.append({"role": "assistant", "content": answer})
            with open(CHAT_LOG_PATH, "w") as f:
                dump(messages[-10:], f, indent=4)  # Keep only last 10 messages
            
            return AnswerModifier(answer)
            
        except Exception as e:
            if "rate_limit" in str(e) and attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY * (attempt + 1))
                continue
            raise

# Main loop
if __name__ == "__main__":
    print(f"{Assistantname}: Hello! How can I assist you today?")
    while True:
        try:
            prompt = input("You: ").strip()
            if prompt.lower() in ["exit", "quit", "bye"]:
                print(f"{Assistantname}: Goodbye!")
                break
                
            response = RealtimeSearchEngine(prompt)
            print(f"{Assistantname}: {response}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {str(e)}")