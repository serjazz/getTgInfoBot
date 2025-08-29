# 🚀 Инструкция по развертыванию

## 📋 Предварительные требования

### 1. Сервер
- VPS или выделенный сервер
- Ubuntu 20.04+ или CentOS 8+
- Минимум 1 ГБ RAM
- Минимум 10 ГБ дискового пространства

### 2. Домен
- Зарегистрированный домен
- Настроенный DNS (A-запись на IP сервера)
- SSL-сертификат (Let's Encrypt)

### 3. Telegram Bot
- Созданный бот через @BotFather
- Полученный токен

## 🛠️ Пошаговая установка

### Шаг 1: Подключение к серверу
```bash
ssh root@your-server-ip
```

### Шаг 2: Обновление системы
```bash
apt update && apt upgrade -y
```

### Шаг 3: Установка необходимых пакетов
```bash
apt install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx git curl
```

### Шаг 4: Создание пользователя для бота
```bash
adduser tgbot
usermod -aG sudo tgbot
su - tgbot
```

### Шаг 5: Клонирование репозитория
```bash
cd /home/tgbot
git clone <your-repository-url> GetTGInfoBot
cd GetTGInfoBot
```

### Шаг 6: Создание виртуального окружения
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Шаг 7: Настройка конфигурации
```bash
cp env.example .env
nano .env
```

Заполните файл `.env`:
```env
BOT_TOKEN=your_actual_bot_token
WEBHOOK_URL=https://your-domain.com
WEBHOOK_PORT=8443
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
FLASK_DEBUG=False
```

### Шаг 8: Настройка Nginx
```bash
sudo nano /etc/nginx/sites-available/tg-bot
```

Содержимое конфигурации:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        return 301 https://$server_name$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    # SSL настройки
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    # Webhook endpoint
    location /webhook {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Health check
    location /health {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
    }
    
    # Главная страница
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
    }
}
```

Активируйте конфигурацию:
```bash
sudo ln -s /etc/nginx/sites-available/tg-bot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Шаг 9: Получение SSL-сертификата
```bash
sudo certbot --nginx -d your-domain.com
```

### Шаг 10: Создание systemd сервиса
```bash
sudo nano /etc/systemd/system/gettginfobot.service
```

Содержимое сервиса:
```ini
[Unit]
Description=Telegram Info Bot
After=network.target

[Service]
Type=simple
User=tgbot
WorkingDirectory=/home/tgbot/GetTGInfoBot
Environment=PATH=/home/tgbot/GetTGInfoBot/venv/bin
ExecStart=/home/tgbot/GetTGInfoBot/venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Активируйте сервис:
```bash
sudo systemctl daemon-reload
sudo systemctl enable gettginfobot
sudo systemctl start gettginfobot
```

### Шаг 11: Проверка статуса
```bash
sudo systemctl status gettginfobot
sudo journalctl -u gettginfobot -f
```

## 🔧 Настройка файрвола

```bash
# Открываем необходимые порты
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## 📊 Мониторинг

### Просмотр логов
```bash
# Логи сервиса
sudo journalctl -u gettginfobot -f

# Логи Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Проверка состояния
```bash
# Статус сервиса
sudo systemctl status gettginfobot

# Проверка webhook
curl https://your-domain.com/health

# Проверка webhook endpoint
curl -X POST https://your-domain.com/webhook
```

## 🚨 Устранение неполадок

### Бот не отвечает
1. Проверьте статус сервиса: `sudo systemctl status gettginfobot`
2. Проверьте логи: `sudo journalctl -u gettginfobot -f`
3. Убедитесь, что webhook установлен

### Webhook не работает
1. Проверьте конфигурацию Nginx
2. Убедитесь, что SSL-сертификат действителен
3. Проверьте, что порт 443 открыт

### Ошибки в логах
1. Проверьте права доступа к файлам
2. Убедитесь, что все зависимости установлены
3. Проверьте переменные окружения

## 🔄 Обновление бота

```bash
cd /home/tgbot/GetTGInfoBot
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart gettginfobot
```

## 📱 Тестирование

После развертывания протестируйте бота:

1. Отправьте команду `/start`
2. Перешлите сообщение из другого чата
3. Проверьте webhook endpoint: `https://your-domain.com/health`

## 🔒 Безопасность

- Регулярно обновляйте систему
- Используйте сильные пароли
- Ограничьте доступ по SSH
- Настройте fail2ban
- Регулярно обновляйте SSL-сертификаты

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи сервиса
2. Проверьте логи Nginx
3. Убедитесь в правильности конфигурации
4. Создайте Issue в репозитории 