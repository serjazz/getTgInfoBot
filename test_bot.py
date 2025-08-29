#!/usr/bin/env python3
"""
Скрипт для тестирования Telegram бота в режиме polling.
Используется для локальной разработки без webhook.
"""

import asyncio
import logging
from telegram.ext import Application
from bot import TelegramBot
from config import BOT_TOKEN

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def test_polling():
    """Тестирование бота в режиме polling"""
    try:
        print("🚀 Запуск бота в режиме polling...")
        
        # Создаем экземпляр бота
        bot_instance = TelegramBot()
        
        # Удаляем webhook если он был установлен
        await bot_instance.application.bot.delete_webhook()
        print("✅ Webhook удален")
        
        # Запускаем polling
        print("📡 Запуск polling...")
        print("💡 Бот готов к работе!")
        print("🛑 Для остановки нажмите Ctrl+C")
        
        await bot_instance.application.run_polling(
            allowed_updates=["message", "callback_query"],
            drop_pending_updates=True
        )
        
    except Exception as e:
        logger.error(f"Ошибка при запуске: {e}")
        raise

def main():
    """Главная функция"""
    try:
        # Проверяем токен
        if not BOT_TOKEN:
            print("❌ Ошибка: BOT_TOKEN не установлен")
            print("💡 Создайте файл .env с вашим токеном")
            return
        
        # Запускаем бота
        asyncio.run(test_polling())
        
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен пользователем")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")

if __name__ == "__main__":
    main() 