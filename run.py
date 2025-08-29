#!/usr/bin/env python3
"""
Скрипт для запуска Telegram бота в режиме разработки.
Использует Flask для обработки webhook'ов.
"""

import os
import sys
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def check_environment():
    """Проверка необходимых переменных окружения"""
    required_vars = ['BOT_TOKEN']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Ошибка: Отсутствуют необходимые переменные окружения:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n📝 Создайте файл .env на основе env.example")
        return False
    
    return True

def main():
    """Главная функция запуска"""
    print("🚀 Запуск Telegram Info Bot...")
    
    # Проверяем переменные окружения
    if not check_environment():
        sys.exit(1)
    
    # Проверяем наличие необходимых файлов
    required_files = ['bot.py', 'app.py', 'config.py']
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Ошибка: Файл {file} не найден")
            sys.exit(1)
    
    print("✅ Все проверки пройдены")
    print("🌐 Запуск Flask-приложения...")
    
    try:
        # Импортируем и запускаем Flask-приложение
        from app import app
        from config import FLASK_HOST, FLASK_PORT, FLASK_DEBUG
        
        print(f"📡 Сервер запущен на http://{FLASK_HOST}:{FLASK_PORT}")
        print(f"🔗 Webhook endpoint: /webhook")
        print(f"📊 Health check: /health")
        print(f"🐛 Debug режим: {'Включен' if FLASK_DEBUG else 'Выключен'}")
        print("\n💡 Для остановки нажмите Ctrl+C")
        
        app.run(
            host=FLASK_HOST,
            port=FLASK_PORT,
            debug=FLASK_DEBUG
        )
        
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("💡 Убедитесь, что все зависимости установлены:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 