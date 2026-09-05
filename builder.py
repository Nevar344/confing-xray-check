import uuid

def get_vless_reality_template(tag: str = "ultinfin-vless-443", port: int = 443, server_name: str = "ultinvpn.biz") -> dict:
    """Генерирует готовый инбаунд VLESS Reality с поддержкой BBR."""
    return {
        "tag": tag,
        "port": port,
        "protocol": "vless",
        "settings": {
            "clients": [],
            "decryption": "none"
        },
        "streamSettings": {
            "network": "tcp",
            "security": "reality",
            "realitySettings": {
                "show": False,
                "dest": f"{server_name}:443",
                "xver": 0,
                "serverNames": [
                    server_name
                ],
                "privateKey": "",  # Заполняется панелью или через скрипт
                "shortIds": [
                    ""
                ]
            },
            "sockopt": {
                "tcpCongestion": "bbr"
            }
        }
    }

def get_hysteria2_template(tag: str = "hy2-inbound-443", port: int = 443, password: str = None) -> dict:
    """Генерирует инбаунд Hysteria 2 для 443/UDP с сертификатами из /dev/shm."""
    if not password:
        password = str(uuid.uuid4())

    return {
        "tag": tag,
        "port": port,
        "protocol": "hysteria2",
        "settings": {
            "users": [
                {
                    "password": password
                }
            ],
            "ignoreClientBandwidth": True
        },
        "streamSettings": {
            "network": "udp",
            "security": "tls",
            "tlsSettings": {
                "certificates": [
                    {
                        "certificateFile": "/dev/shm/hy2_certs/fullchain.pem",
                        "keyFile": "/dev/shm/hy2_certs/privkey.pem"
                    }
                ],
                "alpn": [
                    "h3"
                ]
            }
        }
    }