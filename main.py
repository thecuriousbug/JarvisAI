import os
from openai import OpenAI
import speech_recognition as sr
import win32com.client
import webbrowser
from config import API_KEY, Weather_api_key
import datetime
import requests

weatherapikey = Weather_api_key
chatStr = ""


def chat(query):
    global chatStr
    client = OpenAI(api_key=API_KEY)
    chatStr += f"Sagar : {query}\n Jarvis : "

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{chatStr}"}
        ],

    )
    say(completion.choices[0].message.content)
    chatStr += f"{completion.choices[0].message.content}\n"
    return completion.choices[0].message.content


def ai(prompt):
    client = OpenAI(api_key=API_KEY)
    text = f"OpenAI response for prompt :{prompt} \n ****************\n\n"

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{prompt}"}
        ],

    )
    # print(completion.choices[0].message.content)
    text += completion.choices[0].message.content
    if not os.path.exists("OpenAI"):
        os.mkdir("OpenAI")

    with open(f"OpenAI/{''.join(prompt.split('write')[1:]).strip()}.txt", "w") as f:
        f.write(text)
    say("Task Done, Saved in your Directory")


def weather(city):
    weather_data = requests.get(f"https://api.tomorrow.io/v4/weather/realtime?location={city}&apikey={weatherapikey}")
    temp_in_c = weather_data.json()['data']['values']['temperature']

    say(f"Weather of {city} is {temp_in_c} degree celsius")


def say(text):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(text)


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some error occured. Sorry from Jarvis"


if __name__ == '__main__':

    say("hello I am Jarvis AI how can i help you")
    while True:
        print("Listening...")
        query = takeCommand()
        command_executed = False

        sites = [["youtube", "https://www.youtube.com"],
                 ["wikipedia", "https://www.wikipedia.com"],
                 ["google", "https://www.google.com"],
                 ["spotify", "https://open.spotify.com/"],
                 ["chat GPT", "https://chat.openai.com/chat"]]

        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} ")
                webbrowser.open(site[1])
                command_executed = True
                break

                # Check the flag before going to chat(query)
        if command_executed:
            continue  # Go back to listening

        if "open music".lower() in query.lower():
            try:
                say("opening music player")
                musicpath = r"C:\Users\deeps\Downloads\vinee-heights-126947.mp3"

                os.startfile(musicpath)
                continue  # Go back to listening
            except Exception as e:

                say("Some error occured. Sorry from Jarvis")


        elif "open chrome".lower() in query.lower():
            apppath = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
            say("opening chrome")
            os.startfile(apppath)
            continue  # Go back to listening

        elif "the time".lower() in query.lower():
            time = datetime.datetime.now().strftime("%H:%M")
            say(f"the time is {time}")
            continue  # Go back to listening

        elif "write".lower() in query.lower():
            ai(prompt=query)
            continue  # Go back to listening

        elif "weather information".lower() in query.lower():
            say("sure please tell me the city name")
            city_name = takeCommand()
            weather(city_name)
            continue  # Go back to listening

        elif "jarvis sleep".lower() in query.lower():
            say("Bye Bye")
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""
            say("Task Done")
            continue  # Go back to listening

        else:
            chat(query)




