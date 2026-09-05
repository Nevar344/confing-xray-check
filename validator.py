import json
import os


def load_config(file_path: str) -> tuple[dict | None, str | None]:
    """Загружает и проверяет синтаксис JSON."""
    if not os.path.exists(file_path):
        return None, f"Ошибка: Файл '{file_path}' не найден."

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config, None
    except json.JSONDecodeError as e:
        return None, f"Синтаксическая ошибка в JSON (строка {e.lineno}, колонка {e.colno}): {e.msg}"
    except Exception as e:
        return None, f"Неизвестная ошибка при чтении: {e}"


def validate_xray_structure(config: dict) -> list[str]:
    """Проверяет основные секции и структуру Xray."""
    warnings = []

    # 1. Проверка наличия обязательных секций
    if "inbounds" not in config:
        warnings.append("⚠️ Отсутствует секция 'inbounds' (входящие подключения).")
    elif not isinstance(config["inbounds"], list):
        warnings.append("❌ Секция 'inbounds' должна быть списком (массивом []).")

    if "outbounds" not in config:
        warnings.append("⚠️ Отсутствует секция 'outbounds' (исходящие подключения).")
    elif not isinstance(config["outbounds"], list):
        warnings.append("❌ Секция 'outbounds' должна быть списком (массивом []).")

    # 2. Проверка инбаундов на базовые поля
    inbounds = config.get("inbounds", [])
    for idx, inbound in enumerate(inbounds):
        if not isinstance(inbound, dict):
            continue
        protocol = inbound.get("protocol", "не указан")
        port = inbound.get("port")

        if not port:
            warnings.append(f"⚠️ Inbound #{idx + 1} ({protocol}): Не указан порт (port).")

        # Проверка VLESS без TLS/Reality
        if protocol == "vless":
            stream_settings = inbound.get("streamSettings", {})
            security = stream_settings.get("security", "none")
            if security == "none":
                warnings.append(
                    f"⚠️ Inbound #{idx + 1} (VLESS): Безопасность отключена (security: 'none'). Рекомендуется использовать 'reality' или 'tls'.")

    return warnings