import sys
from builder import generate_config, save_config_to_file
from validator import validate_config
from env_checker import check_system_environment

CONFIG_FILE = "custom_config.json"

def main():
    print("============================================================")
    print("      🔍 Проверка системного окружения и конфигурации")
    print("============================================================")

    env_status = check_system_environment()
    print(f"  ✅ Запуск от root: {env_status['is_root']}")
    print(f"  ✅ Docker установлен: {env_status['docker_installed']}")
    print(f"  ✅ Контейнер remnanode запущен: {env_status['remnanode_running']}")
    print("============================================================")

    print("\n⚙️ Генерация кастомной конфигурации...")
    cfg = generate_config(
        vless_port=443,
        hy2_port=443,
        server_name="ultinfin.ultinvpn.biz",
        private_key="YOUR_PRIVATE_KEY_HERE"
    )

    saved_path = save_config_to_file(cfg, CONFIG_FILE)
    print(f"✅ Конфигурация успешно сохранена в: {saved_path}")

    print("\n🔍 Валидация созданного конфига...")
    is_valid, msg = validate_config(saved_path)

    if is_valid:
        print(f"✅ {msg}")
    else:
        print(f"❌ Ошибка валидации: {msg}")
        sys.exit(1)

if __name__ == "__main__":
    main()