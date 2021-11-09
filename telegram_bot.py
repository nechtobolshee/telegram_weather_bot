import requests
import datetime
from pprint import pprint
from config import weather_token, bot_token
from aiogram import Bot, types, Dispatcher, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

bot = Bot(token=bot_token)
disp = Dispatcher(bot)


# ---- Hello func ----
@disp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    btn_developer = KeyboardButton('Developer?')
    btn_settings = KeyboardButton(f'How to use \U0001F6E0')
    start_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_developer, btn_settings)
    await bot.send_message(message.from_user.id, "Привет, {0.first_name}! \U0001F60E "
                                                 "\nДля того чтобы узнать сводку погоды в конкретном "
                                                 "городе - напиши название города в этот чат."
                                                 "\nТак-же, для удобства, можете написать названия "
                                                 "городов через запятую и я добавлю их в быстрый доступ! "
                                                 "\U0001F642".format(message.from_user), reply_markup=start_menu)


# ---- Main func ----
@disp.message_handler()
async def choose_city(message: types.Message):

    if ',' in message.text:
        city_for_choose = message.text
        lst = list(set(city_for_choose.lower().replace(',', ' ').split()))
        lst = [i.capitalize() for i in lst]
        btn_developer = KeyboardButton('Developer?')
        btn_settings = KeyboardButton('How to use \U0001F6E0')
        btn_clear = KeyboardButton('Clear')
        main_menu = ReplyKeyboardMarkup(resize_keyboard=True)

        # ---- Menu settings ----
        for i in lst:
            btn_name = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={i}&appid={weather_token}&units=metric')
            read = btn_name.json()
            pprint(read)
            if read['cod'] == 200:
                btn_cites = KeyboardButton(f'{i}')
                main_menu.add(btn_cites)
        await bot.send_message(message.from_user.id, "Успешно добавили города! :)",
                               reply_markup=main_menu.add(btn_developer, btn_settings, btn_clear))

    elif 'How to use \U0001F6E0' in message.text:
        await message.reply("\U0001F6E0 Чтобы узнать сводку погоды в конкретном городе - напишите название города в этот чат."
                            "\n\U0001F6E0 Для корректного отображения информации введите правильное название города."
                            "\n\U0001F6E0 Для удобства можете написать названия городов через запятую и я добавлю их в быстрый доступ!"
                            "\n\U0001F6E0 Чтобы изменить города в меню быстрого доступа - напишите заново названия городов через запятую."
                            "\n\U0001F6E0 Если город написан с ошибкой в имени - он не будет добавлен в быстрый доступ.")

    elif 'Developer?' in message.text:
        await message.reply('Разработчик бота - @nechtobolshee.\nПисать по идеям для улучшения.\n')

    elif 'Clear' in message.text:
        btn_developer = KeyboardButton('Developer?')
        btn_settings = KeyboardButton('How to use \U0001F6E0')
        main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
        await message.reply('Панель быстрого доступа очищена :)', reply_markup=main_menu.add(btn_developer, btn_settings))
    else:
        try:
            r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={weather_token}&units=metric')
            data = r.json()
            pprint(data)
            city = data['name']
            country = data['sys']['country']
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            weather = data['weather'][0]['description']
            sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])

            await message.reply(f'\U0001F550 {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")} \U0001F550'
                                f'\nГород: {city}, {country}\nТемпература: {temp}°C'
                                f'\nВлажность: {humidity}%\nПогода: {weather}\nВремя заката: {sunset}'
                                f'\nHave a good day! \U0001F607')

        except:
            await message.reply("\U00002620 Проверьте правильность написания \U00002620")


if __name__ == '__main__':
    executor.start_polling(disp, skip_updates=True)
