import json
import matplotlib.pyplot as plt
import numpy as np

def generate_graphs(api_responses):
    # Список полей для проверки
    fields_to_check = ["SocialTaskName", "Description", "TargetAudience", "MechanismOfActions", "DesiredOutcome"]


    parsed_data = []
    for response in api_responses:
        try:
            data = json.loads(response)
            if isinstance(data, dict):
                parsed_data.append(data)
            else:
                print(f"Пропущен некорректный JSON: ожидался словарь, получен {type(data)}")
        except json.JSONDecodeError as e:
            print(f"Ошибка разбора JSON: {e}")

    if not parsed_data:
        print("Нет данных для построения графиков: список заявок пуст.")
        return


    total_applications = 0
    correct_applications = 0
    field_stats = {field: {"correct": 0, "incorrect": 0} for field in fields_to_check}


    for application in parsed_data:
        total_applications += 1
        is_correct = True
        for field in fields_to_check:
            if field in application and isinstance(application[field], dict) and "корректность" in application[field]:
                if application[field]["корректность"]:
                    field_stats[field]["correct"] += 1
                else:
                    field_stats[field]["incorrect"] += 1
                    is_correct = False
            else:

                is_correct = False
                field_stats[field]["incorrect"] += 1
        if is_correct:
            correct_applications += 1

    incorrect_applications = total_applications - correct_applications


    labels = ['Корректные заявки', 'Некорректные заявки']
    sizes = [correct_applications, incorrect_applications]
    colors = ['#4CAF50', '#FF5252']
    explode = (0.1, 0)

    if sum(sizes) > 0:
        plt.figure(figsize=(8, 6))
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        plt.title('Процент корректных и некорректных заявок')
        plt.show()
    else:
        print("Невозможно построить круговую диаграмму: нет корректных или некорректных заявок (sizes = [0, 0]).")

    fields = list(field_stats.keys())
    correct_counts = [field_stats[field]["correct"] for field in fields]
    incorrect_counts = [field_stats[field]["incorrect"] for field in fields]

    if sum(correct_counts) + sum(incorrect_counts) > 0:
        x = np.arange(len(fields))
        width = 0.35

        fig, ax = plt.subplots(figsize=(12, 6))
        rects1 = ax.bar(x - width / 2, correct_counts, width, label='Корректные', color='#4CAF50')
        rects2 = ax.bar(x + width / 2, incorrect_counts, width, label='Некорректные', color='#FF5252')

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
    else:
        print("Невозможно построить столбчатую диаграмму: все поля имеют нулевые значения.")


