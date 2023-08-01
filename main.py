import time
import requests
import telebot

# Укажите ваш токен от BotFather
TELEGRAM_BOT_TOKEN = "6585906202:AAHKQwx10jFglQhrJ2BpFVUg_YF_VDSO6qY"

# Создаем экземпляр бота
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Айди пользователя, которому будут приходить оповещения (замените на нужный)
USER_ID_TO_NOTIFY = 1065543980

def check_domain(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while checking {url}: {e}")
        return False

def check_domains_and_notify():
    domains = [
        {"url": "https://burya-t.ru/hui.json?rob", "name": "Polsha"},
        {"url": "https://st.burya-t.ru/status.php?installed", "name": "Storage"}
    ]

    for domain in domains:
        if not check_domain(domain["url"]):
            message = f"{domain['name']} снесли get запросом"
            bot.send_message(USER_ID_TO_NOTIFY, message)
            return

    print("1")


# Определим функцию-обработчик для команды /check
@bot.message_handler(commands=["check"])
def handle_check_command(message):
    check_domains_and_notify()
    bot.send_message(message.chat.id, "Checking completed.")

# Запустим бота и будем выполнять проверку каждый час
if __name__ == "__main__":
    while True:
        try:
            check_domains_and_notify()
            time.sleep(300)  # Пауза в 1 час перед следующей проверкой
        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(300)  # В случае ошибки пауза, чтобы не перегружать сервер Telegram
