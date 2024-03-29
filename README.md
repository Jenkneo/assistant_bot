# Голосовой ассистент

## Описание
Однозначно каждый программист мечтал о своем голосовом ассистенте, 
к которому он сможет не только обратится за какой то информацией,
но и просто поболтать о чем угодно.

Точно также думал и я, поэтому создал своего ассистента, 
которому можно задать любые вопросы. (Которые вы должны конечно же прописать самостоятельно 🙃)

> ⚠️ **Это не нейросеть**

![preview img](anime_girl.gif)

## Принцип работы
Методом перебора и неточного сравнения при помощи библиотеки FuzzyWuzzy 
перебираются json-файлы из папки _smalltalk_module/intents_. 

В каждом json-файле содержатся поля:
- **keywords** - обязательные слова, одно из которых должно присутствовать в сообщении
- **messages** - примеры сообщений от пользователя 
- **answers** - ответ

Помимо вышеперечисленных полей, там также присутсвуют поля:
- **commands** - отвечает за выполнение какой-либо функции из command_module/commands.py
- **cmd** - выполняет Windows CMD команду
- **dialog** - указывает на то, стоит ли продолжать диалог

> ⚠️ На данный момент комманд практически нет, но как пример - можно посмотреть погоду из smalltalk.command.weather.json

Настройки для перебора json содержатся в _smalltalk_module/smalltalk.py_

## Технологии
- Библиотека [Silero](https://silero.ai/) для генерации голоса
- Модель распознавания речи [VOSK](https://alphacephei.com/vosk/models) - vosk-model-small-ru-0.22
- Smalltalk intents из [Google DialogFlow](https://dialogflow.cloud.google.com/)


За основу проекта взят пример из [видео](https://www.youtube.com/watch?v=XTeGvaDaraI) от [ХаудиХо](https://www.youtube.com/@HowdyhoNet)

## Дополнительные возможности
Smalltalk модуль не обязательно использовать в связке с голосом. 
Данный модуль также прекрасно можно подключить в бота, который сможет отвечать на простенькие вопросы.