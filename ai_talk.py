import pyttsx3
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import subprocess
import webbrowser
import requests
import time

API_KEY = ""

def ask_openrouter(question):
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    
    data = {
        "model": "openrouter/free",
        "messages": [
            {"role": "system", "content": "Ты полезный голосовой помощник. Отвечай кратко и по делу."},
            {"role": "user", "content": question}
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Ошибка при обращении к OpenRouter: {e}")
        return "Извините, произошла ошибка при обращении к нейросети"

while True:
    engine = pyttsx3.init()  # object creation
    duration = 5
    sample_rate = 44100
    language = 'ru-RU'
    print('говори....')
    recording = sd.rec(int(duration * sample_rate),
                        samplerate=sample_rate,
                        channels=1,
                        dtype='int16'
                        )
    sd.wait()

    wav.write('output.wav', sample_rate, recording)
    print('запись завершена, идет распознавание')
    recognizer = sr.Recognizer()
    with sr.AudioFile('output.wav') as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language=language)
        print("Вы сказали:", text)
        volume = engine.getProperty('volume')
        print(volume)
        engine.setProperty('volume', 1.0)


        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)

        if 'Привет' in text:
            engine.say('Привет Как у тебя дела')
            engine.runAndWait()
                
        elif 'Telegram' in text and 'Открой' in text:
            engine.say('Сейчас открою')
            time.sleep(1)
            engine.runAndWait()
            subprocess.call("D:\\Telegram Desktop\\Telegram.exe")
            
        elif 'Гугл' in text and 'Открой' in text:
            engine.say('Сейчас открою')
            time.sleep(1)
            engine.runAndWait()
            subprocess.call("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
            
        elif 'Открой' in text and 'YouTube' in text:
            engine.say('Сейчас открою')
            time.sleep(1)
            engine.runAndWait()
            webbrowser.open_new_tab('https://www.youtube.com/')
            
        else:
            
            engine.say('Сейчас подумаю...')
            time.sleep(1)
            
            
            
            ai_response = ask_openrouter(text)
            print("Ответ нейросети:", ai_response)
            
           
            engine.say(ai_response)
            engine.runAndWait()
                    
    except Exception as e:
        print('Ошибка', e)
