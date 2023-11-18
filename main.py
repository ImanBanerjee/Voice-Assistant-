# Import the required libraries
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import os
import pywhatkit  # Added for playing songs
import requests 

# Initialize the speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
engine = pyttsx3.init()

class VoiceAssistant:
    def __init__(self):
        self.stopped = False

    # Function to set the voice to female
    def set_female_voice(self):
        voices = engine.getProperty('voices') 
        engine.setProperty('voice', voices[1].id)   
        female_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\SPEECH\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"

    # Function to play a song
    def play_song(self, song_name):
        try:
            search_query = f"youtube.com/results?search_query={song_name}"
            url = f"https://{search_query}"

            webbrowser.open(url)
            print(f"Playing the song: {song_name}")

        except Exception as e:
            print(f"Couldn't find the song {song_name}. Error: {e}")

    # Function to speak
    def speak(self, text):
        engine.say(text)
        engine.runAndWait()

    # Function to recognize speech
    def take_command(self):
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

            try:
                statement = recognizer.recognize_google(audio, language='en-in')
                print(f"User: {statement}\n")
                return statement.lower()

            except sr.UnknownValueError:
                print("Sorry, I didn't get that.")
                return None
            except sr.RequestError as e:
                print(f"Request Error: {e}")
                return None

    # Function to greet the user
    def greet(self):
        self.speak("Hello! How can I assist you today?")

    # Function to perform basic tasks
    # Function to perform basic tasks
    def perform_task(self, statement):
       if "how are you" in statement:
        self.speak("I'm doing well, thank you!")
       elif "what's your name" in statement:
        self.speak("I am Lexa.")
       elif "what can you do" in statement:
        self.speak("I can answer your questions, search the web, play songs, and more.")
       elif "what's your owner's name" in statement:
        self.speak("My owner's name is Lexo, also known as Iman.")
       elif "search" in statement:
        search_query = statement.replace("search", "")
        self.speak(f"Searching for {search_query} on the web.")
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
       elif "play a song" in statement:
        song_name = statement.replace("play a song", "").strip()
        self.play_song(song_name)
       elif "goodbye" in statement or "bye" in statement:
        self.speak("Goodbye! Have a great day.")
        exit()
       elif "wikipedia of" in statement:
        query = statement.replace("wikipedia of", "").strip()
        self.search_wikipedia(query)
       elif "weather in" in statement:
            city = statement.replace("weather in", "").strip()
            self.get_weather_with_aqi(city)


       else:
        self.speak("I'm sorry, I didn't understand that.")

            # Wikipedia search feature
            # Wikipedia search feature
    def search_wikipedia(self, query):
       try:
         # Search for the Wikipedia page related to the query
        page = wikipedia.page(query)
        page_url = page.url
        print(f"Opening Wikipedia page: {page_url}")
        webbrowser.open(page_url)

        # Read the summary of the Wikipedia page
        summary = wikipedia.summary(query, sentences=2)  # Adjust the number of sentences as needed
        print(f"Wikipedia Summary: {summary}")
        self.speak(summary)
       except wikipedia.exceptions.DisambiguationError as e:
        print(f"Multiple matches found. Please specify your query: {e.options}")
        self.speak("Multiple matches found. Please specify your query.")
       except wikipedia.exceptions.HTTPTimeoutError:
        print("Wikipedia search failed due to a timeout error. Please try again later.")
        self.speak("Wikipedia search failed due to a timeout error. Please try again later.")
       except wikipedia.exceptions.PageError:
        print(f"No Wikipedia page found for {query}.")
        self.speak(f"No Wikipedia page found for {query}")

         # Function to get the weather information
    def get_weather_with_aqi(self, city):
        try:
            api_key = '57ebaed63fae4c149e5115051231711'
            base_url = f'https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=yes'
            response = requests.get(base_url)

            if response.status_code == 200:
                weather_data = response.json()
                temperature_celsius = weather_data['current']['temp_c']
                condition = weather_data['current']['condition']['text']
                aqi = weather_data['current']['air_quality']['us-epa-index']

                weather_report = f"The weather in {city} is {condition} with a temperature of {temperature_celsius} degrees Celsius. AQI: {aqi}"
                print(weather_report)
                self.speak(weather_report)
            else:
                print(f"Failed to fetch weather data. Status code: {response.status_code}, Response: {response.text}")
                self.speak("Sorry, I couldn't fetch weather information at the moment.")
        except Exception as e:
            print(f"Error fetching weather information: {e}")
            self.speak("Sorry, I couldn't fetch weather information at the moment.")

    def stop_listening(self):
        self.stopped = True

    def listen(self):
        self.set_female_voice()
        self.greet()
        while not self.stopped:
            self.speak("What can I do for you?")
            statement = self.take_command()
            if statement:
                self.perform_task(statement)


# Run the main function
if __name__ == "__main__":
    voice_assistant = VoiceAssistant()
    voice_assistant.listen()
