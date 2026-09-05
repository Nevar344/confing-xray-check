import uuid

def get_vless_reality_template(port: int = 443, dest_host: str = "dl.google.com:443") -> dict:
    """Генерирует готовый Inbound для VLESS + Reality."""
    user_uuid = str(uuid.uuid4())
    return {
        "port": port,
        "protocol": "vless",
        "settings": {
            "clients": [
                {
                    "id": user_uuid,
                    "flow": "xtls-rprx-vision"
                }
            ],
            "decryption": "none"
        },
        "streamSettings": {
            "network": "tcp",
            "security": "reality",
            "realitySettings": {
                "show": False,
                "dest": dest_host,
                "xver": 0,
                "serverNames": [dest_host.split(":")[0]],
                "privateKey": "СГЕНЕРИРУЙТЕ_ЧЕРЕЗ_xray_x25519",
                "shortIds": [""]
            }
        }
    }

def get_grpc_template(port: int = 8443, service_name: str = "grpc-vpn") -> dict:
    """Генерирует готовый Inbound с транспортировкой gRPC."""
    return {
        "port": port,
        "protocol": "vless",
        "settings": {
            "clients": [],
            "decryption": "none"
        },
        "streamSettings": {
            "network": "grpc",
            "grpcSettings": {
                "serviceName": service_name
            }
        }
    }
def get_hysteria2_template(port: int = 8443, password: str = "SecretPassword123") -> dict:
    """Генерирует готовый Inbound для Hysteria 2 (Hysteria2 / QUIC)."""
    return {
        "port": port,
        "protocol": "hysteria2",
        "settings": {
            "users": [
                {
                    "password": password
                }
            ],
            "ignoreClientBandwidth": False
        },
        "streamSettings": {
            "network": "hysteria2",
            "security": "tls",
            "tlsSettings": {
                "serverName": "your-domain.com",
                "certificates": [
                    {
                        "certificateFile": "/path/to/cert.crt",
                        "keyFile": "/path/to/private.key"
                    }
                ]
            }
        }
    }