import json
import os
from validator import load_config, analyze_and_scan_config
from builder import get_vless_reality_template, get_hysteria2_template
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
            print(
                f"    [{item['index'] + 1}] Протокол: {item['protocol'].upper()} | Порт: {item['port']}/{item['network'].upper()} | Тег: {item['tag']}")

    print(f"  • Наличие DNS блока: {'✅ Настроен' if analysis['has_dns'] else '❌ Отсутствует'}")
    print(f"  • Оптимизация BBR: {'✅ Включена' if analysis['has_bbr'] else '❌ Отсутствует'}")

    if analysis["suggestions"]:
        print("\n💡 РЕКОМЕНДАЦИИ ПО УЛУЧШЕНИЮ:")
        for sug in analysis["suggestions"]:
            print(f"  {sug}")


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
    print("2. Удалить этот инбаунд")
    print("3. Отмена")

    action = input("Выберите действие (1-3): ").strip()

    if action == "1":
        port = int(input(f"Новый порт (текущий {selected['port']}): ") or selected['port'])
        tag = input(f"Новый тег (текущий '{selected['tag']}'): ") or selected['tag']

        if selected["protocol"] == "vless":
            sni = input("Server Name / SNI (по умолчанию ultinvpn.biz): ") or "ultinvpn.biz"
            new_inbound = get_vless_reality_template(tag=tag, port=port, server_name=sni)
        elif selected["protocol"] in ["hysteria2", "hysteria"]:
            pwd = input("Пароль для Hysteria2 (оставьте пустым для сохранения старого): ").strip()
            new_inbound = get_hysteria2_template(tag=tag, port=port, password=pwd)
        else:
            print("⚠️ Пересоздание для этого типа протокола не поддерживается.")
            return config

        config["inbounds"][selected["index"]] = new_inbound
        print(f"✅ Инбаунд '{tag}' успешно обновлен!")

    elif action == "2":
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
        print("3. Управлять существующими Inbound'ами (Пересоздать / Удалить)")
        print("4. Настроить быстрый DNS (1.1.1.1)")
        print("5. Добавить SOCKS5 прокси для сервисов (ozon, wb, vtb)")
        print("6. Сохранить конфигурацию и выйти")

        choice = input("\nВыберите действие (1-6): ").strip()

        if choice == "1":
            port = int(input("Введите порт (по умолчанию 443): ") or 443)
            if port in analysis["used_tcp_ports"]:
                print(f"❌ Ошибка: TCP порт {port} уже занят!")
                continue

            tag = input("Тег инбаунда (по умолчанию ultinfin-vless-443): ") or "ultinfin-vless-443"
            sni = input("Server Name / SNI (по умолчанию ultinvpn.biz): ") or "ultinvpn.biz"
            template = get_vless_reality_template(tag=tag, port=port, server_name=sni)

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