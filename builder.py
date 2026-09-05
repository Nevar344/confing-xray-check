import uuid
import secrets

def generate_short_id() -> str:
    return secrets.token_hex(8)

def get_vless_reality_template(
    tag: str = "vless-inbound-443",
    port: int = 443,
    server_name: str = "example.com",
    private_key: str = "",
    short_id: str = None,
    xver: int = 1
) -> dict:
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

def get_hysteria2_template(
    tag: str = "hy2-inbound-443",
    port: int = 443,
    password: str = None,
    domain: str = "example.com"
) -> dict:
    if not password:
        password = str(uuid.uuid4())

    fullchain_path = f"/etc/letsencrypt/live/{domain}/fullchain.pem"
    privkey_path = f"/etc/letsencrypt/live/{domain}/privkey.pem"

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
                        "certificateFile": fullchain_path,
                        "keyFile": privkey_path
                    }
                ],
                "alpn": [
                    "h3"
                ]
            }
        }
    }