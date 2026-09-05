import json
import sys
from validator import load_config, analyze_and_scan_config
from builder import get_vless_reality_template, get_hysteria2_template, generate_short_id
from tuners import set_dns_servers, add_routing_rule_proxy_domains, add_socks_outbound
from env_checker import run_all_checks


def print_env_status(checks: dict) -> bool:
    print("=" * 60)
    print("         🔍 Проверка системного окружения")
    print("=" * 60)

    all_critical_passed = True

    items = [
        ("Запуск от root", checks["root"]),
        ("Установка Docker", checks["docker_installed"]),
        ("Доступность Docker daemon", checks["docker_daemon"]),
        ("Наличие контейнера 'remnanode'", checks["container_exists"]),
        ("Запуск контейнера 'remnanode'", checks["container_running"]),
        ("Доступность /dev/shm", checks["dev_shm"]),
        ("Сертификаты SSL (/dev/shm/hy2_certs)", checks["certs"]),
        ("Работа VLESS Reality (443/TCP)", checks["vless_port_443_tcp"]),
    ]

    for title, (status, msg) in items:
        icon = "✅" if status else "❌"
        print(f"  {icon} {title}: {msg}")
        if not status and title in ["Запуск от root", "Установка Docker", "Доступность Docker daemon"]:
            all_critical_passed = False

    print("=" * 60)
    return all_critical_passed


def prompt_vless_params(default_port: int = 443, default_tag: str = "vless-inbound-443"):
    port = int(input(f"Введите порт (по умолчанию {default_port}): ") or default_port)
    tag = input(f"Тег инбаунда (по умолчанию '{default_tag}'): ") or default_tag
    sni = input("Server Name / SNI (по умолчанию example.com): ") or "example.com"

    print("\n🔑 Ввод Private Key (Reality):")
    print("💡 Скопируйте Private Key из вашей панели управления нодой.")
    private_key = input("Private Key: ").strip()
    while not private_key:
        print("⚠️ Private Key обязателен!")
        private_key = input("Вставьте Private Key из панели: ").strip()

    print("\n🆔 Настройка Short ID:")
    print("1. Стандартный (8d6da97c874a82e1)")
    print("2. Сгенерировать новый случайный Short ID")
    print("3. Ввести вручную")
    sid_choice = input("Выберите вариант (1-3, по умолчанию 1): ").strip()

    if sid_choice == "2":
        short_id = generate_short_id()
        print(f"🎲 Сгенерирован Short ID: {short_id}")
    elif sid_choice == "3":
        short_id = input("Введите Short ID: ").strip() or "8d6da97c874a82e1"
    else:
        short_id = "8d6da97c874a82e1"

    print("\n🌐 Настройка PROXY Protocol (xver):")
    print("0 - Выключен")
    print("1 - PROXY protocol v1 (Рекомендуется по умолчанию)")
    print("2 - PROXY protocol v2")
    try:
        xver_input = input("Выберите xver (0-2, по умолчанию 1): ").strip()
        xver = int(xver_input) if xver_input in ["0", "1", "2"] else 1
    except ValueError:
        xver = 1

    return get_vless_reality_template(
        tag=tag, port=port, server_name=sni,
        private_key=private_key, short_id=short_id, xver=xver
    ), port


def main():
    checks = run_all_checks()
    critical_ok = print_env_status(checks)

    if not critical_ok:
        print("\n❌ Критические проверки не пройдены. Исправьте ошибки выше и запустите скрипт снова.")
        sys.exit(1)

    file_path = "/etc/remnanode/config.json"
    config, error = load_config(file_path)
    if error:
        print(f"\n❌ Не удалось загрузить конфиг '{file_path}': {error}")
        return

    while True:
        # Обновляем статус проверок перед каждым выбором
        checks = run_all_checks()
        analysis = analyze_and_scan_config(config)

        print("\n" + "-" * 45)
        print("Главное меню:")
        print("1. Добавить VLESS-Reality (443/TCP)")

        # Индикация блокировки Hysteria 2
        hy2_status = "✅ Готово к добавлению" if checks["certs"][0] else "⛔ Заблокировано (нет SSL сертификатов)"
        print(f"2. Добавить Hysteria 2 (443/UDP) [{hy2_status}]")

        print("3. Настроить DNS")
        print("4. Перепроверить системное окружение")
        print("5. Сохранить и выйти")

        choice = input("\nВыберите действие (1-5): ").strip()

        if choice == "1":
            template, port = prompt_vless_params()
            config.setdefault("inbounds", []).append(template)
            print("✅ VLESS Reality успешно добавлен!")

        elif choice == "2":
            if not checks["certs"][0]:
                print("\n❌ НЕВОЗМОЖНО ВКЛЮЧИТЬ HYSTERIA 2!")
                print(f"Причина: {checks['certs'][1]}")
                print("Пожалуйста, разместите fullchain.pem и privkey.pem в /dev/shm/hy2_certs/ перед продолжением.")
                continue

            port = int(input("Введите UDP порт (по умолчанию 443): ") or 443)
            tag = input("Тег инбаунда (по умолчанию hy2-inbound-443): ") or "hy2-inbound-443"
            pwd = input("Пароль (пусто для автогенерации): ").strip()
            template = get_hysteria2_template(tag=tag, port=port, password=pwd)

            config.setdefault("inbounds", []).append(template)
            print("✅ Hysteria 2 успешно добавлена!")

        elif choice == "3":
            dns_ip = input("Введите IP DNS (по умолчанию 1.1.1.1): ") or "1.1.1.1"
            config = set_dns_servers(config, dns_address=dns_ip)
            print(f"✅ DNS сервер {dns_ip} применен!")

        elif choice == "4":
            print_env_status(run_all_checks())

        elif choice == "5":
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print(f"✅ Конфигурация сохранена в '{file_path}'!")
            break


if __name__ == "__main__":
    main()