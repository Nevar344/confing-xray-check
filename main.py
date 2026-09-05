import json
import os
import secrets
from validator import load_config, analyze_and_scan_config
from builder import get_vless_reality_template, get_hysteria2_template, generate_short_id
from tuners import set_dns_servers, set_ip_strategy, add_routing_rule_proxy_domains, add_socks_outbound


def save_config(file_path: str, config: dict):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Конфигурация успешно сохранена в '{file_path}'!")


def create_empty_base_config() -> dict:
    """Создает чистый базовый каркас Xray конфига."""
    return {
        "log": {"loglevel": "warning"},
        "dns": {},
        "inbounds": [],
        "outbounds": [
            {"protocol": "freedom", "tag": "direct"},
            {"protocol": "blackhole", "tag": "blocked"}
        ],
        "routing": {
            "domainStrategy": "IPIfNonMatch",
            "rules": []
        }
    }


def print_scan_report(analysis: dict):
    print("\n📊 Карта текущей конфигурации:")
    if not analysis["inbounds_map"]:
        print("  • Инбаунды: (отсутствуют)")
    else:
        print("  • Найденные инбаунды:")
        for item in analysis["inbounds_map"]:
            # Дополнительный вывод версии PROXY protocol (xver) для VLESS
            raw_inbound = item["raw"]
            xver_info = ""
            if item["protocol"] == "vless":
                xver_val = raw_inbound.get("streamSettings", {}).get("realitySettings", {}).get("xver", 0)
                xver_info = f" | PROXY v{xver_val}"

            print(
                f"    [{item['index'] + 1}] Протокол: {item['protocol'].upper()} | Порт: {item['port']}/{item['network'].upper()}{xver_info} | Тег: {item['tag']}")

    print(f"  • Наличие DNS блока: {'✅ Настроен' if analysis['has_dns'] else '❌ Отсутствует'}")
    print(f"  • Оптимизация BBR: {'✅ Включена' if analysis['has_bbr'] else '❌ Отсутствует'}")

    if analysis["suggestions"]:
        print("\n💡 РЕКОМЕНДАЦИИ ПО УЛУЧШЕНИЮ:")
        for sug in analysis["suggestions"]:
            print(f"  {sug}")


def prompt_vless_params(default_port: int = 443, default_tag: str = "ultinfin-vless-443"):
    """Интерактивный сбор параметров для VLESS Reality."""
    port = int(input(f"Введите порт (по умолчанию {default_port}): ") or default_port)
    tag = input(f"Тег инбаунда (по умолчанию '{default_tag}'): ") or default_tag
    sni = input("Server Name / SNI (по умолчанию ultinvpn.biz): ") or "ultinvpn.biz"

    # Запрос Private Key с подсказкой про Remnawave
    print("\n🔑 Ввод Private Key (Reality):")
    print("💡 Подсказка: Скопируйте Private Key из вашей панели Remnawave (раздел подключения ноды).")
    private_key = input("Private Key: ").strip()
    while not private_key:
        print("⚠️ Private Key обязателен для работы VLESS Reality!")
        private_key = input("Вставьте Private Key из панели Remnawave: ").strip()

    # Запрос Short ID
    print("\n🆔 Настройка Short ID:")
    print("1. Использовать стандартный (8d6da97c874a82e1)")
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

    # Запрос xver (PROXY protocol)
    print("\n🌐 Настройка PROXY Protocol (xver):")
    print("0 - Выключен")
    print("1 - PROXY protocol v1 (Рекомендуется для работы ноды под прокси/vpn/Remnawave)")
    print("2 - PROXY protocol v2")
    try:
        xver_input = input("Выберите xver (0-2, по умолчанию 1): ").strip()
        xver = int(xver_input) if xver_input in ["0", "1", "2"] else 1
    except ValueError:
        xver = 1

    return get_vless_reality_template(
        tag=tag,
        port=port,
        server_name=sni,
        private_key=private_key,
        short_id=short_id,
        xver=xver
    ), port


def manage_existing_inbounds(config: dict, analysis: dict):
    """Управление и редактирование существующих инбаундов."""
    if not analysis["inbounds_map"]:
        print("\n⚠️ В конфигурации нет инбаундов для редактирования.")
        return config

    print("\n--- 🛠️ Редактирование существующих инбаундов ---")
    for item in analysis["inbounds_map"]:
        print(
            f"[{item['index'] + 1}] {item['protocol'].upper()} (Порт: {item['port']}/{item['network'].upper()}, Тег: {item['tag']})")

    try:
        choice_idx = int(input("\nВведите номер инбаунда для изменения (0 для отмены): ")) - 1
        if choice_idx < 0 or choice_idx >= len(analysis["inbounds_map"]):
            return config
    except ValueError:
        return config

    selected = analysis["inbounds_map"][choice_idx]
    print(f"\nВыбран: {selected['protocol'].upper()} [Тег: {selected['tag']}]")
    print("1. Пересоздать с новыми настройками")
    print("2. Переключить PROXY protocol (xver)")
    print("3. Удалить этот инбаунд")
    print("4. Отмена")

    action = input("Выберите действие (1-4): ").strip()

    if action == "1":
        if selected["protocol"] == "vless":
            new_inbound, _ = prompt_vless_params(default_port=selected['port'], default_tag=selected['tag'])
        elif selected["protocol"] in ["hysteria2", "hysteria"]:
            port = int(input(f"Новый порт (текущий {selected['port']}): ") or selected['port'])
            tag = input(f"Новый тег (текущий '{selected['tag']}'): ") or selected['tag']
            pwd = input("Пароль для Hysteria2 (пусто для сохранения): ").strip()
            new_inbound = get_hysteria2_template(tag=tag, port=port, password=pwd)
        else:
            print("⚠️ Пересоздание для этого типа протокола не поддерживается.")
            return config

        config["inbounds"][selected["index"]] = new_inbound
        print(f"✅ Инбаунд '{selected['tag']}' успешно пересоздан!")

    elif action == "2":
        if selected["protocol"] != "vless":
            print("⚠️ Настройка xver поддерживается только для VLESS!")
            return config

        reality_settings = config["inbounds"][selected["index"]].setdefault("streamSettings", {}).setdefault(
            "realitySettings", {})
        current_xver = reality_settings.get("xver", 0)
        print(f"\nТекущее значение xver: {current_xver}")
        new_xver = input("Введите новое значение xver (0, 1 или 2): ").strip()
        if new_xver in ["0", "1", "2"]:
            reality_settings["xver"] = int(new_xver)
            print(f"✅ Значение xver успешно изменено на {new_xver}!")

    elif action == "3":
        config["inbounds"].pop(selected["index"])
        print(f"🗑️ Инбаунд '{selected['tag']}' удален.")

    return config


def main():
    print("=" * 55)
    print("      🚀 UltinVPN Smart Config Manager & Tuner")
    print("=" * 55)

    file_path = input("\nВведите путь к файлу конфига (по умолчанию /etc/remnanode/config.json): ").strip()
    if not file_path:
        file_path = "/etc/remnanode/config.json"

    config, error = load_config(file_path)

    if error == "NOT_FOUND":
        print(f"\n⚠️ Файл '{file_path}' не найден!")
        create_new = input("Создать новую конфигурацию с нуля? (y/n): ").lower()
        if create_new == 'y':
            config = create_empty_base_config()
            print("\n✨ Создан базовый каркас нового конфига!")
        else:
            print("Завершение работы.")
            return
    elif error:
        print(f"\n❌ {error}")
        return

    while True:
        analysis = analyze_and_scan_config(config)
        print_scan_report(analysis)

        print("\n" + "-" * 45)
        print("Главное меню:")
        print("1. Добавить VLESS-Reality (443/TCP)")
        print("2. Добавить Hysteria 2 (443/UDP)")
        print("3. Управлять существующими Inbound'ами (Пересоздать / Изменить xver / Удалить)")
        print("4. Настроить быстрый DNS (1.1.1.1)")
        print("5. Добавить SOCKS5 прокси для сервисов (ozon, wb, vtb)")
        print("6. Сохранить конфигурацию и выйти")

        choice = input("\nВыберите действие (1-6): ").strip()

        if choice == "1":
            template, port = prompt_vless_params()
            if port in analysis["used_tcp_ports"]:
                print(f"⚠️ Внимание: TCP порт {port} уже фигурирует в конфиге.")
                override = input("Всё равно добавить этот инбаунд? (y/n): ").lower()
                if override != 'y':
                    continue

            config.setdefault("inbounds", []).append(template)
            print("✅ VLESS Reality успешно добавлен!")

        elif choice == "2":
            port = int(input("Введите порт (по умолчанию 443): ") or 443)
            if port in analysis["used_udp_ports"]:
                print(f"❌ Ошибка: UDP порт {port} уже занят Hysteria 2!")
                continue

            tag = input("Тег инбаунда (по умолчанию hy2-inbound-443): ") or "hy2-inbound-443"
            pwd = input("Пароль (пусто для генерации): ").strip()
            template = get_hysteria2_template(tag=tag, port=port, password=pwd)

            config.setdefault("inbounds", []).append(template)
            print("✅ Hysteria 2 успешно добавлена!")

        elif choice == "3":
            config = manage_existing_inbounds(config, analysis)

        elif choice == "4":
            dns_ip = input("Введите IP DNS (по умолчанию 1.1.1.1): ") or "1.1.1.1"
            config = set_dns_servers(config, dns_address=dns_ip)
            print(f"✅ DNS сервер {dns_ip} применен!")

        elif choice == "5":
            tag = input("Тег прокси outbound (по умолчанию MOSCOW_PROXY): ") or "MOSCOW_PROXY"
            addr = input("IP адрес SOCKS5 прокси: ").strip()
            port = int(input("Порт SOCKS5 прокси: ").strip())

            print("\nВведите сервисы через запятую (например: ozon, wb, vtb):")
            domains_raw = input("Сервисы: ")
            domains = [d.strip() for d in domains_raw.split(",") if d.strip()]

            config = add_socks_outbound(config, tag=tag, address=addr, port=port)
            config = add_routing_rule_proxy_domains(config, domains=domains, proxy_tag=tag)
            print("✅ SOCKS5 прокси и правила успешно добавлены!")

        elif choice == "6":
            save_config(file_path, config)
            break


if __name__ == "__main__":
    main()