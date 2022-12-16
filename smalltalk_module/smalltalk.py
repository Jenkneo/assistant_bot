import os
import sys
import re
import json
from fuzzywuzzy import fuzz
import random
from config import DEBUG

sys.path.insert(0, os.path.join(os.getcwd(), '..'))

# https://pypi.org/project/fuzzywuzzy/ Типы - "RATIO", "P_RATIO", "T_SORT_RATIO", "T_SET_RATIO"
COMPARISON = "RATIO"

# Использование ключевых слов (улучшает выборку)
USE_KEYWORDS = False

# Разница для выбора False предложения (При USE_KEYWORDS)
MAX_COMPARISON_DIFFERENCE = 20

# Минимальный порог сравнения (0-100)
MIN_COMPARISON_THRESHOLD = 50

if MIN_COMPARISON_THRESHOLD < 0:
    print("MIN_COMPARISON_THRESHOLD и/или MAX_COMPARISON_DIFFERENCE не может быть менее 0.")
    exit(0)


class Smalltalk:
    # Используется для получения ответа
    def smalltalk(self, user_input):
        intent = self.__base_logic(self.__prettyfier(user_input))
        with open("smalltalk_module/intents/" + intent, encoding='utf8') as intent_file:
            file_dict = json.loads(intent_file.read())
            answer = random.choice(file_dict["answers"])
            send_answ = {"answer": answer, "cmd": file_dict["cmd"], 'command': file_dict["commands"],
                         "dialog": file_dict["dialog"]}
            if DEBUG:
                print(f'[SMALLTALK] from {intent} use {answer}')
            return send_answ

    def __base_logic(self, user_input):
        if user_input.split(" ")[0] == "открой":
            return "smalltalk.command.open.json"
        true_intent_score = 0
        true_intent_name = ""
        false_intent_score = 0
        false_intent_name = ""

        for intent in os.listdir("smalltalk_module/intents"):
            with open("smalltalk_module/intents/" + intent, encoding='utf8') as intent_file:
                parce_dict = json.loads(intent_file.read())
            messages = parce_dict["messages"]
            answers = parce_dict["answers"]
            keywords = parce_dict["keywords"]

            if USE_KEYWORDS: this_intent_keywords = False

            intent_score_list = []
            for message in messages:
                if message == user_input: intent_score_list = [100]

                if COMPARISON == "RATIO":
                    intent_score_list.append(fuzz.ratio(message, user_input))
                elif COMPARISON == "P_RATIO":
                    intent_score_list.append(fuzz.partial_ratio(message, user_input))
                elif COMPARISON == "T_SORT_RATIO":
                    intent_score_list.append(fuzz.token_sort_ratio(message, user_input))
                elif COMPARISON == "T_SET_RATIO":
                    intent_score_list.append(fuzz.token_set_ratio(message, user_input))

                if USE_KEYWORDS:
                    for keyword in keywords:
                        if keyword in user_input: this_intent_keywords = True
            if intent_score_list:
                if MIN_COMPARISON_THRESHOLD < max(intent_score_list):
                    if USE_KEYWORDS and this_intent_keywords and true_intent_score < max(intent_score_list):
                        true_intent_score = max(intent_score_list)
                        true_intent_name = intent
                    elif false_intent_score < max(intent_score_list):
                        false_intent_score = max(intent_score_list)
                        false_intent_name = intent
            else:
                continue

        if DEBUG:
            if USE_KEYWORDS: print("[SMALLTALK] TRUE: " + true_intent_name + " - " + str(true_intent_score))
            print("[SMALLTALK] FALSE: " + false_intent_name + " - " + str(false_intent_score))

        if true_intent_score == 100:
            return true_intent_name
        elif false_intent_score == 100:
            return false_intent_name

        if USE_KEYWORDS:
            if true_intent_score != 0:
                if true_intent_score >= false_intent_score:
                    return true_intent_name
                elif false_intent_score - true_intent_score >= MAX_COMPARISON_DIFFERENCE:
                    return false_intent_name
                else:
                    return true_intent_name
            elif false_intent_score != 0:
                return false_intent_name
            else:
                return "smalltalk.unknown.json"
        elif false_intent_score != 0:
            return false_intent_name
        else:
            return "smalltalk.unknown.json"

    def __prettyfier(self, user_input):
        split_message = []
        for word in re.split(r'\s+|[,*&^%#;?!()_.-]\s*', user_input.lower()):
            if word != '': split_message.append(word)
        message = ""
        for word in split_message:
            message = message + " " + word
        return message[1:]


# Тестирование системы реагирования
if __name__ == "__main__":
    bot = Smalltalk()
    print("bot:" + bot.smalltalk(input("You:")))
