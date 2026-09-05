import os
import sys
import subprocess
import json
import shutil
import uuid

# Попытка импорта rich дляสวยного TUI интерфейса в терминале
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich import print as rprint
except ImportError:
    print("Установка необходимых библиотек интерфейса (rich)...")
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], check=True)
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich import print as rprint

console = Console()


def run_cmd(command: str) -> tuple[int, str]:
    """Выполнение системной команды и возврат кода ответа и вывода."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout.strip()


def check_environment() -> bool:
    """Выполнение всех системных проверок с отображением TUI."""
    console.print("\n[bold cyan]🔍 Запуск системных проверок окружения...[/bold cyan]\n")

    checks = [
        ("Проверка запуска от root", "id -u", lambda code, out: code == 0 and out == "0"),
        ("Проверка наличия Docker", "which docker", lambda code, out: code == 0),
        ("Проверка доступности Docker daemon", "docker info", lambda code, out: code == 0),
        ("Проверка наличия контейнера remnanode", "docker ps -a --format '{{.Names}}'",
         lambda code, out: "remnanode" in out.splitlines()),
        ("Проверка статуса работы remnanode", "docker ps --format '{{.Names}}'",
         lambda code, out: "remnanode" in out.splitlines()),
        ("Проверка доступности /dev/shm", "mountpoint -q /dev/shm || [ -d /dev/shm ]", lambda code, out: code == 0),
        ("Проверка наличия сертификатов Let's Encrypt", "test -d /etc/letsencrypt/live", lambda code, out: code == 0),
        ("Проверка работы VLESS Reality (443/tcp)", "ss -tulnp | grep -E '443.*tcp|tcp.*443'",
         lambda code, out: code == 0)
    ]

    table = Table(title="Результаты проверки системы", show_header=True, header_style="bold magenta")
    table.add_column("Компонент", style="cyan")
    table.add_column("Статус", justify="center")

    all_passed = True

    for name, cmd, check_fn in checks:
        code, out = run_cmd(cmd)
        passed = check_fn(code, out)
        if passed:
            table.add_row(name, "[bold green]PASS ✅[/bold green]")
        else:
            table.add_row(name, "[bold red]FAIL ❌[/bold red]")
            all_passed = False

    console.print(table)
    return all_passed


def setup_hysteria2_system(domain: str) -> bool:
    """Настройка окружения Linux для Hysteria2 (файервол, certs, cron, /dev/shm)."""
    console.print(Panel("[bold yellow]⚙️ Настройка системных компонентов Hysteria2[/bold yellow]"))

    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
    ) as progress:

        # 1. Открытие порта 443/udp в ufw/iptables
        progress.add_task(description="Открытие порта 443/UDP в файерволе...", total=None)
        run_cmd("ufw allow 443/udp")
        run_cmd("iptables -A INPUT -p udp --dport 443 -j ACCEPT")

        # 2. Копирование сертификатов в /dev/shm
        progress.add_task(description="Копирование сертификатов в /dev/shm...", total=None)
        shm_cert_dir = "/dev/shm/hy2_certs"
        os.makedirs(shm_cert_dir, exist_ok=True)

        cert_path = f"/etc/letsencrypt/live/{domain}/fullchain.pem"
        key_path = f"/etc/letsencrypt/live/{domain}/privkey.pem"

        if os.path.exists(cert_path) and os.path.exists(key_path):
            shutil.copy(cert_path, f"{shm_cert_dir}/fullchain.pem")
            shutil.copy(key_path, f"{shm_cert_dir}/privkey.pem")
            run_cmd(f"chmod 644 {shm_cert_dir}/*.pem")
        else:
            console.print(f"[bold red]❌ Сертификаты для домена {domain} не найдены в /etc/letsencrypt/live/[/bold red]")
            return False

        # 3. Настройка автоматической синхронизации и Cron задач
        progress.add_task(description="Создание скрипта автообновления и Cron...", total=None)
        sync_script = "/usr/local/bin/sync_hy2_certs.sh"
        script_content = f"""#!/bin/bash
cp /etc/letsencrypt/live/{domain}/fullchain.pem /dev/shm/hy2_certs/fullchain.pem
cp /etc/letsencrypt/live/{domain}/privkey.pem /dev/shm/hy2_certs/privkey.pem
chmod 644 /dev/shm/hy2_certs/*.pem
docker restart remnanode
"""
        with open(sync_script, "w") as f:
            f.write(script_content)
        os.chmod(sync_script, 0o755)

        # Добавление в cron (каждый день в 03:00)
        cron_job = "0 3 * * * /usr/local/bin/sync_hy2_certs.sh >/dev/null 2>&1"
        _, current_cron = run_cmd("crontab -l")
        if "sync_hy2_certs.sh" not in current_cron:
            new_cron = f"{current_cron}\n{cron_job}\n" if current_cron else f"{cron_job}\n"
            subprocess.run(["crontab", "-"], input=new_cron, text=True)

    console.print("[bold green]✅ Системные зависимости Hysteria2 успешно настроены![/bold green]\n")
    return True


def inject_hysteria2_config(config_path: str, password: str) -> bool:
    """Встраивание инбаунда Hysteria2 на порт 443/UDP в config.json."""
    if not os.path.exists(config_path):
        console.print(f"[bold red]❌ Файл {config_path} не найден![/bold red]")
        return False

    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # Проверяем, есть ли уже Hysteria2
    inbounds = config.setdefault("inbounds", [])
    for inbound in inbounds:
        if inbound.get("protocol") == "hysteria2" or inbound.get("tag") == "hy2-inbound-443":
            console.print(
                "[bold yellow]⚠️ Инбаунд Hysteria2 уже существует в конфиге! Обновляем настройки...[/bold yellow]")
            inbounds.remove(inbound)
            break

    # Формируем шаблон Hysteria2 на 443 UDP
    hy2_inbound = {
        "tag": "hy2-inbound-443",
        "port": 443,
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
                "alpn": ["h3"]
            }
        }
    }

    inbounds.append(hy2_inbound)

    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    console.print("[bold green]✅ Hysteria2 успешно встроена в config.json на порт 443/UDP![/bold green]")
    return True


def main():
    console.print(Panel.fit(
        "[bold white on blue] 🚀 UltinVPN Smart Deployment Wizard [/bold white on blue]\n"
        "[dim]Автоматическая установка VLESS-Reality & Hysteria2 на порт 443[/dim]",
        border_style="cyan"
    ))

    # Выполнение проверок
    if not check_environment():
        console.print("\n[bold red]❌ Система не прошла предпроверку! Исправьте ошибки и запустите снова.[/bold red]")
        sys.exit(1)

    console.print("\n[bold green]🎉 Все предварительные проверки пройдены успешно![/bold green]\n")

    print("Выберите режим установки:")
    print("1. Установить / Обновить Hysteria 2 (на порт 443/UDP с авто-сертификатами)")
    print("2. Стандартный VLESS Reality")
    print("3. Выход")

    choice = input("\nВаш выбор (1-3): ").strip()

    if choice == "1":
        domain = input("Введите домен Let's Encrypt (например, sub.domain.com): ").strip()
        if not domain:
            console.print("[bold red]❌ Домен не может быть пустым![/bold red]")
            return

        config_path = input(
            "Путь к config.json (по умолчанию /etc/remnanode/config.json): ").strip() or "/etc/remnanode/config.json"

        password = input("Введите пароль для Hysteria2 (оставьте пустым для автогенерации): ").strip()
        if not password:
            password = str(uuid.uuid4())
            console.print(f"🔑 Сгенерирован пароль: [bold cyan]{password}[/bold cyan]")

        # Запуск настройки системы и конфига
        if setup_hysteria2_system(domain):
            if inject_hysteria2_config(config_path, password):
                console.print("\n[bold yellow]🔄 Перезапускаем контейнер remnanode...[/bold yellow]")
                run_cmd("docker restart remnanode")
                console.print(Panel(
                    f"[bold green]✨ Настройка завершена успешно![/bold green]\n\n"
                    f"• Протокол: [cyan]Hysteria 2[/cyan]\n"
                    f"• Порт: [cyan]443 (UDP)[/cyan]\n"
                    f"• Пароль: [cyan]{password}[/cyan]\n"
                    f"• Сертификаты: [cyan]/dev/shm/hy2_certs/[/cyan]",
                    title="Итог установки",
                    border_style="green"
                ))


if __name__ == "__main__":
    main()