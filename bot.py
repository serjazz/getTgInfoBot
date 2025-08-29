import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import BOT_TOKEN, WEBHOOK_URL, WEBHOOK_PORT

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        self.application = Application.builder().token(BOT_TOKEN).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Настройка обработчиков сообщений"""
        # Обработчик команды /start
        self.application.add_handler(CommandHandler("start", self.start_command))
        
        # Обработчик пересланных сообщений
        self.application.add_handler(MessageHandler(filters.FORWARDED, self.handle_forwarded_message))
        
        # Обработчик всех остальных сообщений
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /start"""
        user = update.effective_user
        welcome_text = (
            f"👋 Привет, {user.first_name}!\n\n"
            "Я бот для получения информации о пользователях и каналах.\n\n"
            "📋 Что я умею:\n"
            "• Отвечаю на команду /start\n"
            "• Анализирую пересланные сообщения\n"
            "• Показываю ID пользователей и каналов\n\n"
            "📤 Перешлите мне сообщение из другого чата или канала, "
            "и я покажу всю доступную информацию!"
        )
        
        await update.message.reply_text(welcome_text)
    
    async def handle_forwarded_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка пересланных сообщений"""
        message = update.message
        user = update.effective_user
        
        # Собираем информацию о пересланном сообщении
        info_text = "📤 Информация о пересланном сообщении:\n\n"
        
        # Информация о текущем пользователе
        info_text += f"👤 **Отправитель запроса:**\n"
        info_text += f"• ID: `{user.id}`\n"
        info_text += f"• Имя: {user.first_name}\n"
        if user.last_name:
            info_text += f"• Фамилия: {user.last_name}\n"
        if user.username:
            info_text += f"• Username: @{user.username}\n"
        info_text += "\n"
        
        # Информация о пересланном сообщении
        if message.forward_from:
            forward_user = message.forward_from
            info_text += f"📤 **Переслано от пользователя:**\n"
            info_text += f"• ID: `{forward_user.id}`\n"
            info_text += f"• Имя: {forward_user.first_name}\n"
            if forward_user.last_name:
                info_text += f"• Фамилия: {forward_user.last_name}\n"
            if forward_user.username:
                info_text += f"• Username: @{forward_user.username}\n"
            info_text += "\n"
        
        # Информация о чате, откуда переслано
        if message.forward_from_chat:
            forward_chat = message.forward_from_chat
            info_text += f"📢 **Переслано из чата/канала:**\n"
            info_text += f"• ID: `{forward_chat.id}`\n"
            info_text += f"• Тип: {forward_chat.type}\n"
            info_text += f"• Название: {forward_chat.title}\n"
            if forward_chat.username:
                info_text += f"• Username: @{forward_chat.username}\n"
            info_text += "\n"
        
        # Информация о дате пересылки
        if message.forward_date:
            from datetime import datetime
            forward_date = datetime.fromtimestamp(message.forward_date)
            info_text += f"📅 **Дата пересылки:**\n"
            info_text += f"• {forward_date.strftime('%d.%m.%Y %H:%M:%S')}\n\n"
        
        # Информация о текущем чате
        chat = message.chat
        info_text += f"💬 **Текущий чат:**\n"
        info_text += f"• ID: `{chat.id}`\n"
        info_text += f"• Тип: {chat.type}\n"
        if chat.title:
            info_text += f"• Название: {chat.title}\n"
        if chat.username:
            info_text += f"• Username: @{chat.username}\n"
        
        await message.reply_text(info_text, parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка обычных текстовых сообщений"""
        message = update.message
        user = update.effective_user
        
        info_text = (
            f"📝 **Информация о сообщении:**\n\n"
            f"👤 **Отправитель:**\n"
            f"• ID: `{user.id}`\n"
            f"• Имя: {user.first_name}\n"
        )
        
        if user.last_name:
            info_text += f"• Фамилия: {user.last_name}\n"
        if user.username:
            info_text += f"• Username: @{user.username}\n"
        
        info_text += f"\n💬 **Чат:**\n"
        info_text += f"• ID: `{message.chat.id}`\n"
        info_text += f"• Тип: {message.chat.type}\n"
        
        if message.chat.title:
            info_text += f"• Название: {message.chat.title}\n"
        if message.chat.username:
            info_text += f"• Username: @{message.chat.username}\n"
        
        info_text += f"\n💡 **Подсказка:** Перешлите сообщение из другого чата, "
        info_text += f"чтобы получить больше информации!"
        
        await message.reply_text(info_text, parse_mode='Markdown')
    
    def webhook_handler_sync(self, update_dict):
        """Полностью синхронная обработка webhook"""
        try:
            from telegram import Update
            update = Update.de_json(update_dict, self.application.bot)
            
            message = update.message
            user = update.effective_user
            chat = update.effective_chat
            
            if not message:
                return True
            
            # Определяем тип сообщения и формируем ответ
            if message.text == '/start':
                response_text = f"👋 Привет, {user.first_name}!\n\nЯ бот для получения информации о пользователях и каналах.\n\n📋 Что я умею:\n• Отвечаю на команду /start\n• Анализирую пересланные сообщения\n• Показываю ID пользователей и каналов\n\n📤 Перешлите мне сообщение из другого чата или канала, и я покажу всю доступную информацию!"
            elif message.forward_from or message.forward_from_chat:
                response_text = self._format_forwarded_info_sync(message, user, chat)
            else:
                response_text = self._format_message_info_sync(message, user, chat)
            
            # Отправляем ответ синхронно через HTTP API
            import requests
            url = f"https://api.telegram.org/bot{self.application.bot.token}/sendMessage"
            data = {
                'chat_id': chat.id,
                'text': response_text,
                # 'parse_mode': 'Markdown'  # закомментируйте эту строку
            }
            
            response = requests.post(url, json=data)
            if response.status_code == 200:
                logger.info(f"Сообщение отправлено в чат {chat.id}")
            else:
                logger.error(f"Ошибка отправки: {response.status_code} - {response.text}")
            
            return True
            
        except Exception as e:
            logger.error(f"Ошибка в webhook_handler_sync: {e}")
            return False

    def _format_forwarded_info_sync(self, message, user, chat):
        """Форматирование информации о пересланном сообщении"""
        info_text = "📤 Информация о пересланном сообщении:\n\n"
        
        # Информация о текущем пользователе
        info_text += f"👤 Отправитель запроса:\n"
        info_text += f"• ID: {user.id}\n"
        info_text += f"• Имя: {user.first_name}\n"
        if user.last_name:
            info_text += f"• Фамилия: {user.last_name}\n"
        if user.username:
            info_text += f"• Username: @{user.username}\n"
        info_text += "\n"
        
        # Информация о пересланном сообщении
        if message.forward_from:
            forward_user = message.forward_from
            info_text += f"📤 Переслано от пользователя:\n"
            info_text += f"• ID: {forward_user.id}\n"
            info_text += f"• Имя: {forward_user.first_name}\n"
            if forward_user.last_name:
                info_text += f"• Фамилия: {forward_user.last_name}\n"
            if forward_user.username:
                info_text += f"• Username: @{forward_user.username}\n"
            info_text += "\n"
        
        # Информация о чате, откуда переслано
        if message.forward_from_chat:
            forward_chat = message.forward_from_chat
            info_text += f"📢 Переслано из чата/канала:\n"
            info_text += f"• ID: {forward_chat.id}\n"
            info_text += f"• Тип: {forward_chat.type}\n"
            if forward_chat.title:
                info_text += f"• Название: {forward_chat.title}\n"
            if forward_chat.username:
                info_text += f"• Username: @{forward_chat.username}\n"
            info_text += "\n"
        
        # Информация о дате пересылки (исправлено)
        if hasattr(message, 'forward_date') and message.forward_date:
            try:
                from datetime import datetime
                # Проверяем тип forward_date
                if isinstance(message.forward_date, datetime):
                    forward_date = message.forward_date
                else:
                    # Если это timestamp, конвертируем
                    forward_date = datetime.fromtimestamp(message.forward_date)
                
                info_text += f"📅 Дата пересылки:\n"
                info_text += f"• {forward_date.strftime('%d.%m.%Y %H:%M:%S')}\n\n"
            except Exception as e:
                logger.warning(f"Ошибка форматирования даты: {e}")
                info_text += f"📅 Дата пересылки:\n"
                info_text += f"• {message.forward_date}\n\n"
        
        # Информация о текущем чате
        info_text += f"💬 Текущий чат:\n"
        info_text += f"• ID: {chat.id}\n"
        info_text += f"• Тип: {chat.type}\n"
        if hasattr(chat, 'title') and chat.title:
            info_text += f"• Название: {chat.title}\n"
        if hasattr(chat, 'username') and chat.username:
            info_text += f"• Username: @{chat.username}\n"
        
        return info_text

    def _format_message_info_sync(self, message, user, chat):
        """Форматирование информации о сообщении"""
        info_text = (
            f"📝 Информация о сообщении:\n\n"
            f"👤 Отправитель:\n"
            f"• ID: {user.id}\n"
            f"• Имя: {user.first_name}\n"
        )
        
        if user.last_name:
            info_text += f"• Фамилия: {user.last_name}\n"
        if user.username:
            info_text += f"• Username: @{user.username}\n"
        
        info_text += f"\n💬 Чат:\n"
        info_text += f"• ID: {chat.id}\n"
        info_text += f"• Тип: {chat.type}\n"
        
        if hasattr(chat, 'title') and chat.title:
            info_text += f"• Название: {chat.title}\n"
        if hasattr(chat, 'username') and chat.username:
            info_text += f"• Username: @{chat.username}\n"
        
        info_text += f"\n💡 Подсказка: Перешлите сообщение из другого чата, "
        info_text += f"чтобы получить больше информации!"
        
        return info_text
    
    def run_webhook(self):
        """Запуск бота через webhook"""
        # Устанавливаем webhook
        self.application.bot.set_webhook(url=f"{WEBHOOK_URL}:{WEBHOOK_PORT}/webhook")
        logger.info(f"Webhook установлен на {WEBHOOK_URL}:{WEBHOOK_PORT}/webhook")
        
        # Запускаем приложение
        self.application.run_webhook(
            listen="0.0.0.0",
            port=WEBHOOK_PORT,
            webhook_url=f"{WEBHOOK_URL}:{WEBHOOK_PORT}/webhook"
        )

if __name__ == "__main__":
    bot = TelegramBot()
    bot.run_webhook() 