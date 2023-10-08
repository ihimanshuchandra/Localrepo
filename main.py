#import libraries
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random
import smtplib
import psutil
import openai
from config import apikey
from config import password

# Initialize chatStr
chatStr = ""  # Initialize chatStr
openai_enabled = False  # Flag to control OpenAI interaction
openai_response = ""  # Store the response from OpenAI


# 1) Microsoft API takes audio input from Windows
engine = pyttsx3.init('sapi5')  
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


# 2) Add more websites here as needed
websites = [
    ["youtube", "https://www.youtube.com"],
    ["wikipedia", "https://www.wikipedia.org"],
    ["google", "https://www.google.com"],
    ["stackoverflow", "https://stackoverflow.com"],
    ["github", "https://github.com"],
    ["amazon", "https://www.amazon.com"],
    ["twitter", "https://twitter.com"],
    ["facebook", "https://www.facebook.com"],
    ["linkedin", "https://www.linkedin.com"],
    ["instagram", "https://www.instagram.com"],
    ["reddit", "https://www.reddit.com"],
    ["ebay", "https://www.ebay.com"],
    ["quora", "https://www.quora.com"],
    ["bing", "https://www.bing.com"],
    ["pinterest", "https://www.pinterest.com"],
    ["netflix", "https://www.netflix.com"],
    ["spotify", "https://www.spotify.com"],
    ["apple", "https://www.apple.com"],
    ["microsoft", "https://www.microsoft.com"],
    ["yahoo", "https://www.yahoo.com"],
]

# 3) Check password function
def check_password():
    speak("Please say the password to continue.")
    entered_password = takeCommand().lower()
    
    # You can replace this with a more complex password
    actual_password = password 
    
    if entered_password == actual_password:
        speak("Authentication successful. How may I help you?")
        return True
    else:
        speak("Authentication failed. Please try again.")
        return False

# 4) Speak Function
def speak(audio):               
    engine.say(audio)
    engine.runAndWait()

# 5) wishme function
def wishme():                    
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening")

    speak("Hello, I am Octopus!")

# 6) Take command-It takes microphone input from the user and gives string output
def takeCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        # Adjust the parameters for better listening
        r.pause_threshold = 1
        r.phrase_threshold = 0.3
        r.non_speaking_duration = 0.8

        r.adjust_for_ambient_noise(source)
        print("Listening...")
        try:
            audio = r.listen(source, timeout=5)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
            return query.lower()
        except sr.WaitTimeoutError:
            print("Listening timeout. Please try again.")
            return "None"
        except sr.UnknownValueError:
            print("Could not understand audio. Please try again.")
            return "None"
        
# 7) Play music
def play_music():
    music_dir = r'C:\Users\AU008TX\Downloads\Meal'
    songs = os.listdir(music_dir)
    print(songs)

    speak("Do you want to play a specific song? If yes, please say the song name.")
    specific_song_query = takeCommand().lower()

    if 'yes' in specific_song_query:
        speak("Please tell me the name of the song you want to play.")
        song_to_play = takeCommand().lower()

        # Check if the specified song is in the list of available songs
        if song_to_play in songs:
            song_path = os.path.join(music_dir, song_to_play)
            os.startfile(song_path)
        else:
            speak(f"Sorry, I couldn't find the song {song_to_play}. Playing a random song.")
            # Generate a random index to select a random song
            random_index = random.randint(0, len(songs) - 1)
            os.startfile(os.path.join(music_dir, songs[random_index]))
    else:
        # User didn't specify a song, play a random song
        speak("Playing a random song.")
        # Generate a random index to select a random song
        random_index = random.randint(0, len(songs) - 1)
        os.startfile(os.path.join(music_dir, songs[random_index]))


# 8) Change the currently playing song
def change_song():
    # Check if Windows Media Player is running
    for process in psutil.process_iter(attrs=['name']):
        if process.info['name'] == 'wmplayer.exe':
            # If it's running, close it
            subprocess.Popen(["taskkill", "/f", "/im", "wmplayer.exe"], shell=True)
            break
    
    play_music()  # Play a new random song

# 9)
def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"User: {query}\n Jarvis: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    speak(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]

# 9) Function to interact with OpenAI for chat
def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    # print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    # with open(f"Openai/prompt- {random.randint(1, 2343434356)}", "w") as f:
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)

# 10) Function to exit Octopus and say goodbye
def exit_octopus():
    speak("Goodbye! Hope we talk soon.")
    exit()

# main function
if __name__ == "__main__":
    wishme()
    authenticated = False

    while True:
        if not authenticated:
            query = takeCommand().lower()
            if 'stop octopus' in query:
                exit_octopus()
            elif 'password' in query:
                authenticated = check_password()
            else:
                speak("You must enter the password to proceed.")
        else:
            query = takeCommand().lower()
            if 'stop octopus' in query:
                exit_octopus()
            elif 'open' in query:
                for website in websites:
                    if website[0] in query:
                        speak(f"Opening {website[0]}...")
                        webbrowser.open(website[1])
                        break

           # Logic for executing tasks based on query
            elif 'wikipedia' in query:
                speak('Searching Wikipedia...')
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2) 
                speak("According to Wikipedia")
                print(results)
                speak(results)

            elif 'open youtube' in query:
                webbrowser.open("youtube.com")

            elif 'play some music' in query:
                play_music()

            elif 'change song' in query:  # Command to change the song
                change_song()


            elif 'the time' in query:
                hour = datetime.datetime.now().strftime("%H")
                min = datetime.datetime.now().strftime("%M")
                speak(f"Sir time is {hour} hours and {min} minutes")

            elif 'open code' in query:
                codePath = r'C:\Users\AU008TX\AppData\Local\Programs\Microsoft VS Code\Code.exe'
                os.startfile(codePath)

            elif 'email to harry' in query:
                try:
                    speak("What should I say?")
                    content = takeCommand().lower()
                    to = "himuchandra1002@gmail.com"    
                    sendEmail(to, content)
                    speak("Email has been sent!")
                except Exception as e:
                    print(e)
                    speak("Sorry. I am not able to send this email")

            elif "chat with ai".lower() in query.lower():
                ai(prompt=query)

            elif "Jarvis stop".lower() in query.lower():
                exit()

            elif "reset".lower() in query.lower():
                chatStr = ""

            else:
                print("Chatting...")
                chat(query)
