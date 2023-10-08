#import libraries
import pyttsx3
import datetime
import time
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
# Define a chat history list to keep track of the conversation
chat_history = []


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
    speak("Tell the password")
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

# 9) Function to interact with OpenAI for chat
def ai(prompt):
    try:
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
        
        response_text = response["choices"][0]["text"]
        text += response_text
        
        # Create a folder named "openai" if it doesn't exist
        if not os.path.exists("openai"):
            os.mkdir("openai")

        # Generate a unique filename based on the response content
        filename = f"openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt"
        
        # Save the response to a text file
        with open(filename, "w") as f:
            f.write(text)
            
        return response_text
    except Exception as e:
        # Handle any exceptions that may occur during the OpenAI request
        print(f"Error communicating with OpenAI: {str(e)}")
        return "An error occurred while communicating with OpenAI."

# Example usage:
#response = ai("Generate a creative story about space exploration.")
#print(response)

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

            elif "chat with ai" in query.lower():
                speak("Sure! What would you like to chat about?")
                openai_enabled = True
                chat_history = []  # Initialize an empty chat history
                while openai_enabled:
                    user_input = takeCommand().lower()
                    if 'close ai' in user_input:
                        openai_enabled = False
                        speak("I'm closing the chat with AI.")
                        break

                    # Check for the "reset" command
                    if 'reset' in user_input:
                        chat_history = []  # Reset the chat history
                        speak("Chat history has been reset.")

                    # Add the user's input to the chat history
                    chat_history.append(f"You: {user_input}")

                    # Create a prompt by joining the chat history
                    prompt = "\n".join(chat_history)

                    # Get response from OpenAI
                    openai_response = ai(prompt)

                    # Append OpenAI's response to the chat history
                    chat_history.append(f"AI: {openai_response}")

                    # Speak OpenAI's response
                    speak(openai_response)

                    # Save the chat history to a text file
                    with open("chat_history.txt", "w") as chat_file:
                        chat_file.write("\n".join(chat_history))

