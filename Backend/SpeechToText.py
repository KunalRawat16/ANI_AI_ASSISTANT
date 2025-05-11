from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt
import time

# Disable TensorFlow oneDNN warnings (optional)
# os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username", "User")
Assistantname = env_vars.get("Assistantname", "Assistant")
GroqqAPIKey = env_vars.get("GroqqAPIKey", "")
InputLanguage = env_vars.get("InputLanguage", "en-US")  # Default to English

# Simplified HTML for background recognition
HtmlCode = f'''<!DOCTYPE html>
<html>
<head>
    <title>Background Speech Recognition</title>
    <script>
        let recognition;
        let lastResult = "";
        
        function startRecognition() {{
            recognition = new (window.webkitSpeechRecognition || window.SpeechRecognition)();
            recognition.lang = '{InputLanguage}';
            recognition.continuous = true;
            recognition.interimResults = false;

            recognition.onresult = function(event) {{
                const transcript = event.results[event.results.length - 1][0].transcript;
                document.getElementById('output').textContent = transcript;
                lastResult = transcript;
            }};

            recognition.onerror = function(event) {{
                console.error("Recognition error:", event.error);
            }};

            recognition.start();
        }}

        function getLastResult() {{
            return lastResult;
        }}
    </script>
</head>
<body>
    <div id="output" style="display:none;"></div>
    <script>startRecognition();</script>
</body>
</html>'''

# Save HTML file
os.makedirs("Data", exist_ok=True)
with open(r"Data\Voice.html", "w") as f:
    f.write(HtmlCode)

# Chrome options for completely headless operation
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--mute-audio")

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Path configuration
current_dir = os.getcwd()
TempDirPath = os.path.join(current_dir, "Frontend", "Files")
os.makedirs(TempDirPath, exist_ok=True)

def SetAssistantStatus(status):
    with open(os.path.join(TempDirPath, 'Status.data'), 'w', encoding='utf-8') as file:
        file.write(status)

def QueryModifier(query):
    query = query.strip().capitalize()
    if not query.endswith(('.', '?', '!')):
        question_words = ["how", "what", "who", "where", "when", "why", "which"]
        if any(query.lower().startswith(word) for word in question_words):
            query += '?'
        else:
            query += '.'
    return query

def UniversalTranslator(text):
    try:
        return mt.translate(text, "en", "auto").capitalize()
    except Exception as e:
        print(f"Translation error: {e}")
        return text.capitalize()

def SpeechRecognition():
    driver.get(f"file://{os.path.join(current_dir, 'Data', 'Voice.html')}")
    
    last_text = ""
    while True:
        try:
            # Get text directly from JavaScript variable
            current_text = driver.execute_script("return getLastResult() || ''")
            
            if current_text and current_text != last_text:
                last_text = current_text
                
                if InputLanguage.lower() != "en":
                    SetAssistantStatus("Translating...")
                    translated = UniversalTranslator(current_text)
                    return QueryModifier(translated)
                return QueryModifier(current_text)
            
            time.sleep(0.5)  # Reduce CPU usage
            
        except Exception as e:
            print(f"Recognition error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        print("Speech recognition running in background...")
        while True:
            text = SpeechRecognition()
            if text:
                print("Recognized:", text)
    except KeyboardInterrupt:
        print("\nStopping recognition...")
    finally:
        driver.quit()