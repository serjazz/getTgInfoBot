#!/usr/bin/env python3
"""
Скрипт для проверки корректности настройки проекта.
Проверяет все необходимые файлы, зависимости и конфигурацию.
"""

import os
import sys
import importlib
from pathlib import Path

def print_header(title):
    """Вывод заголовка"""
    print(f"\n{'='*50}")
    print(f" {title}")
    print(f"{'='*50}")

def print_section(title):
    """Вывод секции"""
    print(f"\n{'-'*30}")
    print(f" {title}")
    print(f"{'-'*30}")

def check_files():
    """Проверка наличия необходимых файлов"""
    print_section("Проверка файлов")
    
    required_files = [
        'requirements.txt',
        'config.py',
        'bot.py',
        'app.py',
        'env.example',
        'README.md',
        '.gitignore'
    ]
    
    missing_files = []
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️  Отсутствуют файлы: {', '.join(missing_files)}")
        return False
    
    print("\n✅ Все необходимые файлы присутствуют")
    return True

def check_python_version():
    """Проверка версии Python"""
    print_section("Проверка версии Python")
    
    version = sys.version_info
    print(f"Текущая версия: {version.major}.{version.minor}.{version.micro}")
    
    if version >= (3, 8):
        print("✅ Версия Python соответствует требованиям")
        return True
    else:
        print("❌ Требуется Python 3.8 или выше")
        return False

def check_dependencies():
    """Проверка зависимостей"""
    print_section("Проверка зависимостей")
    
    required_packages = [
        'telegram',
        'flask',
        'dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Отсутствуют пакеты: {', '.join(missing_packages)}")
        print("💡 Установите зависимости: pip install -r requirements.txt")
        return False
    
    print("\n✅ Все зависимости установлены")
    return True

def check_environment():
    """Проверка переменных окружения"""
    print_section("Проверка переменных окружения")
    
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ Файл .env не найден")
        print("💡 Скопируйте env.example в .env и настройте переменные")
        return False
    
    # Загружаем переменные окружения
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = ['BOT_TOKEN']
        missing_vars = []
        
        for var in required_vars:
            value = os.getenv(var)
            if value and value != "your_bot_token_here":
                print(f"✅ {var}: {'*' * len(value)}")
            else:
                print(f"❌ {var}: не установлен")
                missing_vars.append(var)
        
        if missing_vars:
            print(f"\n⚠️  Не настроены переменные: {', '.join(missing_vars)}")
            return False
        
        print("\n✅ Все переменные окружения настроены")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при загрузке .env: {e}")
        return False

def check_config():
    """Проверка конфигурации"""
    print_section("Проверка конфигурации")
    
    try:
        from config import BOT_TOKEN, WEBHOOK_URL, WEBHOOK_PORT, FLASK_HOST, FLASK_PORT, FLASK_DEBUG
        
        print(f"BOT_TOKEN: {'*' * len(BOT_TOKEN) if BOT_TOKEN else 'не установлен'}")
        print(f"WEBHOOK_URL: {WEBHOOK_URL}")
        print(f"WEBHOOK_PORT: {WEBHOOK_PORT}")
        print(f"FLASK_HOST: {FLASK_HOST}")
        print(f"FLASK_PORT: {FLASK_PORT}")
        print(f"FLASK_DEBUG: {FLASK_DEBUG}")
        
        if BOT_TOKEN:
            print("\n✅ Конфигурация загружена корректно")
            return True
        else:
            print("\n❌ BOT_TOKEN не установлен")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при загрузке конфигурации: {e}")
        return False

def check_bot_logic():
    """Проверка логики бота"""
    print_section("Проверка логики бота")
    
    try:
        from bot import TelegramBot
        print("✅ Класс TelegramBot импортирован успешно")
        
        # Проверяем методы класса
        bot = TelegramBot()
        methods = ['start_command', 'handle_forwarded_message', 'handle_message']
        
        for method in methods:
            if hasattr(bot, method):
                print(f"✅ Метод {method} присутствует")
            else:
                print(f"❌ Метод {method} отсутствует")
                return False
        
        print("\n✅ Логика бота корректна")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при проверке логики бота: {e}")
        return False

def check_flask_app():
    """Проверка Flask-приложения"""
    print_section("Проверка Flask-приложения")
    
    try:
        from app import app
        
        # Проверяем наличие маршрутов
        routes = ['/', '/webhook', '/health']
        for route in routes:
            if any(rule.rule == route for rule in app.url_map.iter_rules()):
                print(f"✅ Маршрут {route} зарегистрирован")
            else:
                print(f"❌ Маршрут {route} отсутствует")
                return False
        
        print("\n✅ Flask-приложение настроено корректно")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при проверке Flask-приложения: {e}")
        return False

def main():
    """Главная функция проверки"""
    print_header("Проверка настройки Telegram Info Bot")
    
    checks = [
        ("Файлы проекта", check_files),
        ("Версия Python", check_python_version),
        ("Зависимости", check_dependencies),
        ("Переменные окружения", check_environment),
        ("Конфигурация", check_config),
        ("Логика бота", check_bot_logic),
        ("Flask-приложение", check_flask_app)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Ошибка при проверке {name}: {e}")
            results.append((name, False))
    
    # Итоговый результат
    print_header("Результаты проверки")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ ПРОЙДЕНА" if result else "❌ ПРОВАЛЕНА"
        print(f"{name}: {status}")
    
    print(f"\n📊 Итого: {passed}/{total} проверок пройдено")
    
    if passed == total:
        print("\n🎉 Все проверки пройдены! Бот готов к работе.")
        print("\n💡 Для запуска используйте:")
        print("   - python start_dev.py (режим разработки)")
        print("   - python test_bot.py (тестирование)")
        print("   - python app.py (production)")
    else:
        print(f"\n⚠️  {total - passed} проверок не пройдено.")
        print("Исправьте ошибки и запустите проверку снова.")
        return 1
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n🛑 Проверка прервана пользователем")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        sys.exit(1) 