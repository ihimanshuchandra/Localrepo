import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random
import smtplib

# Microsoft API takes audio input from Windows
engine = pyttsx3.init('sapi5')  
voices = engine.getProperty('voices')
# print(voices)
# print(voices[0].id)
engine.setProperty('voice', voices[0].id)

# Speak Function
def speak(audio):               
    engine.say(audio)
    engine.runAndWait()

# wishme function
def wishme():                    
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening")

    speak("Hello, I am Octopus! Please tell me how may I help you.")

# It takes microphone input from the user and gives string output
def takeCommand():               
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening..")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing..")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        #print(e)
        print("Say that again, please...")
        return "None"
    return query

#Email send function
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('maharahul801@gmail.com', 'Kingkong12@')
    server.sendmail('himuchandra100@gmail.com', to, content)
    server.close()

# Function to exit Octopus and say goodbye
def exit_octopus():
    speak("Goodbye! Have a great day.")
    exit()

# main function
if __name__ == "__main__":  
    wishme()
    while True:
    # if 1:
        query = takeCommand().lower() #Converting user query into lower case

        # Logic for executing tasks based on query
        if 'wikipedia' in query:  #if wikipedia found in the query then this block will be executed
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2) 
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")

        elif 'play music' in query:
             music_dir = r'C:\Users\AU008TX\Downloads\Meal'
             songs = os.listdir(music_dir)
             print(songs)

             # Generate a random index to select a random song
             random_index = random.randint(0, len(songs) - 1)

             # Play the randomly selected song
             os.startfile(os.path.join(music_dir, songs[random_index]))


        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            codePath = r'C:\Users\AU008TX\AppData\Local\Programs\Microsoft VS Code\Code.exe'
            os.startfile(codePath)
        
        elif 'email to harry' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "himuchandra1002@gmail.com"    
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry. I am not able to send this email")

        # Exit command
        elif 'stop octopus' in query:
            exit_octopus()