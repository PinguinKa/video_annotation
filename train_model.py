import os
import yaml
from ultralytics import YOLO
from pathlib import Path


def load_data_config(yaml_path: Path) -> dict:
    """
    Загружает конфигурацию датасета из YAML файла.
    Обязательные поля: path, train, val.
    Дополнительно: kpt_shape, flip_idx, names.
    """
    if not yaml_path.is_file():
        raise FileNotFoundError(
            f"Файл {yaml_path} не найден. Проверьте правильность пути."
        )

    with open(yaml_path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    for key in ["path", "train", "val"]:
        if key not in config:
            raise ValueError(f"Ключ '{key}' отсутствует в {yaml_path}.")
    return config


def main():
    # --- Настройки ---
    # Путь к файлу с конфигурацией датасета (data.yaml)
    yaml_file_path = Path("C:/Users/PinguinK/Desktop/ml/data.yaml")

    # Базовая модель: YOLOv8-pose (здесь используется 's' версия для небольшого датасета)
    base_model = "yolov8s-pose.pt"

    # Гиперпараметры обучения
    epochs = 100
    img_size = 640
    batch_size = 8

    # Папка для сохранения результатов и имя запуска
    project_name = "fall_detection_pose_training"
    run_name = "yolov8s_pose_100epochs"

    # --- Загрузка и проверка конфигурации датасета ---
    try:
        data_config = load_data_config(yaml_file_path)
        print("Конфигурация датасета успешно загружена:")
        print(yaml.dump(data_config, sort_keys=False))
    except Exception as e:
        print(f"Ошибка при загрузке data.yaml: {e}")
        return

    # --- Инициализация модели YOLOv8-pose ---
    print(f"\nЗагрузка базовой модели: {base_model}")
    model = YOLO(base_model)

    # --- Обучение ---
    print("\nЗапуск обучения YOLOv8-pose...")
    results = model.train(
        data=str(yaml_file_path.resolve()),  # Абсолютный путь к data.yaml
        epochs=epochs,
        imgsz=img_size,
        batch=batch_size,
        project=project_name,
        name=run_name,
        exist_ok=True,  # Если папка уже существует, перезаписываем
        # Дополнительно можно указать аргументы для аугментации, optimizer и пр.
    )

    print("\nОбучение завершено!")
    print(f"Результаты сохранены в: {results.save_dir}")

    # --- Экспорт модели (опционально) ---
    best_pt_path = Path(results.save_dir) / "weights" / "best.pt"
    if best_pt_path.is_file():
        print(f"\nНайдена лучшая модель: {best_pt_path}")
        print("Экспорт модели в формат ONNX...")
        onnx_path = model.export(format="onnx", opset=12)
        print(f"Модель успешно экспортирована в ONNX: {onnx_path}")
    else:
        print(f"\nОшибка: Файл с лучшими весами не найден: {best_pt_path}")


if __name__ == "__main__":
    main()
