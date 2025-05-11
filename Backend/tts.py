import pyttsx3

# Initialize the TTS engine
engine = pyttsx3.init()

# Set voice properties if you want (Optional)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # [0] for male, [1] for female voice
engine.setProperty('rate', 170)  # Speed of speech (default around 200)

def speak_offline(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error speaking: {e}")

if __name__ == "__main__":
    while True:
        try:
            text = input("Enter text: ")
            speak_offline(text)
        except KeyboardInterrupt:
            print("\nProgram exited.")
            break
