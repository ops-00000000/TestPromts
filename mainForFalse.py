import re

from yandex_cloud_ml_sdk import YCloudML
import pandas as pd
import json
from dotenv import load_dotenv
import os
import Anal

load_dotenv()

YANDEX_USER = os.getenv("YANDEX_USER")
FOLDER_ID = os.getenv("FOLDER_ID")

csv_file_path = 'FalseTable.csv'
df = pd.read_csv(csv_file_path, sep=';', encoding='utf-8')

columns_to_drop = ['Статус', 'Дата изменения', 'Полное название организации',
                   'Выберите направление социальной задачи ( До 3х напрвлений)']
df = df.drop(columns=columns_to_drop)

system_message = {
    "role": "system",
    "text": """
    Отмодерируй заявки так, чтобы каждый её элемент соответствовали критериям и четко напиши где проблемы есть, а где их нет. Свой ответ внести в JSON таблицу(структура должна быть такой:элемент таблицы ->  корректность(True/False), комментарий -> прислать текст только при несоответствии, Откорректированный текст -> Добавить улучшенный текст пользователя который подходил бы под критерии.). Список элементов таблицы: ID, SocialTaskName, Description, TargetAudience, MechanismOfActions, DesiredOutcome.
    Поле ID не нужно проверять на корректность, просто возьми цифру ID из исходных данных. 

           Критерии оценки заявок

        Наименование социальной задачи
            Избегает эмоциональности, коммерческой рекламы или внутренних задач организации.
        Описание социальной задачи и связь с организацией
            Задача описывает актуальную социальную проблему и её значение.
            Роль обучающегося в решении задачи ясна и активна.
            Может быть большим по объему.
        Целевая аудитория (благополучатели)
            Названа конкретная внешняя группа, нуждающаяся в помощи (не участники проекта или организация).
            Указано, в чём состоит их потребность или проблема (можно кратко).
        Механизм действий
            Описаны шаги или действия, которые выполнит обучающийся.
            Есть намёк на обучающий процесс (например, анализ, взаимодействие, рефлексия), а не только волонтёрство.
            Механизм достижим и логичен.
            Может быть большим по объему.
        Желаемый продукт или результат
            Результат конкретен, измерим и полезен для благополучателей.
            Достижим в рамках проекта одним обучающимся (без нереалистичных масштабов).
            Может быть большим по объему.

    Помни, что твоя задача отмодерировать заявки(поставить везде True), при выполнении критериев.


    """
}

sdk = YCloudML(
    folder_id=FOLDER_ID,
    auth=YANDEX_USER,
)


def clean_json_string(response_text):
    cleaned_text = re.sub(r'^```[\s\S]*?\n([\s\S]*?)\n```$', r'\1', response_text, flags=re.MULTILINE)
    cleaned_text = cleaned_text.strip()
    return cleaned_text


responses_list = []

for row_dict in df.head(20).to_dict(orient='records'):
    json_str = json.dumps(row_dict)

    user_message = {
        "role": "user",
        "text": json_str
    }
    messages = [system_message, user_message]

    result = sdk.models.completions("yandexgpt").configure(temperature=0.5).run(messages)

    for alternative in result:
        json_text = clean_json_string(alternative.text)
        print(json_text)
        responses_list.append(json_text)

Anal.generate_graphs(responses_list)
