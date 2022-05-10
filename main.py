import sqlite3
import telebot
from telebot import types

bot = telebot.TeleBot("5129841473:AAHT89WpQ2HcFs61GGGHolaXfWh0b_n3AmE")

speed = 2  # быстрая ли машина
cheap = 2  # дешевая ли машина
patency = 2  # проходимая ли машина
capacity = 2  # вместимая ли машина

current_char = 0

is_review = 0
cur_rate = 0
cur_review = ""
is_naming = 0
cur_name = ""


# обрабокта команды старт
@bot.message_handler(commands=['start'])
def send_welcome(message):
    global current_char
    current_char = 0
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Да, начнём"))
    markup.add(types.KeyboardButton("Посмотреть отзывы"))
    bot.send_message(message.from_user.id, "Привет, это бот для подбора автомобиля. Начнём?", reply_markup=markup)


# обработка всех сообщений
@bot.message_handler(content_types='text')
def message_reply(message):
    global current_char

    global is_review
    global cur_rate
    global cur_review
    global is_naming
    global cur_name

    global speed
    global cheap
    global patency
    global capacity

    if message.text == "Посмотреть отзывы":
        con = sqlite3.connect("db/reviews_db.db")
        cur = con.cursor()
        request = "SELECT * FROM reviews"
        result = cur.execute(request).fetchall()
        if len(result) == 0:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("Да, начнём"))
            markup.add(types.KeyboardButton("Посмотреть отзывы"))
            bot.send_message(message.from_user.id, "Отзывов пока нет. Начнём?", reply_markup=markup)
        else:
            for i in range(len(result)):
                bot.send_message(message.from_user.id, result[i][1] + '\nИмя: ' + result[i][0] + '\n' + result[i][2])
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("Да, начнём"))
            markup.add(types.KeyboardButton("Посмотреть отзывы"))
            bot.send_message(message.from_user.id, "Больше отзывов нет. Начнём?", reply_markup=markup)
    elif message.text == "Хороший выбор, спасибо!":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Оставлю"))
        markup.add(types.KeyboardButton("Не буду оставлять"))
        bot.send_message(message.chat.id, "Не за что, обращайтесь!")
        bot.send_message(message.chat.id, "Хотите оставить отзыва о работе бота?", reply_markup=markup)
    elif message.text == "Оставлю":
        cur_rate = "0"
        is_review = 0
        is_naming = 0
        cur_review = ""
        cur_name = ""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("★★★★★"))
        markup.add(types.KeyboardButton("★★★★"))
        markup.add(types.KeyboardButton("★★★"))
        markup.add(types.KeyboardButton("★★"))
        markup.add(types.KeyboardButton("★"))
        bot.send_message(message.chat.id, "На сколько вы оцените работу бота?", reply_markup=markup)
    elif message.text == "Не буду оставлять":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("/start"))
        bot.send_message(message.chat.id, "Как знаете. Удачи", reply_markup=markup)
    elif "★" in message.text:
        cur_rate = message.text
        bot.send_message(message.chat.id, "Напишите пару слов в качестве отзыва...", reply_markup=None)
        is_review = 1
    elif message.text == "Не подходит":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Хочу"))
        markup.add(types.KeyboardButton("Нет, спасибо"))
        bot.send_message(message.chat.id, "Очень жаль. Хотите пройти опрос заново?", reply_markup=markup)
    elif message.text == "Хочу":
        current_char = 1
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Да"))
        markup.add(types.KeyboardButton("Нет"))
        bot.send_message(message.chat.id, "Должна ли твоя машина быть быстрой?", reply_markup=markup)
    elif message.text == "Нет, спасибо":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("/start"))
        bot.send_message(message.chat.id, "Как знаете. До встречи!", reply_markup=markup)
    elif message.text == "Да, начнём":
        current_char = 1
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Да"))
        markup.add(types.KeyboardButton("Нет"))
        bot.send_message(message.chat.id, "Должна ли твоя машина быть быстрой?", reply_markup=markup)
    elif message.text == "Да" and current_char != 0 and current_char != 5:
        if current_char == 1:
            speed = 1
            current_char = 2
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("Да"))
            markup.add(types.KeyboardButton("Нет"))
            bot.send_message(message.chat.id, "Должна ли твоя машина быть дешевой?", reply_markup=markup)
        elif current_char == 2:
            cheap = 1
            current_char = 3
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("Да"))
            markup.add(types.KeyboardButton("Нет"))
            bot.send_message(message.chat.id, "Должна ли твоя машина быть проходимой?", reply_markup=markup)
        elif current_char == 3:
            patency = 1
            current_char = 4
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("Да"))
            markup.add(types.KeyboardButton("Нет"))
            bot.send_message(message.chat.id, "Должна ли твоя машина быть вместительной?", reply_markup=markup)
        elif current_char == 4:
            capacity = 1
            current_char = 5
            find_car(message)
    elif message.text == "Нет" and current_char != 0 and current_char != 6:
        if current_char == 1:
            speed = 0
            current_char = 2
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("Да"))
            markup.add(types.KeyboardButton("Нет"))
            bot.send_message(message.chat.id, "Должна ли твоя машина быть дешевой?", reply_markup=markup)
        elif current_char == 2:
            cheap = 0
            current_char = 3
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("Да"))
            markup.add(types.KeyboardButton("Нет"))
            bot.send_message(message.chat.id, "Должна ли твоя машина быть проходимой?", reply_markup=markup)
        elif current_char == 3:
            patency = 0
            current_char = 4
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("Да"))
            markup.add(types.KeyboardButton("Нет"))
            bot.send_message(message.chat.id, "Должна ли твоя машина быть вместительной?", reply_markup=markup)
        elif current_char == 4:
            capacity = 0
            current_char = 5
            find_car(message)
    else:
        if is_review == 1:
            cur_review = message.text
            is_review = 0
            bot.send_message(message.chat.id, "Спасибо за написание! Как вас называть?")
            is_naming = 1
        elif is_naming == 1:
            cur_name = message.text
            is_naming = 0
            con = sqlite3.connect("db/reviews_db.db")
            cur = con.cursor()
            request = "INSERT INTO reviews VALUES(\'" + cur_name + "\', \'" + cur_rate + "\', \'" + cur_review + "\')"
            cur.execute(request)
            con.commit()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("/start"))
            bot.send_message(message.chat.id, "Спасибо за составление отзыва!", reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("/start"))
            bot.send_message(message.chat.id, "Не понимаю. Напиши /start для начала!", reply_markup=markup)


# функция поиска машины
def find_car(message):
    con = sqlite3.connect("db/cars_db.db")
    cur = con.cursor()
    request = "SELECT name FROM cars WHERE speed = " + str(speed) + " and cheap = " + str(cheap) + " and patency = " + \
              str(patency) + " and capacity = " + str(capacity)
    result = str(cur.execute(request).fetchall()[0][0])
    if result == "400":
        str_result = "Москвич 400"
    elif result == "20":
        str_result = "ГАЗ М-20 Победа"
    elif result == "69":
        str_result = "ГАЗ 69"
    elif result == "131":
        str_result = "ЗИЛ 131"
    elif result == "1111":
        str_result = "ВАЗ 1111 Ока"
    elif result == "1102":
        str_result = "ЗАЗ 1102 Таврия"
    elif result == "965":
        str_result = "ЗАЗ 965 Запорожец"
    elif result == "969":
        str_result = "ЛУАЗ 969"
    elif result == "kalina":
        str_result = "Лада Калина"
    elif result == "2111":
        str_result = "ВАЗ 2111"
    elif result == "2121":
        str_result = "ВАЗ 2121 Нива"
    elif result == "patriot":
        str_result = "УАЗ Патриот"
    elif result == "moto":
        str_result = "мотоцикл"
    elif result == "2104":
        str_result = "ВАЗ 2104"
    elif result == "968m":
        str_result = "ЗАЗ 968М"
    elif result == "buch":
        str_result = "УАЗ Буханка"
    else:
        str_result = ""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Хороший выбор, спасибо!"))
    markup.add(types.KeyboardButton("Не подходит"))
    img = open('images/' + result + ".jpg", 'rb')
    if str_result != "мотоцикл":
        bot.send_message(message.chat.id, "Подходящая тебе машина - " + str_result, reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Тебе подойдёт отечественный мотоцикл, например ИЖ Юпитер",
                         reply_markup=markup)
    bot.send_photo(message.chat.id, img)


bot.polling(none_stop=True, interval=0)
