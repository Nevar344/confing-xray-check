import uuid
import secrets


def generate_short_id() -> str:
    """Генерирует случайный 8-байтовый (16 hex-символов) Short ID."""
    return secrets.token_hex(8)


def get_vless_reality_template(
        tag: str = "ultinfin-vless-443",
        port: int = 443,
        server_name: str = "ultinvpn.biz",
        private_key: str = "",
        short_id: str = None,
        xver: int = 1
) -> dict:
    """Генерирует готовый инбаунд VLESS Reality с поддержкой BBR и PROXY protocol (xver)."""

    if not short_id:
        short_id = "8d6da97c874a82e1"

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
                "xver": xver,
                "serverNames": [
                    server_name
                ],
                "privateKey": private_key,
                "shortIds": [
                    short_id
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