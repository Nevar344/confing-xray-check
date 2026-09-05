def format_domains(domain_inputs: list[str]) -> list[str]:
    """
    Автоматически добавляет 'keyword:' для названий сервисов (ozon, wb, vtb),
    но сохраняет префиксы или точки, если пользователь ввел их вручную.
    """
    formatted = []
    for d in domain_inputs:
        d = d.strip()
        if not d:
            continue
        if ":" in d or "." in d:
            formatted.append(d)
        else:
            formatted.append(f"keyword:{d}")
    return formatted

def set_dns_servers(config: dict, dns_address: str = "1.1.1.1", strategy: str = "UseIPv4") -> dict:
    """Настраивает блок DNS."""
    config["dns"] = {
        "servers": [
            {
                "address": dns_address,
                "skipFallback": True
            }
        ],
        "queryStrategy": strategy
    }
    return config

def set_ip_strategy(config: dict, use_ipv6: bool = False) -> dict:
    """Настраивает стратегию IP (IPv4 / IPv6)."""
    strategy = "UseIP" if use_ipv6 else "UseIPv4"

    if "dns" in config:
        config["dns"]["queryStrategy"] = strategy

    if "outbounds" in config:
        for outbound in config["outbounds"]:
            if outbound.get("tag") == "DIRECT" or outbound.get("protocol") == "freedom":
                outbound.setdefault("settings", {})["domainStrategy"] = strategy

    if "routing" in config:
        config["routing"]["domainStrategy"] = "IPOnDemand" if use_ipv6 else "IPIfNonMatch"

    return config

def add_routing_rule_proxy_domains(config: dict, domains: list[str], proxy_tag: str = "MOSCOW_PROXY") -> dict:
    """Добавляет правило маршрутизации для указанных сервисов."""
    if "routing" not in config:
        config["routing"] = {"rules": [], "domainStrategy": "IPIfNonMatch"}
    if "rules" not in config["routing"]:
        config["routing"]["rules"] = []

    formatted_list = format_domains(domains)

    rule = {
        "type": "field",
        "domain": formatted_list,
        "outboundTag": proxy_tag
    }
    config["routing"]["rules"].append(rule)
    return config

def add_socks_outbound(config: dict, tag: str, address: str, port: int) -> dict:
    """Добавляет или обновляет SOCKS5 аутбаунд."""
    if "outbounds" not in config:
        config["outbounds"] = []

    for out in config["outbounds"]:
        if out.get("tag") == tag:
            out["settings"] = {"servers": [{"address": address, "port": port}]}
            return config

    socks_outbound = {
        "tag": tag,
        "protocol": "socks",
        "settings": {
            "servers": [
                {
                    "address": address,
                    "port": port
                }
            ]
        }
    }
    config["outbounds"].append(socks_outbound)
    return config