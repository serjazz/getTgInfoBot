#!/usr/bin/env python3
"""
Скрипт для быстрого запуска Telegram бота в режиме разработки.
Автоматически настраивает переменные окружения и запускает бота.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Проверка версии Python"""
    if sys.version_info < (3, 8):
        print("❌ Ошибка: Требуется Python 3.8 или выше")
        print(f"   Текущая версия: {sys.version}")
        return False
    print(f"✅ Python версия: {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Проверка и установка зависимостей"""
    print("📦 Проверка зависимостей...")
    
    try:
        import telegram
        import flask
        import dotenv
        print("✅ Все зависимости уже установлены")
        return True
    except ImportError:
        print("📥 Установка зависимостей...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Зависимости установлены")
            return True
        except subprocess.CalledProcessError:
            print("❌ Ошибка при установке зависимостей")
            return False

def setup_environment():
    """Настройка переменных окружения"""
    env_file = Path(".env")
    example_env = Path("env.example")
    
    if env_file.exists():
        print("✅ Файл .env уже существует")
        return True
    
    if not example_env.exists():
        print("❌ Файл env.example не найден")
        return False
    
    print("📝 Создание файла .env...")
    
    # Читаем пример конфигурации
    with open(example_env, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Заменяем placeholder'ы на значения по умолчанию
    content = content.replace("your_bot_token_here", "YOUR_BOT_TOKEN_HERE")
    content = content.replace("https://your-domain.com", "http://localhost:5000")
    content = content.replace("8443", "5000")
    content = content.replace("False", "True")
    
    # Записываем файл .env
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Файл .env создан")
    print("⚠️  Не забудьте указать ваш BOT_TOKEN в файле .env!")
    return True

def get_bot_token():
    """Получение токена бота от пользователя"""
    token = os.getenv('BOT_TOKEN')
    
    if token and token != "YOUR_BOT_TOKEN_HERE":
        return token
    
    print("\n🔑 Настройка токена бота:")
    print("1. Напишите @BotFather в Telegram")
    print("2. Создайте нового бота командой /newbot")
    print("3. Скопируйте полученный токен")
    
    while True:
        token = input("\nВведите токен бота: ").strip()
        if token and len(token) > 20:
            # Обновляем .env файл
            with open('.env', 'r', encoding='utf-8') as f:
                content = f.read()
            
            content = content.replace("YOUR_BOT_TOKEN_HERE", token)
            
            with open('.env', 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Токен сохранен в .env")
            return token
        else:
            print("❌ Неверный формат токена. Попробуйте снова.")

def start_bot():
    """Запуск бота"""
    print("\n🚀 Запуск бота...")
    
    try:
        # Запускаем Flask-приложение
        from app import app
        from config import FLASK_HOST, FLASK_PORT, FLASK_DEBUG
        
        print(f"📡 Сервер запущен на http://{FLASK_HOST}:{FLASK_PORT}")
        print(f"🔗 Webhook endpoint: /webhook")
        print(f"📊 Health check: /health")
        print(f"🐛 Debug режим: {'Включен' if FLASK_DEBUG else 'Выключен'}")
        print("\n💡 Для остановки нажмите Ctrl+C")
        print("⚠️  В режиме разработки webhook не будет работать!")
        print("   Для тестирования используйте test_bot.py")
        
        app.run(
            host=FLASK_HOST,
            port=FLASK_PORT,
            debug=FLASK_DEBUG
        )
        
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")
        return False

def main():
    """Главная функция"""
    print("🤖 Telegram Info Bot - Режим разработки")
    print("=" * 50)
    
    # Проверяем версию Python
    if not check_python_version():
        sys.exit(1)
    
    # Проверяем зависимости
    if not check_dependencies():
        sys.exit(1)
    
    # Настраиваем окружение
    if not setup_environment():
        sys.exit(1)
    
    # Получаем токен бота
    token = get_bot_token()
    if not token:
        print("❌ Токен бота не указан")
        sys.exit(1)
    
    # Запускаем бота
    start_bot()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен пользователем")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        sys.exit(1) 