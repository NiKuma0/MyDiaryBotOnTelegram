# MyDiaryBotOnTelegram
This bot sends you a message to you don't forget about deals 
(all interface on russian).

Небольшой журнал, в котором вы можете что-то планировать. 
Просто отправьте сообщение телеграм-боту "Новая задача!" потом ведите время и 
"послание". Оно вам придёт ровно в то время которое вы указали.

## Технологии
* Весь бот написан на языке 
[**Python v3.10**](https://www.python.org/)
* Для СУБД был использован [**SQLite**](https://www.sqlite.org/)
* Также не обошлось без фраемворке 
[**aiogram**](https://github.com/aiogram/aiogram)

## Как развернуть приложение
1. Сначала нужно клонировать репозиторий:
```bash
git clone https://github.com/NiKuma0/MyDiaryBotOnTelegram.git
```
2. Создаём бота с помощью 
[@BotFather](https://t.me/botfather), и запоминаем токен
3. В директории проекта создаём файл .env и заполняем его:
```bash
TOKEN=<BOT token>  # Токен вашего бота
ADMINS=<user id>,<user2 id>  # ID Ваших аккаунтов телеграм
```
4. Создайте окружение python3.10 и установите библиотеки:
```bash
python3.10 -m venv venv
. venv/bin/activate
python3.10 -m pip install -r requirements.txt
```
5. Запускаем!
```bash
python3.10 main.py
```
6. Напишите боту команду `/start_polling`.
