import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    print("Voice ID:", voice.id)
    print("Name:", voice.name)
    print("Gender:", voice.gender)
    print("Age:", voice.age)
    print("Languages:", voice.languages)
    print("---")
engine.runAndWait()