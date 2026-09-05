import os
import shutil
import subprocess
import socket
import glob

def check_root() -> tuple[bool, str]:
    if os.geteuid() == 0:
        return True, "Запуск от пользователя root"
    return False, "Скрипт должен быть запущен от root (используйте sudo)"

def check_docker_installed() -> tuple[bool, str]:
    if shutil.which("docker") is not None:
        return True, "Docker установлен"
    return False, "Docker не найден в системе"

def check_docker_daemon() -> tuple[bool, str]:
    try:
        res = subprocess.run(["docker", "info"], capture_output=True, text=True, timeout=5)
        if res.returncode == 0:
            return True, "Docker daemon доступен"
        return False, "Docker daemon недоступен или не запущен"
    except Exception as e:
        return False, f"Ошибка при обращении к Docker daemon: {e}"

def check_container_exists(container_name: str = "remnanode") -> tuple[bool, str]:
    try:
        res = subprocess.run(
            ["docker", "ps", "-a", "--format", "{{.Names}}"],
            capture_output=True, text=True, timeout=5
        )
        containers = res.stdout.strip().split("\n")
        if container_name in containers:
            return True, f"Контейнер '{container_name}' найден"
        return False, f"Контейнер '{container_name}' не найден"
    except Exception as e:
        return False, f"Ошибка поиска контейнера: {e}"

def check_container_running(container_name: str = "remnanode") -> tuple[bool, str]:
    try:
        res = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}"],
            capture_output=True, text=True, timeout=5
        )
        running_containers = res.stdout.strip().split("\n")
        if container_name in running_containers:
            return True, f"Контейнер '{container_name}' запущен"
        return False, f"Контейнер '{container_name}' остановлен"
    except Exception as e:
        return False, f"Ошибка проверки статуса контейнера: {e}"

def check_dev_shm() -> tuple[bool, str]:
    if os.path.exists("/dev/shm") and os.access("/dev/shm", os.W_OK):
        return True, "Директория /dev/shm доступна для записи"
    return False, "Директория /dev/shm недоступна или закрыта для записи"

def check_existing_certificates() -> tuple[bool, str, str]:
    """Сканирует /etc/letsencrypt/live/ на наличие готовых сертификатов."""
    certs = glob.glob("/etc/letsencrypt/live/*/fullchain.pem")
    if certs:
        fullchain = certs[0]
        domain = fullchain.split("/")[4]
        privkey = f"/etc/letsencrypt/live/{domain}/privkey.pem"
        if os.path.exists(privkey):
            return True, domain, fullchain
    return False, "", ""

def check_port_listening(port: int = 443, proto: str = "tcp") -> tuple[bool, str]:
    try:
        sock_type = socket.SOCK_STREAM if proto == "tcp" else socket.SOCK_DGRAM
        with socket.socket(socket.AF_INET, sock_type) as s:
            s.settimeout(1.0)
            result = s.connect_ex(("127.0.0.1", port))
            if result == 0:
                return True, f"Порт {port}/{proto.upper()} активен"
            return False, f"Порт {port}/{proto.upper()} закрыт или не отвечает"
    except Exception as e:
        return False, f"Ошибка проверки порта {port}/{proto}: {e}"

def run_all_checks() -> dict:
    has_certs, cert_domain, cert_path = check_existing_certificates()
    return {
        "root": check_root(),
        "docker_installed": check_docker_installed(),
        "docker_daemon": check_docker_daemon(),
        "container_exists": check_container_exists(),
        "container_running": check_container_running(),
        "dev_shm": check_dev_shm(),
        "certs": (has_certs, f"Домен: {cert_domain}" if has_certs else "Сертификаты не найдены"),
        "cert_domain": cert_domain,
        "vless_port_443_tcp": check_port_listening(443, "tcp"),
        "hy2_port_443_udp": check_port_listening(443, "udp")
    }