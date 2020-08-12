import speech_recognition as sr 

record = sr.Recognizer()
microphone = sr.Microphone()
while True:
    with microphone as source:
        record.adjust_for_ambient_noise(source)
        audio = record.listen(source)
        result = record.recognize_google(audio, language='ru_RU')
        result = result.lower()
        print(result)