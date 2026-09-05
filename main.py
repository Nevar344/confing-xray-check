import json
from validator import load_config, validate_xray_structure
from builder import get_vless_reality_template, get_grpc_template, get_hysteria2_template


def save_config(file_path: str, config: dict):
    """Сохраняет обновленный конфиг обратно в файл."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    print(f"\n✅ Конфигурация успешно сохранена в '{file_path}'!")


def main():
    print("=" * 50)
    print("       🚀 Xray Config Checker & Builder")
    print("=" * 50)

    file_path = input("\nВведите путь к файлу конфига (по умолчанию config.json): ").strip()
    if not file_path:
        file_path = "config.json"

    config, error = load_config(file_path)
    if error:
        print(f"\n❌ {error}")
        return

    print("\n🔍 Проверка структуры конфига...")
    warnings = validate_xray_structure(config)

    if not warnings:
        print("✅ Серьезных ошибок и предупреждений не обнаружено!")
    else:
        print("\nНайденные проблемы и рекомендации:")
        for w in warnings:
            print(f"  {w}")

    # Меню модификации
    print("\n" + "-" * 40)
    print("Доступные действия:")
    print("1. Добавить VLESS-Reality Inbound")
    print("2. Добавить gRPC Inbound")
    print("3. Добавить Hysteria 2 Inbound")
    print("4. Выйти без изменений")

    choice = input("\nВыберите действие (1-4): ").strip()

    if choice == "1":
        port = int(input("Введите порт для Reality (по умолчанию 443): ") or 443)
        dest = input("Введите SNI/Dest сайт (по умолчанию dl.google.com:443): ") or "dl.google.com:443"
        template = get_vless_reality_template(port=port, dest_host=dest)

        if "inbounds" not in config:
            config["inbounds"] = []
        config["inbounds"].append(template)
        save_config(file_path, config)

    elif choice == "2":
        port = int(input("Введите порт для gRPC (по умолчанию 8443): ") or 8443)
        service = input("Введите Service Name (по умолчанию grpc-vpn): ") or "grpc-vpn"
        template = get_grpc_template(port=port, service_name=service)

        if "inbounds" not in config:
            config["inbounds"] = []
        config["inbounds"].append(template)
        save_config(file_path, config)

    elif choice == "3":
        port = int(input("Введите порт для Hysteria 2 (по умолчанию 8443): ") or 8443)
        pwd = input("Введите пароль доступа (по умолчанию SecretPassword123): ") or "SecretPassword123"
        template = get_hysteria2_template(port=port, password=pwd)

        if "inbounds" not in config:
            config["inbounds"] = []
        config["inbounds"].append(template)
        save_config(file_path, config)

    else:
        print("\nЗавершение работы без изменений.")


if __name__ == "__main__":
    main()