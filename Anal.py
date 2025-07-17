import json
import matplotlib.pyplot as plt
import numpy as np

def generate_graphs(api_responses):

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