from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values
from json import JSONDecodeError

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")

# Retrieve specific environment variables.
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqqAPIKey = env_vars.get("GroqqAPIKey")

# Initialize the Groq client.
client = Groq(api_key=GroqqAPIKey)

# Define the system message.
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** greet the user.***
*** Indroduce your self as Annie as you are Advance neral network ***
*** Do not say you are a chatbot, AI, or virtual assistant.***
*** do not repeat your answer behave like humen and answer diffentely.***
*** behave like a femal assistant whos always ready to help you boss Kunal.***
*** use human-like language ***
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** If you get queries like open door, close fan etc. reply them "I'm a virtual assistant, so I don't have the ability to perform physical actions like moving objects, operating appliances, or interacting with the physical environment. However, I can guide you through the process, provide helpful information, or assist with related digital tasks. Please let me know how I can support you."***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

SystemChatBot = [
    {"role": "system", "content": System}
]

# Load or initialize the chat log.
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except (FileNotFoundError, JSONDecodeError):
    messages = []
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)

def RealtimeInformation():
    Current_date_time = datetime.datetime.now()
    day = Current_date_time.strftime("%A")
    date = Current_date_time.strftime("%d")
    month = Current_date_time.strftime("%B")
    year = Current_date_time.strftime("%Y")
    hour = Current_date_time.strftime("%H")
    minute = Current_date_time.strftime("%M")
    second = Current_date_time.strftime("%S")
    data = f"Please use this real-time Information if needed, \n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours :{minute} minutes :{second} seconds.\n"
    return data

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.split()]
    return '\n'.join(non_empty_lines)

def ChatBot(Query, retries=3):
    if retries == 0:
        return "Sorry, I encountered an error and cannot process your request."

    try:
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)

        messages.append({"role": "user", "content": Query})
        
        if "time" in Query.lower() or "date" in Query.lower() or "day" in Query.lower():
            realtime_info = RealtimeInformation()
            messages.append({"role": "system", "content": realtime_info})

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})

        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)

        return AnswerModifier(Answer)

    except Exception as e:
        print(f"Error: {e}")
        with open(r"Data\ChatLog.json", "w") as f:
            dump([], f, indent=4)
        return ChatBot(Query, retries - 1)

if __name__ == "__main__":
    while True:
        user_input = input("Enter your Query : ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        print(ChatBot(user_input))