import json
import sys
from validator import load_config
from builder import get_vless_reality_template, get_hysteria2_template, generate_short_id
from tuners import set_dns_servers
from env_checker import run_all_checks
from cert_manager import issue_letsencrypt_cert, update_docker_compose_certs, open_port_firewall


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
        ("SSL Сертификаты (Let's Encrypt)", checks["certs"]),
        ("Работа VLESS Reality (443/TCP)", checks["vless_port_443_tcp"]),
        ("Работа Hysteria 2 (443/UDP)", checks["hy2_port_443_udp"]),
    ]

    for title, (status, msg) in items:
        icon = "✅" if status else "❌"
        print(f"  {icon} {title}: {msg}")
        if not status and title in ["Запуск от root", "Установка Docker", "Доступность Docker daemon"]:
            all_critical_passed = False

    print("=" * 60)
    return all_critical_passed


def handle_auto_remediation(checks: dict) -> dict:
    if not checks["certs"][0]:
        print("\n⚠️ SSL-сертификаты Let's Encrypt не найдены.")
        answer = input("❓ Выпустить сертификаты через Let's Encrypt прямо сейчас? (y/n): ").strip().lower()
        if answer == 'y':
            domain = input("Введите ваш домен (например, sub.example.com): ").strip()
            if domain:
                ok, fullchain, privkey = issue_letsencrypt_cert(domain)
                if ok:
                    update_docker_compose_certs(domain)
                    checks["certs"] = (True, f"Найден домен: {domain}")
                    checks["cert_domain"] = domain

    if not checks["vless_port_443_tcp"][0] or not checks["hy2_port_443_udp"][0]:
        print("\n⚠️ Порт 443 (TCP/UDP) закрыт или заблокирован файрволом.")
        answer = input("❓ Открыть порты 443/TCP и 443/UDP в файрволе (UFW/iptables)? (y/n): ").strip().lower()
        if answer == 'y':
            open_port_firewall(443, "both")

    return checks


def prompt_vless_params(default_domain: str = "", default_port: int = 443, default_tag: str = "vless-inbound-443"):
    port = int(input(f"Введите порт (по умолчанию {default_port}): ") or default_port)
    tag = input(f"Тег инбаунда (по умолчанию '{default_tag}'): ") or default_tag

    sni_default = default_domain if default_domain else "example.com"
    sni = input(f"Server Name / SNI (по умолчанию '{sni_default}'): ") or sni_default

    print("\n🔑 Ввод Private Key (Reality):")
    private_key = input("Private Key из панели Remnawave: ").strip()
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
    elif sid_choice == "3":
        short_id = input("Введите Short ID: ").strip() or "8d6da97c874a82e1"
    else:
        short_id = "8d6da97c874a82e1"

    print("\n🌐 Настройка PROXY Protocol (xver):")
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
        print("\n❌ Критические проверки не пройдены. Исправьте ошибки выше.")
        sys.exit(1)

    checks = handle_auto_remediation(checks)

    file_path = "/etc/remnanode/config.json"
    config, error = load_config(file_path)
    if error:
        print(f"\n❌ Не удалось загрузить конфиг '{file_path}': {error}")
        return

    while True:
        checks = run_all_checks()

        print("\n" + "-" * 45)
        print("Главное меню:")
        print("1. Добавить VLESS-Reality (443/TCP)")

        hy2_status = "✅ Готово к добавлению" if checks["certs"][0] else "⚠️ Требуется выпуск SSL сертификата"
        print(f"2. Добавить Hysteria 2 (443/UDP) [{hy2_status}]")

        print("3. Настроить DNS")
        print("4. Авто-выпуск SSL / Открытие портов")
        print("5. Перепроверить системное окружение")
        print("6. Сохранить и выйти")

        choice = input("\nВыберите действие (1-6): ").strip()

        if choice == "1":
            template, port = prompt_vless_params(default_domain=checks.get("cert_domain", ""))
            config.setdefault("inbounds", []).append(template)
            print("✅ VLESS Reality успешно добавлен!")

        elif choice == "2":
            if not checks["certs"][0]:
                ans = input("Выпустить сертификаты сейчас через Let's Encrypt? (y/n): ").strip().lower()
                if ans == 'y':
                    domain = input("Введите ваш домен: ").strip()
                    ok, fullchain, privkey = issue_letsencrypt_cert(domain)
                    if ok:
                        update_docker_compose_certs(domain)
                        checks["cert_domain"] = domain
                    else:
                        continue
                else:
                    continue

            domain = checks.get("cert_domain") or input("Введите ваш домен для Hysteria 2: ").strip()
            port = int(input("Введите UDP порт (по умолчанию 443): ") or 443)
            tag = input("Тег инбаунда (по умолчанию hy2-inbound-443): ") or "hy2-inbound-443"
            pwd = input("Пароль (пусто для автогенерации): ").strip()

            template = get_hysteria2_template(tag=tag, port=port, password=pwd, domain=domain)
            config.setdefault("inbounds", []).append(template)
            print("✅ Hysteria 2 успешно добавлена!")

        elif choice == "3":
            dns_ip = input("Введите IP DNS (по умолчанию 1.1.1.1): ") or "1.1.1.1"
            config = set_dns_servers(config, dns_address=dns_ip)
            print(f"✅ DNS сервер {dns_ip} применен!")

        elif choice == "4":
            handle_auto_remediation(checks)

        elif choice == "5":
            print_env_status(run_all_checks())

        elif choice == "6":
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print(f"✅ Конфигурация сохранена в '{file_path}'!")
            break


if __name__ == "__main__":
    main()