from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.types.input_file import FSInputFile
from aiogram.filters import CommandStart, Command

import keyboards as kb
import commands as cm


router = Router()


@router.message(CommandStart())
async def start(message: Message):
    cm.upsert_report('start')
    
    await message.answer('Привет, привет! Рада тебя видеть здесь!😇🩵\n\nЕжедневно наши специалисты обрабатывают множество заявок, поэтому я здесь, чтобы помочь Вам быстрее найти ответы на свои вопросы ☺️\n\nСнизу вы найдете меню. Выберите тему и начнем! 👍', reply_markup=kb.helper)
    

@router.message(F.text == 'Отмена')
async def cancel_action(message: Message):
    user = message.from_user.id
    cm.reset_state(user)
    await message.answer('Действие отменено', reply_markup=kb.helper)


@router.message(Command('help'))
async def reply_help(message: Message):
    await message.answer('Можешь выбрать одно из действий', reply_markup=kb.helper)


@router.message(F.photo)
async def handle_photo(message: Message):
    await message.answer('Я не могу просматривать картинки...\nЛучше выберите одно из действий', reply_markup=kb.helper)


### Как подключить домофон
@router.message(F.text == 'Как подключить умный домофон?')
async def connect_intercom(message: Message):
    cm.upsert_report('how_connect')
    
    await message.answer('Благодарю за интерес к моему дому, это хорошая инвестиция в свой комфорт 😊👍\n\nЧтобы подключить домофон, нужно заполнить заявку. Для этого нужно ответить на несколько вопросов. Готовы?', reply_markup=kb.inl_connection)


### О компании
@router.message(F.text == 'О компании')
async def connect_intercom(message: Message):
    cm.upsert_report('about_us')
    
    path_to_image = '/home/asan/MyProject/IntercomBot/photo/about_us.jpg'
    photo = FSInputFile(path_to_image)
    
    text = 'Интерком - это отечественная компания, которая предоставляет услуги Умной домофонии с 2023 года. ✨\n\nМы стремимся предоставить больше комфорта и безопасности жителям многоэтажных домов, устанавливая современные системы домофонов с видеонаблюдением и приложением. Таким образом мы делаем безопасными не только дома, но и город в целом. На данный момент наша база подключенных абонентов составляет более 2000 человек.\n\n🕒 График работы:\nонлайн с 9:00 до 20:00 (Пн - Пт)\nофис с 9:00 до 18:00 (Пн-Пт)\n\n📞 Колл-центр:\n0707888822\n0997888822\n\n📍 Адрес:\nул. Фрунзе, 533А (Бишкек)'
    await message.answer_photo(text, reply_markup=kb.inl_about_us, photo=photo)
    

### Кто такая Сию?
@router.message(F.text == 'Кто такая Сию?')
async def who_im(message: Message):
    cm.upsert_report('who_im')
    
    path_to_image = '/home/asan/MyProject/IntercomBot/photo/seeu.jpg'
    photo = FSInputFile(path_to_image)
    
    text = 'Сию - маскот компании Интерком. Это глазок камеры домофона. Сию в переводе с английского языка "See You" означает "Я тебя вижу". Персонаж охраняет жителей дома от посторонних, следит за порядком и заботится о системе.'
    await message.answer_photo(photo, text)


### Как подключить домофон
@router.message(F.text == 'Где можно купить новый ключ?')
async def where_ibuy(message: Message):
    cm.upsert_report('where_buy')
    
    text = 'Ключ можно преобрести у домкома или у нас в офисе.\n\nТелефоны для справок:\n0707888822\n0997888822\n\nГрафик работы:\n9:00 - 18:00 с Пн по Пт\n\nАдрес: ул.Фрунзе, 533а (Бишкек)'
    await message.answer(text, reply_markup=kb.inl_where_ibuy)


@router.callback_query(F.data == 'report')
async def handle_report(callback: CallbackQuery):
    user = callback.from_user.id
    cm.upsert_user_state(user, 1)

    await callback.answer('Спасибо за ваш интерес.')

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.bot.send_message(user, 'Как Вас зовут?', reply_markup=kb.cancel)


@router.message(lambda message: cm.get_user_state(message.from_user.id)[0] == 1)
async def handle_name(message: Message):
    user = message.from_user.id
    text = message.text

    cm.upsert_ticket(user, 'name', text)
    cm.upsert_user_state(user, 2)

    await message.answer('Напишите ваш адрес', reply_markup=kb.cancel)


@router.message(lambda message: cm.get_user_state(message.from_user.id)[0] == 2)
async def handle_address(message: Message):
    user = message.from_user.id
    text = message.text
    cm.upsert_ticket(user, 'address', text)
    cm.upsert_user_state(user, 3)

    await message.answer('В Вашем доме уже установлен домофон?', reply_markup=kb.inl_inter)


### Have u intercom
@router.callback_query(F.data == 'yes_we_have')
async def yes_we_have(callback: CallbackQuery):
    user = callback.from_user.id
    
    cm.upsert_ticket(user, 'inter_type', 'Да, установлен')
    cm.upsert_user_state(user, 4)

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.bot.send_message(user, 'Как с вами связаться?', reply_markup=kb.inl_connection_type)
    

@router.callback_query(F.data == 'no_we_havent')
async def no_we_havent(callback: CallbackQuery):
    user = callback.from_user.id
    
    cm.upsert_ticket(user, 'inter_type', 'Нет, не установлен')
    cm.upsert_user_state(user, 4)

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.bot.send_message(user, 'Как с вами связаться?', reply_markup=kb.inl_connection_type)
    

@router.callback_query(F.data == 'house')
async def house(callback: CallbackQuery):
    user = callback.from_user.id
    
    cm.upsert_ticket(user, 'inter_type', 'Частный дом')
    cm.upsert_user_state(user, 4)

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.bot.send_message(user, 'Как с вами связаться?', reply_markup=kb.inl_connection_type)


### Contact type
@router.callback_query(F.data == 'whats')
async def whats(callback: CallbackQuery):
    user = callback.from_user.id
    
    cm.upsert_ticket(user, 'callback_type', 'Написать в What\'s App')
    cm.upsert_user_state(user, 5)

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.bot.send_message(user, 'Напишите номер телефона.', reply_markup=kb.cancel)


@router.callback_query(F.data == 'mobile')
async def whats(callback: CallbackQuery):
    user = callback.from_user.id
    
    cm.upsert_ticket(user, 'callback_type', 'Позвонить')
    cm.upsert_user_state(user, 5)

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.bot.send_message(user, 'Напишите номер телефона.', reply_markup=kb.cancel)


@router.message(lambda message: cm.get_user_state(message.from_user.id)[0] == 5)
async def handle_phone(message: Message):
    user = message.from_user.id
    text = message.text
    cm.upsert_ticket(user, 'num', text)
    cm.upsert_user_state(user, 6)

    await message.answer('Напишите примечание - комментарий.', reply_markup=kb.cancel)


@router.message(lambda message: cm.get_user_state(message.from_user.id)[0] == 6)
async def handle_description(message: Message):
    user = message.from_user.id
    text = message.text
    cm.upsert_ticket(user, 'description', text)
    cm.reset_state(user)

    get_data = cm.get_ticket(user)
    date = message.date.today().strftime("%Y-%m-%d %H:%M")

    await message.bot.send_message(
        -1002009533675,
        f'Ответ пользователя @{message.from_user.username}. Время: {date}\
        \n\nВопрос: Как Вас зовут?🤗\nОтвет: {get_data[1]}\
        \n\nВопрос: На Вашем доме уже установлен домофон?\nОтвет: {get_data[6]}\
        \n\nВопрос: По какому адресу вы хотите установить домофон, либо подключиться к системе уже установленного домофона?\nОтвет: {get_data[2]}\
        \n\nВопрос: Выберите способ связи\nОтвет: {get_data[3]}\
        \n\nВопрос: Отправьте номер для связи 🙃\nОтвет: {get_data[5]}\
        \n\nВопрос: Напишите примечание - комментарий.\nОтвет: {get_data[4]}'
    )

    await message.answer('Ваше обращение было успешно отправлено! Сроки обработки заявки - 3 рабочих дня.\n\n\nСледите за нашим инстаграмом, чтобы не пропустить новостей! 🤩👌😉🩵', reply_markup=kb.helper)


### Расскажи, что умеет умный домофон
@router.message(F.text == 'Расскажи, что умеет умный домофон')
async def about_intercom(message: Message):
    cm.upsert_report('tell_about')
    
    path_to_image = '/home/asan/MyProject/IntercomBot/photo/1.jpg'
    photo = FSInputFile(path_to_image)
    
    text = 'Наш домофон работает в системе вместе с видеонаблюдением и приложением. Камеры устанавливаются во дворе, в подъезде, на парковке, на детской площадке и в любом другом месте по запросу жителей. 😉\n\nУ вас есть личный транспорт, дети, пожилые члены семьи или ценные вещи в доме?'

    await message.answer_photo(photo, text, reply_markup=kb.inl_about)


@router.callback_query(F.data == 'ihave')    
async def ihave(callback: CallbackQuery):
    user = callback.from_user.id
    path_to_image = '/home/asan/MyProject/IntercomBot/photo/2.jpg'
    photo = FSInputFile(path_to_image)
    
    text = 'Прямая трансляция со всех камер доступна через наше приложение. Вы в любой момент сможете убедиться в сохранности вашего транспорта, посмотреть, с кем играет ваш ребенок, и быть уверенными, что в случае неприятной ситуации у вас будет запись с камер. 👍\n\n‼️ Кстати, записи хранятся в облачном архиве 5 дней, а затем удаляются. Но если вы хотите сохранить записи, их можно с легкостью скачать на телефон. 💫'    

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.bot.send_photo(user, caption=text, reply_markup=kb.inl_letsgo, photo=photo)
    

@router.callback_query(F.data == 'gonext')
async def gonext(callback: CallbackQuery):
    user = callback.from_user.id
    
    text = 'Камера домофона оснащена датчиками, благодаря которым она может распознавать лица и отличать живых людей от фотографий. 😮\n\nКамера также обладает сверхсветочувствительной матрицей, что позволяет транслировать цветное изображение даже в ночное время суток. 😀👍\n\nМы живем в такое время, когда не страшно забыть кошелек с деньгами, ведь можно воспользоваться переводами, или забыть ключи, ведь дверь можно открыть по Face ID и не только.'
    
    await callback.message.edit_reply_markup(None)
    await callback.bot.send_message(user, caption=text, reply_markup=kb.inl_without)
    

@router.callback_query(F.data == 'without_key')
async def whats_this(callback: CallbackQuery):
    user = callback.from_user.id
    path_to_image = '/home/asan/MyProject/IntercomBot/photo/3.jpg'
    photo = FSInputFile(path_to_image)
    
    text = '✅ 3 способа открыть дверь без ключа:\n\n\n\n1. По функции распознавания лиц;\n2. Через онлайн ключ в приложении;\n3. Раздать временный доступ по ссылке.\n\n\nи секретный лайфхак от наших аббонентов💣:\n\n\nпозвонить себе с домофона и открыть дверь через телефон.'
    
    await callback.message.edit_reply_markup(None)
    await callback.bot.send_photo(user, caption=text, reply_markup=kb.inl_keys, photo=photo)
    

@router.callback_query(F.data == 'online_key')
async def whats_this(callback: CallbackQuery):
    user = callback.from_user.id
    path_to_image = '/home/asan/MyProject/IntercomBot/photo/4.jpg'
    photo = FSInputFile(path_to_image)
    
    text = '🔑 Онлайн-ключ — это возможность открывать дверь кнопкой в приложении.'
    
    await callback.message.edit_reply_markup(None)
    await callback.bot.send_photo(user, caption=text, reply_markup=kb.inl_keys_ex, photo=photo)


@router.callback_query(F.data == 'time_key')
async def time_key(callback: CallbackQuery):
    user = callback.from_user.id
    path_to_image = '/home/asan/MyProject/IntercomBot/photo/4.jpg'
    photo = FSInputFile(path_to_image)
    
    text = '🕐 Временный доступ — это возможность отправлять доступ друзьям и близким. Вы можете поделиться ссылкой в любой соцсети (WhatsApp, Instagram, Telegram и т. д.). Вашим гостям нужно будет лишь перейти по ссылке и открыть дверь. Удобно, когда ждете гостей и не хотите отвлекаться на дверь.\n\nВременный доступ можно настроить на 2, 4, 8, 12 или 24 часа.'
    
    await callback.message.edit_reply_markup(None)
    await callback.bot.send_photo(user, caption=text, reply_markup=kb.inl_keys_ex, photo=photo)


@router.callback_query(F.data == 'keys_ex')
async def keys_ex(callback: CallbackQuery):
    user = callback.from_user.id
    path_to_image = '/home/asan/MyProject/IntercomBot/photo/5.jpg'
    photo = FSInputFile(path_to_image)
    
    text = 'Конечно, есть! Для любителей традиционных домофонов и материалистов у нас есть некопируемые ключи. Ключи имеют свой личный идентификационный номер и защищены системой шифрования. Их не так просто скопировать в подземке, что усложняет доступ в подъезд посторонним. 😌'
    
    await callback.message.edit_reply_markup(None)
    await callback.bot.send_photo(user, caption=text, reply_markup=kb.inl_how_work, photo=photo)
    

@router.callback_query(F.data == 'how_work')
async def how_work(callback: CallbackQuery):
    user = callback.from_user.id
    
    text = 'Отличный вопрос! Давайте представим, что вы подключены к системе и к вам пришел гость😧. Он набирает номер квартиры на вашем домофоне и ждет ответа. Звонок поступает на ваш телефон в виде видеозвонка. В это время вы нянчитесь с маленьким малышом или готовите обед (а может и то, и другое вместе). Все, что вам нужно сделать, — это принять вызов. Далее вы можете увидеть, поговорить, а затем решить, впустить гостя или нет. 🤗👍\n\nБолее того, звонки можно принимать, даже если вас нет дома и даже если вы находитесь в другой стране. Удобно?😏'
    
    await callback.message.edit_reply_markup(None)
    await callback.bot.send_message(user, caption=text, reply_markup=kb.inl_what_if)
    
    
@router.callback_query(F.data == 'good')
async def good(callback: CallbackQuery):
    user = callback.from_user.id
    
    text = 'В случае неисправности домофона вам не нужно будет беспокоиться и искать техника, который сможет его починить. Достаточно сообщить нам о проблеме, мы проведем диагностику и приведем домофон в исправное состояние😉. В случае поломки по естественным причинам мы заменим его бесплатно.'
    
    await callback.message.edit_reply_markup(None)
    await callback.bot.send_message(user, caption=text, reply_markup=kb.inl_how_much)
    

@router.callback_query(F.data == 'how_much')
async def how_much(callback: CallbackQuery):
    user = callback.from_user.id
    
    text = 'А сейчас я предлагаю Вам посетить наш сайт и ознакомиться с тарифами нашей компании. Очень надеюсь, что информация была полезной! 🥰🤗⬇️'
    
    await callback.message.edit_reply_markup(None)
    await callback.bot.send_message(user, text, reply_markup=kb.inl_find_money)
    

### У меня не работает
@router.message(F.text == 'У меня не работает...')
async def not_work(message: Message):
    text = 'Очень жаль, что Вам пришлось столкнуться с трудностями. Надеюсь я смогу Вам помочь 🥺🤗🩵\n\nДавайте разбираться! В меню снизу выберите подходящий раздел. ⬇️'
    await message.answer(text, reply_markup=kb.not_work)


@router.message(F.text == 'Назад')
async def back(message: Message):
    text = 'Главное меню'
    await message.answer(text, reply_markup=kb.helper)


### У меня не работает распознавание
@router.message(F.text == 'У меня не работает распознавание')
async def not_work(message: Message):
    cm.upsert_report('dwork_face')
    
    text = 'Прежде чем мы пойдем дальше, ознакомьтесь с возможными причинами и нашей памяткой с советами. 🤗⬇️\n\nНестабильный или слабый интернет может повлиять на работу домофона, поскольку он функционирует через сеть.\n\nЧтобы функция распознавания лиц работала лучше, рекомендуем загрузить в приложение несколько фотографий. Убедитесь, что фото сделано при хорошем освещении, без помех и аксессуаров.'
    await message.answer(text, reply_markup=kb.inl_im_read)
    

@router.callback_query(F.data == 'im_read')
async def im_read(callback: CallbackQuery):
    user = callback.from_user.id
    
    text = 'Если эта памятка Вам не подошла, давайте заполним заявку, чтобы специалисты быстрее обработали запрос и решили проблему 🤗\n\nЭто не займет много времени, вам лишь нужно ответить на несколько вопросов...\n\nОтправляйте ответы одним сообщением на каждый вопрос. Ваши ответы я заношу в заявку. 🤗'
    
    await callback.message.edit_reply_markup(None)
    await callback.bot.send_message(user, text, reply_markup=kb.inl_im_understood)


### Не получается войти в приложение
@router.message(F.text == 'Не получается войти в приложение')
async def dnot_cannot_enter(message: Message):
    cm.upsert_report('cannot_ent')
    
    text = 'Прежде чем мы пойдем дальше, ознакомьтесь с возможными причинами и нашей памяткой с советами 🤗⬇️\n1. Если сейчас начало месяца, убедитесь, что на балансе достаточно средств. Даже если не хватает 1 тыйына, система не спишет оплату за домофон.\n\n2. Надеюсь, что вы проверили правильность правильность ввода пароля и логина.'
    await message.answer(text, reply_markup=kb.inl_im_read)
    

@router.callback_query(F.data == 'im_read_app')
async def im_read_app(callback: CallbackQuery):
    user = callback.from_user.id
    
    text = 'Вам нужно получить пароль и логин от наших специалистов. Давайте заполним небольшую анкету, чтобы они смогли с вами связаться и выслать все необходимые данные.\n\nЭто не займет много времени, вам лишь нужно ответить на несколько вопросов..Отправляйте ответы одним сообщением на каждый вопрос. Ваши ответы я заношу в заявку. 🤗'
    
    await callback.message.edit_reply_markup(None)
    await callback.bot.send_message(user, text, reply_markup=kb.inl_im_understood)


### Не работают камеры
@router.message(F.text == 'Не работают камеры')
async def dnot_work_cameras(message: Message):
    cm.upsert_report('dwork_camera')
    
    text = '‼️ Камеры видеонаблюдения доступны только по тарифу "домофон 200". Если у Вас именно этот тариф, но камеры не отображаются в приложении или не работают, давайте попробуем разобраться в возможных причинах.\n\nДля этого нам нужно заполнить заявку. Это не займет много времени, вам лишь нужно ответить на несколько вопросов.. Пожалуйста, отправляйте ответы одним сообщением на каждый вопрос. Ваши ответы я заношу в заявку. 🤗'
    await message.answer(text, reply_markup=kb.inl_im_understood)
    
    
### Приложение не работает
@router.message(F.text == 'Приложение не работает')
async def dnot_work_app(message: Message):
    cm.upsert_report('dwork_app')
    
    text = 'Прежде чем мы пойдем дальше, ознакомьтесь с возможными причинами и нашей памяткой с советами 🤗⬇️\n\n1. Включенный VPN. Приложение НЕ РАБОТАЕТ при включенном VPN. Это может быть причиной, по которой к вам не поступают звонки и уведомления. Поэтому обязательно убедитесь, что VPN отключен.\n\n2. Запрет на уведомления. Любое приложение, которое вы устанавливаете на телефон запрашивает пакет разрешений. Убедитесь, что настройках телефона включены все необходимые разрешения для приложения Intercom.\n\n3. Если сейчас начало месяца, убедитесь, что на балансе достаточно средств. Даже если не хватает 1 тыйына, система не спишет оплату за домофон.'
    await message.answer(text, reply_markup=kb.inl_app_dnot)
    

@router.callback_query(F.data == 'im_app_dnot')
async def im_app_dnot(callback: CallbackQuery):
    user = callback.from_user.id
    
    text = 'Если эта памятка Вам не подошла, давайте заполним заявку, чтобы специалисты быстрее обработали запрос и решили проблему 🤗\n\nЭто не займет много времени, вам лишь нужно ответить на несколько вопросов...\nПожалуйста, отправляйте ответы одним сообщением на каждый вопрос. Ваши ответы я заношу в заявку.'
    
    await callback.message.edit_reply_markup(None)
    await callback.bot.send_message(user, text, reply_markup=kb.inl_im_understood)
    

### Другое
@router.message(F.text == 'Другое')
async def another(message: Message):
    cm.upsert_report('another')
    
    text = 'Если вам не подошел ни один из предложенных разделов, вам поможет только специалист. Давайте заполним заявку, чтобы ваш запрос быстрее обработали.\n\nЯ задам несколько вопросов, на каждый вопрос нужно отвечать одним сообщением. Все данные я заношу в заявку. 🤗\n\nНачнем?'
    await message.answer(text, reply_markup=kb.inl_start)
    
    
@router.callback_query(F.data == 'report_w')
async def handle_report(callback: CallbackQuery):
    user = callback.from_user.id
    cm.upsert_user_state(user, 10)

    await callback.answer('Спасибо за ваш интерес.')

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.bot.send_message(user, 'Как Вас зовут?', reply_markup=kb.cancel)


@router.message(lambda message: cm.get_user_state(message.from_user.id)[0] == 10)
async def handle_name(message: Message):
    user = message.from_user.id
    text = message.text

    cm.upsert_ticket(user, 'name', text)
    cm.upsert_user_state(user, 20)

    await message.answer('Напишите ваш адрес', reply_markup=kb.cancel)


@router.message(lambda message: cm.get_user_state(message.from_user.id)[0] == 20)
async def handle_address(message: Message):
    user = message.from_user.id
    text = message.text
    cm.upsert_ticket(user, 'address', text)
    cm.upsert_user_state(user, 3)

    await message.answer('Как с вами связаться?', reply_markup=kb.inl_connection_type)


### Contact type
@router.callback_query(F.data == 'whats')
async def whats(callback: CallbackQuery):
    user = callback.from_user.id
    
    cm.upsert_ticket(user, 'callback_type', 'Написать в What\'s App')
    cm.upsert_user_state(user, 50)

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.bot.send_message(user, 'Напишите номер телефона.', reply_markup=kb.cancel)


@router.callback_query(F.data == 'mobile')
async def whats(callback: CallbackQuery):
    user = callback.from_user.id
    
    cm.upsert_ticket(user, 'callback_type', 'Позвонить')
    cm.upsert_user_state(user, 50)

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.bot.send_message(user, 'Напишите номер телефона.', reply_markup=kb.cancel)


@router.message(lambda message: cm.get_user_state(message.from_user.id)[0] == 50)
async def handle_phone(message: Message):
    user = message.from_user.id
    text = message.text
    cm.upsert_ticket(user, 'num', text)
    cm.upsert_user_state(user, 60)

    await message.answer('Напишите примечание - комментарий. (Можете написать предложения и пожелания, или трудности с которыми вы стокнулись, чтобы мы могли вам помочь)', reply_markup=kb.cancel)


@router.message(lambda message: cm.get_user_state(message.from_user.id)[0] == 60)
async def handle_description(message: Message):
    user = message.from_user.id
    text = message.text
    cm.upsert_ticket(user, 'description', text)
    cm.reset_state(user)

    get_data = cm.get_ticket(user)
    date = message.date.today().strftime("%Y-%m-%d %H:%M")

    await message.bot.send_message(
        -1002009533675,
        f'Ответ пользователя @{message.from_user.username}. Время: {date}\
        \n\nВопрос: Как Вас зовут?\nОтвет: {get_data[1]}\
        \n\nВопрос: По какому адресу вы хотите установить домофон, либо подключиться к системе уже установленного домофона?\nОтвет: {get_data[2]}\
        \n\nВопрос: Выберите способ связи\nОтвет: {get_data[3]}\
        \n\nВопрос: Отправьте номер для связи\nОтвет: {get_data[5]}\
        \n\nВопрос: Напишите примечание - комментарий. (Можете написать предложения и пожелания, или трудности с которыми вы стокнулись, чтобы мы могли вам помочь)\nОтвет: {get_data[4]}'
    )

    await message.answer('Ваше обращение было успешно отправлено! Сроки обработки заявки - 3 рабочих дня.\n\n\nСледите за нашим инстаграмом, чтобы не пропустить новостей! 🤩👌😉🩵', reply_markup=kb.helper)
    

@router.message(Command('report_about'))
async def report_about(message: Message):
    rep = cm.report_about_report()
    text = f'Start: {rep[0][0]}\nКак подключить умный домофон?: {rep[0][1]}\nРасскажи, что умеет умный домофон: {rep[0][2]}\
             \nГде можно купить новый ключ?: {rep[0][3]}\nКто такая Сию?: {rep[0][4]}\nО компании: {rep[0][5]}\
             \nУ меня не работает распознавание: {rep[0][6]}\nНе получается войти в приложение: {rep[0][7]}\
             \nНе работают камеры: {rep[0][8]}\nПриложение не работает: {rep[0][9]}\nДругое: {rep[0][10]}'
    
    await message.answer(text, reply_markup=kb.helper)