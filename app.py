from flask import Flask, request, jsonify
import asyncio
import logging
from bot import TelegramBot
from config import FLASK_HOST, FLASK_PORT, FLASK_DEBUG

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
bot = TelegramBot()

@app.route('/webhook', methods=['POST'])
def webhook():
    """Webhook endpoint для Telegram Bot API"""
    try:
        # Получаем данные от Telegram
        update_data = request.get_json()
        
        if update_data is None:
            logger.warning("Получены пустые данные от Telegram")
            return jsonify({"status": "error", "message": "Empty data"}), 400
        
        logger.info(f"Получен webhook: {update_data.get('update_id', 'unknown')}")
        
        # Обрабатываем обновление асинхронно
        asyncio.run(bot.webhook_handler(update_data))
        
        return jsonify({"status": "ok"}), 200
    
    except Exception as e:
        logger.error(f"Ошибка при обработке webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Проверка состояния сервиса"""
    return jsonify({
        "status": "healthy",
        "service": "Telegram Bot Webhook",
        "timestamp": asyncio.run(bot.application.bot.get_me()).to_dict()
    })

@app.route('/', methods=['GET'])
def index():
    """Главная страница"""
    return jsonify({
        "service": "Telegram Bot Webhook",
        "endpoints": {
            "webhook": "/webhook",
            "health": "/health"
        },
        "status": "running"
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    logger.info(f"Запуск Flask-приложения на {FLASK_HOST}:{FLASK_PORT}")
    app.run(
        host=FLASK_HOST,
        port=FLASK_PORT,
        debug=FLASK_DEBUG
    ) 