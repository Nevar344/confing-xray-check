#!/usr/bin/env bash

set -e

# Цветовое оформление
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}====================================================${NC}"
echo -e "${GREEN}    🚀 Remnanode Config Assistant Installer        ${NC}"
echo -e "${GREEN}====================================================${NC}"

# Проверка root прав
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}❌ Ошибка: Запустите скрипт от пользователя root (sudo).${NC}"
  exit 1
fi

# Проверка наличия Python3 и Git
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 не найден. Устанавливаем python3...${NC}"
    apt-get update && apt-get install -y python3 git || yum install -y python3 git
fi

INSTALL_DIR="/opt/confing-xray-check"

if [ -d "$INSTALL_DIR" ]; then
    echo -e "🔄 Обновление существующего репозитория..."
    cd "$INSTALL_DIR"
    git pull origin main 2>/dev/null || git pull origin master 2>/dev/null || true
else
    echo -e "📦 Загрузка компонентов из репозитория..."
    git clone https://github.com/Nevar344/confing-xray-check.git "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

echo -e "${GREEN}✅ Запуск ассистента...${NC}\n"
python3 main.py
