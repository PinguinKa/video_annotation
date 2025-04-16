import os

# Путь к папке с файлами разметки
folder_path = "chute07/data/labels/train"


def swap_classes(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    updated_lines = []
    for line in lines:
        parts = line.strip().split()
        if parts:

            if parts[0] == "0":
                parts[0] = "1"
            elif parts[0] == "1":
                parts[0] = "0"
            updated_lines.append(" ".join(parts))

    with open(file_path, "w") as file:
        file.write("\n".join(updated_lines))


for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)
        swap_classes(file_path)
