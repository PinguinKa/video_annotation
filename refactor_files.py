import os


def process_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    processed_lines = []
    for line in lines:
        values = line.strip().split()
        if len(values) > 1:  # Проверяем, что строка содержит больше одного значения
            # Идем с конца строки
            for i in range(len(values) - 1, 0, -1):
                if values[i] == "0":
                    # Зануляем -1 и -2 значения
                    if i - 1 > 0:
                        values[i - 1] = "0.000"
                    if i - 2 > 0:
                        values[i - 2] = "0.000"
            processed_lines.append(" ".join(values) + "\n")

    with open(file_path, "w") as file:
        file.writelines(processed_lines)


def process_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                process_file(file_path)


folder_path = "chute07/data/labels/train"
process_folder(folder_path)
