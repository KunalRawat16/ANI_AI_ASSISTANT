import pygame
import random
import asyncio
import edge_tts
import os
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice")

async def TextToAudioFile(text):
    file_path = r"Data\\speech.mp3"

    # Remove old speech file if it exists
    if os.path.exists(file_path):
        os.remove(file_path)

    try:
        communicate = edge_tts.Communicate(text, AssistantVoice)
        await communicate.save(file_path)
        return True  # Success
    except Exception as e:
        print(f"Error during text-to-audio conversion: {e}")
        return False  # Failure

def TTS(Text, func=lambda r=None: True):
    try:
        # Convert text to audio first
        success = asyncio.run(TextToAudioFile(Text))
        
        if not success:
            print("❌ Failed to generate speech. Check your internet connection or try again later.")
            return False

        # Initialize pygame only if speech generated
        pygame.mixer.init()
        pygame.mixer.music.load(r"Data\\speech.mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            if func() == False:
                break
            pygame.time.Clock().tick(10)

        return True

    except Exception as e:
        print(f"Error in TTS: {e}")

    finally:
        try:
            func(False)
            if pygame.mixer.get_init():  # Check if mixer was initialized
                pygame.mixer.music.stop()
                pygame.mixer.quit()
        except Exception as e:
            print(f"Error in finally block: {e}")

def TextToSpeech(Text, func=lambda r=None: True):
    Data = str(Text).split(".")

    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]

    if len(Data) > 4 and len(Text) > 250:
        TTS(" ".join(Data[0:2]) + ". " + random.choice(responses), func)
    else:
        TTS(Text, func)

if __name__ == "__main__":
    while True:
        try:
            TextToSpeech(input("Enter the text: "))
        except KeyboardInterrupt:
            print("\nProgram exited.")
            break





























# import random
# import pyttsx3
# from dotenv import dotenv_values

# # Load environment variables
# env_vars = dotenv_values(".env")
# AssistantVoice = env_vars.get("AssistantVoice")

# class TTSEngine:
#     def __init__(self):
#         self.engine = pyttsx3.init()
#         self._configure_voice()
        
#     def _configure_voice(self):
#         """Configure the voice based on environment settings"""
#         if AssistantVoice:
#             voices = self.engine.getProperty('voices')
#             for voice in voices:
#                 if AssistantVoice in voice.id:
#                     self.engine.setProperty('voice', voice.id)
#                     break
#         # Set reasonable default rate (words per minute)
#         self.engine.setProperty('rate', 150)
        
#     def speak(self, text, stop_flag=lambda: False):
#         """Speak the given text, with optional stop flag checking"""
#         try:
#             # Queue the text to be spoken
#             self.engine.say(text)
            
#             # Start speech in a non-blocking way
#             self.engine.startLoop(False)
            
#             # Check the stop flag periodically
#             while self.engine.isBusy():
#                 if stop_flag():
#                     self.engine.endLoop()
#                     return False
#                 self.engine.iterate()
                
#             return True
#         except Exception as e:
#             print(f"Error in speech synthesis: {e}")
#             return False
#         finally:
#             self.engine.stop()

# def TextToSpeech(Text, stop_flag=lambda: False):
#     Data = str(Text).split(".")

#     responses = [
#         "The rest of the result has been printed to the chat screen, kindly check it out sir.",
#         "The rest of the text is now on the chat screen, sir, please check it.",
#         "You can see the rest of the text on the chat screen, sir.",
#         "The remaining part of the text is now on the chat screen, sir.",
#         "Sir, you'll find more text on the chat screen for you to see.",
#         "The rest of the answer is now on the chat screen, sir.",
#         "Sir, please look at the chat screen, the rest of the answer is there.",
#         "You'll find the complete answer on the chat screen, sir.",
#         "The next part of the text is on the chat screen, sir.",
#         "Sir, please check the chat screen for more information.",
#         "There's more text on the chat screen for you, sir.",
#         "Sir, take a look at the chat screen for additional text.",
#         "You'll find more to read on the chat screen, sir.",
#         "Sir, check the chat screen for the rest of the text.",
#         "The chat screen has the rest of the text, sir.",
#         "There's more to see on the chat screen, sir, please look.",
#         "Sir, the chat screen holds the continuation of the text.",
#         "You'll find the complete answer on the chat screen, kindly check it out sir.",
#         "Please review the chat screen for the rest of the text, sir.",
#         "Sir, look at the chat screen for the complete answer."
#     ]

#     tts_engine = TTSEngine()
    
#     if len(Data) > 4 and len(Text) > 250:
#         tts_engine.speak(" ".join(Data[0:2]) + ". " + random.choice(responses), stop_flag)
#     else:
#         tts_engine.speak(Text, stop_flag)

# if __name__ == "__main__":
#     while True:
#         try:
#             TextToSpeech(input("Enter the text: "))
#         except KeyboardInterrupt:
#             print("\nProgram exited.")
#             break