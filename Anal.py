import json
import matplotlib.pyplot as plt
import numpy as np


api_responses = [
    '[\n  {\n    "ID": 364612,\n    "SocialTaskName": "АВТОНОМНАЯ НЕКОММЕРЧЕСКАЯ ОРГАНИЗАЦИЯ ПО РЕАЛИЗАЦИИ ПРОЕКТА В СФЕРЕ РАЗВИТИЯ ГОРОДОВ И ЦИФРОВОЙ ТРАНСФОРМАЦИИ ГОРОДСКОГО ХОЗЯЙСТВА",\n    "корректность": false,\n    "комментарий": "Название слишком длинное и не отражает суть социальной проблемы и действий обучающегося.",\n    "Откорректированный текст": "Проект по развитию городской среды и цифровой трансформации городского хозяйства"\n  },\n  {\n    "Description": "Формирование сообществ недостаточно обеспеченных жителей, готовых участвовать в проектах по развитию своих территорий...",\n    "корректность": true\n  },\n  {\n    "TargetAudience": "Жители муниципальных образований Российской Федерации",\n    "корректность": true\n  },\n  {\n    "MechanismOfActions": "Сбор, анализ, систематизация и размещение контента для информационно-аналитического портала проекта по цифровизации городского хозяйства...",\n    "корректность": true\n  },\n  {\n    "DesiredOutcome": "Регулярно обновляемые информационные ресурсы проекта «Умный город» в соответствии с установленным планом и требованиями к оформлению...",\n    "корректность": true\n  }\n]',
    '[\n    {\n        "ID": 364865,\n        "SocialTaskName": {\n            "корректность": true,\n            "комментарий": null,\n            "Откорректированный текст": null\n        },\n        "Description": {\n            "корректность": false,\n            "комментарий": "Описание слишком длинное и содержит много лишней информации, не связанной напрямую с социальной задачей и ролью обучающегося.",\n            "Откорректированный текст": "Проект направлен на организацию спортивных мероприятий для детей и взрослых с ОВЗ, способствуя их социальной адаптации и улучшению физического здоровья. Обучающийся будет помогать в организации и проведении игр, а также в обучении участников спортивным навыкам."\n        },\n        "TargetAudience": {\n            "корректность": true,\n            "комментарий": null,\n            "Откорректированный текст": null\n        },\n        "MechanismOfActions": {\n            "корректность": false,\n            "комментарий": "Механизм действий описан слишком общим образом, без конкретных шагов или обучающего процесса.",\n            "Откорректированный текст": "Обучающийся будет участвовать в планировании и организации спортивных мероприятий, помогать в обучении участников, анализировать результаты и разрабатывать рекомендации для улучшения."\n        },\n        "DesiredOutcome": {\n            "корректность": false,\n            "комментарий": "Результат не конкретен и не измерим, не указано, как будет оцениваться успех проекта.",\n            "Откорректированный текст": "Успешное проведение спортивных мероприятий для людей с ОВЗ, повышение их физической активности и социальной интеграции, а также улучшение навыков и уверенности в себе."\n        }\n    }\n]'
]


fields_to_check = ["SocialTaskName", "Description", "TargetAudience", "MechanismOfActions", "DesiredOutcome"]


parsed_data = []
for response in api_responses:
    try:
        data = json.loads(response)
        parsed_data.append(data)
    except json.JSONDecodeError as e:
        print(f"Ошибка разбора JSON: {e}")


total_applications = 0
correct_applications = 0
field_stats = {field: {"correct": 0, "incorrect": 0} for field in fields_to_check}

for application in parsed_data:
    if isinstance(application, list) and len(application) > 0:
        total_applications += 1
        is_correct = True
        if isinstance(application[0], dict) and "ID" in application[0] and any(isinstance(application[0].get(field), dict) for field in fields_to_check):
            app_dict = application[0]
            for field in fields_to_check:
                if field in app_dict:
                    field_data = app_dict[field]
                    if field_data["корректность"]:
                        field_stats[field]["correct"] += 1
                    else:
                        field_stats[field]["incorrect"] += 1
                        is_correct = False
        else:
            for item in application:
                if "корректность" in item:
                    for field in fields_to_check:
                        if field in item:
                            if item["корректность"]:
                                field_stats[field]["correct"] += 1
                            else:
                                field_stats[field]["incorrect"] += 1
                                is_correct = False
        if is_correct:
            correct_applications += 1

incorrect_applications = total_applications - correct_applications


labels = ['Корректные заявки', 'Некорректные заявки']
sizes = [correct_applications, incorrect_applications]
colors = ['#4CAF50', '#FF5252']
explode = (0.1, 0)

plt.figure(figsize=(8, 6))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
plt.title('Процент корректных и некорректных заявок')
plt.show()


fields = list(field_stats.keys())
correct_counts = [field_stats[field]["correct"] for field in fields]
incorrect_counts = [field_stats[field]["incorrect"] for field in fields]

x = np.arange(len(fields))
width = 0.35

fig, ax = plt.subplots(figsize=(12, 6))
rects1 = ax.bar(x - width/2, correct_counts, width, label='Корректные', color='#4CAF50')
rects2 = ax.bar(x + width/2, incorrect_counts, width, label='Некорректные', color='#FF5252')

ax.set_xlabel('Поля заявки')
ax.set_ylabel('Количество заявок')
ax.set_title('Корректность полей заявок')
ax.set_xticks(x)
ax.set_xticklabels(fields, rotation=45, ha='right')
ax.legend()

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{int(height)}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)

fig.tight_layout()
plt.show()