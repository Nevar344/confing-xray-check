import json
import os


def load_config(file_path: str) -> tuple[dict | None, str | None]:
    """Загружает JSON или возвращает флаг NOT_FOUND, если файла нет."""
    if not os.path.exists(file_path):
        return None, "NOT_FOUND"

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config, None
    except json.JSONDecodeError as e:
        return None, f"Синтаксическая ошибка в JSON (строка {e.lineno}, колонка {e.colno}): {e.msg}"
    except Exception as e:
        return None, f"Ошибка при чтении файла: {e}"


def analyze_and_scan_config(config: dict) -> dict:
    """
    Создает подробную карту конфигурации:
    - Показывает существующие инбаунды с разбивкой на TCP/UDP
    - Проверяет наличие BBR, DNS и правил маршрутизации
    - Выдает рекомендации по улучшению
    """
    analysis = {
        "inbounds_map": [],
        "used_tcp_ports": set(),
        "used_udp_ports": set(),
        "used_tags": set(),
        "has_dns": "dns" in config and bool(config["dns"].get("servers")),
        "has_routing": "routing" in config and bool(config["routing"].get("rules")),
        "has_bbr": False,
        "suggestions": []
    }

    inbounds = config.get("inbounds", [])
    for idx, inbound in enumerate(inbounds):
        if not isinstance(inbound, dict):
            continue

        protocol = inbound.get("protocol", "unknown").lower()
        port = inbound.get("port", 0)
        tag = inbound.get("tag", f"inbound-{idx}")
        network = inbound.get("streamSettings", {}).get("network", "tcp").lower()

        if network == "udp" or protocol in ["hysteria2", "hysteria"]:
            analysis["used_udp_ports"].add(port)
        else:
            analysis["used_tcp_ports"].add(port)

        analysis["used_tags"].add(tag)

        # Проверка BBR
        sockopt = inbound.get("streamSettings", {}).get("sockopt", {})
        if sockopt.get("tcpCongestion") == "bbr":
            analysis["has_bbr"] = True

        analysis["inbounds_map"].append({
            "index": idx,
            "protocol": protocol,
            "port": port,
            "network": network if protocol not in ["hysteria2", "hysteria"] else "udp",
            "tag": tag,
            "raw": inbound
        })

    # Формирование рекомендаций
    if not analysis["has_dns"]:
        analysis["suggestions"].append("💡 Отсутствует блок DNS. Рекомендуется настроить быстрый DNS (1.1.1.1).")

    if not analysis["has_bbr"] and any(i["protocol"] == "vless" for i in analysis["inbounds_map"]):
        analysis["suggestions"].append("💡 В VLESS инбаунде не включена оптимизация BBR (tcpCongestion).")

    if not analysis["has_routing"]:
        analysis["suggestions"].append("💡 Нет блока 'routing'. Рекомендуется добавить правила маршрутизации.")

    return analysis