import speech_recognition as sr
import webbrowser
import pyttsx3
import time
import music_library
from google import genai

# ---------------- INIT ----------------
recognizer = sr.Recognizer()
client = genai.Client (api_key="API")


# ---------------- SPEAK ----------------
def speak(text):

    print("Jarvis:", text)

    engine = pyttsx3.init(driverName='sapi5')
    engine.setProperty('rate', 170)

    engine.say(str(text))
    engine.runAndWait()
    engine.stop()

    time.sleep(0.2)


# ---------------- AI ----------------
def aiprocess(command):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Answer in short, max 1-2 sentences: {command}"
        )

        return response.text if response.text else "I couldn't generate a response"

    except Exception as e:
        return f"AI error: {e}"


# ---------------- COMMAND HANDLER ----------------
def processcommand(c):
    c = c.lower()

    if "open google" in c:
        webbrowser.open("https://google.com")

    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")

    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")

    elif "open instagram" in c:
        webbrowser.open("https://instagram.com")

    elif c.startswith("play"):
        parts = c.split(" ")

        if len(parts) > 1:
            song = parts[1]

            if song in music_library.music:
                webbrowser.open(music_library.music[song])
            else:
                speak("Song not found")
        else:
            speak("Please tell a song name")

    else:
        output = aiprocess(c)
        speak(output)


# ---------------- MAIN LOOP ----------------
if __name__ == "__main__":
    print("main.py started")
    speak("Initializing Jarvis")

    while True:
        try:
            print("Waiting for wake word...")

            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=3
                )

            word = recognizer.recognize_google(audio)
            print("Heard:", word)

            if word.lower() == "jarvis":
                speak("Jarvis activated")

                # IMPORTANT: speak OUTSIDE mic block
                with sr.Microphone() as source:
                    print("Listening command...")
                    recognizer.adjust_for_ambient_noise(source)

                    audio = recognizer.listen(
                        source,
                        timeout=5,
                        phrase_time_limit=5
                    )

                command = recognizer.recognize_google(audio)
                print("Command:", command)

                processcommand(command)

        except sr.WaitTimeoutError:
            print("No speech detected")

        except sr.UnknownValueError:
            print("Could not understand audio")

        except Exception as e:
            print("Error:", e)