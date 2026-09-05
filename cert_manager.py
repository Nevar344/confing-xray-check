import os
import shutil
import subprocess

DOCKER_COMPOSE_PATH = "docker-compose.yml"


def check_certbot_installed() -> bool:
    return shutil.which("certbot") is not None


def install_certbot() -> bool:
    print("📦 Установка certbot...")
    try:
        if shutil.which("apt-get"):
            subprocess.run(["apt-get", "update"], check=True)
            subprocess.run(["apt-get", "install", "-y", "certbot"], check=True)
            return True
        elif shutil.which("yum"):
            subprocess.run(["yum", "install", "-y", "certbot"], check=True)
            return True
    except Exception as e:
        print(f"❌ Ошибка при установке certbot: {e}")
    return False


def issue_letsencrypt_cert(domain: str, email: str = "") -> tuple[bool, str, str]:
    """Выпускает сертификаты через Certbot в автономном (standalone) режиме."""
    if not check_certbot_installed():
        if not install_certbot():
            return False, "", ""

    cmd = [
        "certbot", "certonly", "--standalone",
        "-d", domain,
        "--non-interactive", "--agree-tos"
    ]
    if email:
        cmd.extend(["-m", email])
    else:
        cmd.append("--register-unsafely-without-email")

    print(f"🔒 Выпуск SSL-сертификата для {domain} через Let's Encrypt...")
    try:
        res = subprocess.run(cmd, capture_output=True, text=True)
        fullchain = f"/etc/letsencrypt/live/{domain}/fullchain.pem"
        privkey = f"/etc/letsencrypt/live/{domain}/privkey.pem"

        if os.path.exists(fullchain) and os.path.exists(privkey):
            print("✅ Сертификаты успешно выпущены!")
            return True, fullchain, privkey
        else:
            print(f"❌ Ошибка выпуска сертификатов: {res.stderr}")
            return False, "", ""
    except Exception as e:
        print(f"❌ Ошибка запуска certbot: {e}")
        return False, "", ""


def update_docker_compose_certs(domain: str) -> bool:
    """Автоматически добавляет проброс SSL-сертификатов в docker-compose.yml для remnawave-nginx."""
    if not os.path.exists(DOCKER_COMPOSE_PATH):
        print(f"⚠️ Файл {DOCKER_COMPOSE_PATH} не найден в текущей директории.")
        return False

    fullchain_vol = f"      - /etc/letsencrypt/live/{domain}/fullchain.pem:/etc/nginx/ssl/{domain}/fullchain.pem:ro"
    privkey_vol = f"      - /etc/letsencrypt/live/{domain}/privkey.pem:/etc/nginx/ssl/{domain}/privkey.pem:ro"

    with open(DOCKER_COMPOSE_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    if f"/etc/letsencrypt/live/{domain}/fullchain.pem" in content:
        print("ℹ️ Сертификаты уже прописаны в docker-compose.yml")
        return True

    if "- /dev/shm:/dev/shm:rw" in content:
        new_volumes = f"{fullchain_vol}\n{privkey_vol}\n      - /dev/shm:/dev/shm:rw"
        updated_content = content.replace("      - /dev/shm:/dev/shm:rw", new_volumes)
        with open(DOCKER_COMPOSE_PATH, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print("✅ docker-compose.yml успешно обновлен!")
        return True

    return False


def open_port_firewall(port: int, proto: str = "both") -> bool:
    """Активирует и открывает порты через UFW или iptables."""
    print(f"🔓 Открытие порта {port}/{proto.upper()} в файрволе...")

    if shutil.which("ufw"):
        try:
            if proto in ["tcp", "both"]:
                subprocess.run(["ufw", "allow", f"{port}/tcp"], check=True)
            if proto in ["udp", "both"]:
                subprocess.run(["ufw", "allow", f"{port}/udp"], check=True)
            print("✅ Порты успешно открыты в UFW!")
            return True
        except Exception as e:
            print(f"⚠️ Ошибка UFW: {e}")

    if shutil.which("iptables"):
        try:
            if proto in ["tcp", "both"]:
                subprocess.run(["iptables", "-I", "INPUT", "-p", "tcp", "--dport", str(port), "-j", "ACCEPT"],
                               check=True)
            if proto in ["udp", "both"]:
                subprocess.run(["iptables", "-I", "INPUT", "-p", "udp", "--dport", str(port), "-j", "ACCEPT"],
                               check=True)
            print("✅ Правила добавлены в iptables!")
            return True
        except Exception as e:
            print(f"⚠️ Ошибка iptables: {e}")

    return False