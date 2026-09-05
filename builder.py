import json
import os

def generate_config(
    vless_port=443,
    hy2_port=443,
    server_name="ultinfin.ultinvpn.biz",
    private_key="",
    short_ids=None,
    clients=None
):
    if short_ids is None:
        short_ids = [""]
    if clients is None:
        clients = []

    config = {
        "log": {
            "loglevel": "warning"
        },
        "inbounds": [
            {
                "tag": "vless-in",
                "port": vless_port,
                "protocol": "vless",
                "settings": {
                    "clients": clients,
                    "decryption": "none"
                },
                "streamSettings": {
                    "network": "tcp",
                    "security": "reality",
                    "realitySettings": {
                        "show": False,
                        "dest": f"{server_name}:443",
                        "xver": 0,
                        "serverNames": [server_name],
                        "privateKey": private_key,
                        "shortIds": short_ids
                    }
                }
            },
            {
                "tag": "hysteria2-in",
                "port": hy2_port,
                "protocol": "hysteria2",
                "settings": {
                    "ignoreClientBandwidth": False,
                    "masquerade": f"https://{server_name}"
                }
            }
        ],
        "outbounds": [
            {
                "protocol": "freedom",
                "tag": "direct"
            },
            {
                "protocol": "blackhole",
                "tag": "block"
            }
        ]
    }
    return config

def save_config_to_file(config, filepath="custom_config.json"):
    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    return filepath