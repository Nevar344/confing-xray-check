import json
import os


def validate_config(config_input):
    """
    Принимает либо путь к файлу (str), либо словарь (dict).
    """
    if isinstance(config_input, str):
        if not os.path.exists(config_input):
            return False, f"Файл {config_input} не найден."
        try:
            with open(config_input, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            return False, f"Ошибка чтения JSON: {str(e)}"
    elif isinstance(config_input, dict):
        data = config_input
    else:
        return False, "Неверный тип данных для конфигурации."

    # Проверка обязательных секций
    if "inbounds" not in data or not isinstance(data["inbounds"], list):
        return False, "Секция 'inbounds' отсутствует или не является списком."

    if "outbounds" not in data or not isinstance(data["outbounds"], list):
        return False, "Секция 'outbounds' отсутствует или не является списком."

    tags = [inb.get("tag") for inb in data["inbounds"] if "tag" in inb]

    return True, f"Конфигурация валидна. Найдено inbounds: {len(tags)}"