import telebot
from telebot import types
from telebot import TeleBot

TOKEN = input("Введите токен вашего бота: ")

bot = TeleBot(TOKEN)

 
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Посмотреть расписание экзаменов')
    btn2 = types.KeyboardButton('Посмотреть вопросы к экзамену')
    markup.row(btn1, btn2)
    btn3 = types.KeyboardButton('Получить материалы для подготовки')
    markup.row(btn3)
    bot.send_message(message.chat.id, 'Привет! Я бот, который собрал всё что касается твоих экзаменов в одном месте. Выбирай нужную опцию!', reply_markup=markup)
   
@bot.message_handler(func=lambda message: message.text == 'Получить материалы для подготовки')
def show_preparation_materials(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('ТОЭ', callback_data='материалы_ТОЭ')
    btn2 = types.InlineKeyboardButton('Дискретная математика', callback_data='материалы_ДМиТИ')
    btn3 = types.InlineKeyboardButton('Алгоритмы и структуры данных', callback_data='материалы_АиСД')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, 'Выберите предмет для получения материалов:', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('материалы'))
def handle_material_selection(call):
    subject = call.data.split('_')[1]  # Получаем название предмета
    markup = types.InlineKeyboardMarkup()

    # Создаем кнопки для выбора конкретных материалов
    if subject == 'ТОЭ':
        btn1 = types.InlineKeyboardButton('Лекции', url='https://drive.google.com/drive/folders/1cgY-EH2i6w-6s9T8nr2S2pCtidBsKgaD?usp=drive_link')
        btn2 = types.InlineKeyboardButton('Примеры решения задач', callback_data='ТОЭ_примеры')
        btn3 = types.InlineKeyboardButton('Перейти на курс LETITEACH', url='https://open.eltech.ru/courses/course-v1:kafedra-teoreticheskih-osnov-elektrotehniki+TOE-101+fall_2024/courseware/cbe0b05726ec455ca5c10dd292d77dd1/5557fae349e645a3ad72af6e3ef525c7/1?activate_block_id=block-v1%3Akafedra-teoreticheskih-osnov-elektrotehniki%2BTOE-101%2Bfall_2024%2Btype%40html%2Bblock%406f87b5eb69d74941aa71af3ee316229c')
        btn4 = types.InlineKeyboardButton('Литература', callback_data='ТОЭ_литература')
        markup.row(btn1, btn2)
        markup.add(btn3, btn4)
        
    elif subject == 'ДМиТИ':
        btn5 = types.InlineKeyboardButton('Лекции', url='https://drive.google.com/drive/folders/1-DXbYCzAZ52LFsXcAE9otR2vYsuRahFx?usp=drive_link')
        btn6 = types.InlineKeyboardButton('Литература', callback_data='ДМиТИ_литература')
        markup.row(btn5, btn6)

    elif subject == 'АиСД':
        btn7 = types.InlineKeyboardButton('Лекции', url='https://drive.google.com/drive/folders/1-EZ-LKZRFW7elCr4qbRhZ126pw8Wl7sp?usp=drive_link')
        btn8 = types.InlineKeyboardButton('Литература', callback_data='АиСД_литература')
        markup.row(btn7, btn8)

    bot.send_message(call.message.chat.id, 'Выберите нужные материалы:', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'ТОЭ_примеры')
def handle_toe_examples(call):
    bot.send_message(call.message.chat.id, "Вот файл с примерами решения задач:")
    bot.send_document(call.message.chat.id, open('TOEtasks.pdf', 'rb'))  # Путь к вашему PDF-файлу 

@bot.callback_query_handler(func=lambda call: call.data.endswith('литература'))
def handle_literature_selection(call):
    subject = call.data.split('_')[0]  # Получаем предмет
    if subject == 'ТОЭ':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Учебник', callback_data='ТОЭ_учебник')
        btn2 = types.InlineKeyboardButton('Задачник', callback_data='ТОЭ_задачник')
        markup.add(btn1, btn2)
        bot.send_message(call.message.chat.id, 'Выберите тип литературы:', reply_markup=markup)
    elif subject == 'ДМиТИ':
        bot.send_message(call.message.chat.id, "Вот учебник по Дискретной математике:") 
        bot.send_document(call.message.chat.id, open('DMITIbook.pdf', 'rb'))
    elif subject == 'АиСД':
        bot.send_message(call.message.chat.id, "Вот учебник по Алгоритмам и структурам данных") 
        bot.send_document(call.message.chat.id, open('cormen.pdf', 'rb'))

@bot.callback_query_handler(func=lambda call: call.data.startswith('ТОЭ_'))
def handle_toe_literature_selection(call):
    if call.data == 'ТОЭ_учебник':
        bot.send_message(call.message.chat.id, "Вот учебник по ТОЭ") 
        bot.send_document(call.message.chat.id, open('TOEbook.pdf', 'rb'))
    elif call.data == 'ТОЭ_задачник':
        bot.send_message(call.message.chat.id, "Вот задачник по ТОЭ")  
        bot.send_document(call.message.chat.id, open('TOEtasksbook.pdf', 'rb'))
   
@bot.message_handler(func=lambda message: message.text == 'Посмотреть вопросы к экзамену')
def show_subjects(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('ТОЭ', callback_data='ТОЭ')
    btn2 = types.InlineKeyboardButton('Дискретная математика', callback_data='Дискретная математика')
    btn3 = types.InlineKeyboardButton('Алгоритмы и структуры данных', callback_data='Алгоритмы и структуры данных')
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    bot.send_message(message.chat.id, 'Выберите предмет:', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_subject_selection(call):
    subject = call.data  # Получаем данные из кнопки
    subject_photos = {
        'ТОЭ': 'TOEquestions.jpg',
        'Дискретная математика': 'DMITIquestions.jpg',
        'Алгоритмы и структуры данных': 'AISDquestions.jpg'
    }

    if subject in subject_photos:
        photo_path = subject_photos[subject]
        with open(photo_path, 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo)
            bot.send_message(call.message.chat.id, f'Экзаменационные вопросы к предмету: {subject}.')
    else:
        bot.send_message(call.message.chat.id, 'Не удалось найти вопросы для этого предмета.')
    
 
@bot.message_handler(func=lambda message: message.text == 'Посмотреть расписание экзаменов')
def show_exam_schedule(message):
    exam_schedule_text = (
        "Вот расписание экзаменов:\n"
        "1. ТОЭ - 14 января, 10:00\n"
        "2. Дискретная математика - 18 января (время пока неизвестно)\n"
        "3. Алгоритмы и структуры данных - 24 января (время пока неизвестно)\n"
    )
    bot.send_message(message.chat.id, exam_schedule_text)    

bot.polling(none_stop=True)