import smalltalk_module.smalltalk as talk
from config import VOICE, DEBUG
from playsound import playsound
from command_module.commands import *

logic = talk.Smalltalk()

if VOICE:
    import voice_module.voice_recognition as vr
    import voice_module.voice_generator as vg

    user_speech = vr.VoiceRecognition()
    bot_voice = vg.Speaker()

    dialog = False
    while True:
        if not dialog:
            if DEBUG: print("[MAIN] CHANGE MODE TO WAIT CALL")
            user_speech.wait_call()
        dialog = False

        if DEBUG: print("[MAIN] CHANGE MODE TO WAIT COMMAND")
        playsound("sound.mp3", block=False)

        user_input = user_speech.wait_command();
        if user_input == None:
            if DEBUG: print('[MAIN] SPEECH NOT FOUND')
            continue
        print(f"Вы: {user_input}")
        answer_dict = logic.smalltalk(user_input)
        dialog = answer_dict['dialog']

        if answer_dict['command'] != None:
            answer = eval(answer_dict['command'] + '(\"' + user_input + '\")')
        elif answer_dict['cmd'] != None:
            os.system(answer_dict['cmd'])
            answer = "Сделано."
        else:
            answer = answer_dict["answer"]
        print(f'Каталина: {answer}')
        bot_voice.say(answer)

# else:
#     while True:
#         user_input = input("You: ")
#         type_command = chat_module(user_input)
#         print(f'Каталина: {bot_answer(type_command, logic.smalltalk(user_input))}')

