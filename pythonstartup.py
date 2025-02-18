import telebot

TOKEN = "7630766994:AAFa-qhqQQSxusisT4vigSragfTQEuWju1A"
bot = telebot.TeleBot(TOKEN)

# Admin ID-ləri
ADMINS = {7712175966, 7793638111, 7970632951, 6489771542}

# Ad və nömrələr bazası
contacts = {
    "Miri": "+994557770809",
    "Sobranie": "+994515443140",
    "Nur": "+994554329899",
    "Qasimov": "+994503204026",
    "Elvin": "+994516421851",
    "Kutsal": "+994702225440",
    "Fizi": "+994553123383",
    "Hikmet": "+79921842839",
    "Qaqli": "+994509785451",
    "Azer019": "+994553073703",
    "Cedrik": "+994519248311",
    "Xubi": "+994103184062",
    "Balaca": "+994707448888",
    "Aurlucis": "+994703054909",
    "Mexnoch": "+994516731438",
    "Xech": "+994705414251",
    "Batweos": "+994515645859",
    "Turan(Recoveries)": "+994555969932",
    "Hertor": "+994559366367"
}

# `/start` - Adminlərə tam komut siyahısı, admin olmayanlara ödəniş mesajı
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.id in ADMINS:
        name = message.from_user.first_name
        welcome_msg = f"Xoş gəldin, {name}! Komutlarım:\n\n" \
                      "/number [ad] - Şəxsin nömrəsini göstərər.\n" \
                      "/add [ad] [nömrə] - Yeni şəxs əlavə edər.\n" \
                      "/delete [ad] - Şəxsi silər.\n" \
                      "/list - Bütün adları göstərər.\n" \
                      "/elaqe - Əlaqə məlumatı göstərər (admin olmayanlar üçündür)."
        bot.reply_to(message, welcome_msg)
    else:
        bot.reply_to(message, "Salam, botdan sadəcə adminlər istifadə edə bilər. Admin siyahısına daxil olmaq ödənişlidir. Daha çox məlumat üçün: @lostorj")

# `/number` - Kiçik və böyük hərf fərqi olmadan axtarış
@bot.message_handler(commands=['number'])
def send_number(message):
    if message.chat.id not in ADMINS:
        bot.reply_to(message, "Peysər, bot sənin üçün deyil.")
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "Zəhmət olmasa bir ad daxil edin: `/number [ad]`")
        return

    name = args[1].strip().lower()
    match = next((key for key in contacts.keys() if key.lower() == name), None)

    if match:
        bot.reply_to(message, f"{match} - {contacts[match]}")
    else:
        bot.reply_to(message, "Bu adda məlumat tapılmadı.")

# `/list` - Adları göstərir
@bot.message_handler(commands=['list'])
def send_list(message):
    if message.chat.id not in ADMINS:
        bot.reply_to(message, "Peysər, bot sənin üçün deyil.")
        return

    contact_list = "\n".join([f"<code>{name}</code>" for name in contacts.keys()])
    bot.send_message(message.chat.id, "Adlar siyahısı:", parse_mode='HTML')
    bot.send_message(message.chat.id, contact_list, parse_mode='HTML')

# `/add` - Yeni ad və nömrə əlavə etmək
@bot.message_handler(commands=['add'])
def add_contact(message):
    if message.chat.id not in ADMINS:
        bot.reply_to(message, "Peysər, bot sənin üçün deyil.")
        return

    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        bot.reply_to(message, "Zəhmət olmasa doğru formatda daxil edin: `/add [ad] [nömrə]`")
        return

    name = args[1].strip()
    number = args[2].strip()

    if name in contacts:
        bot.reply_to(message, f"{name} artıq siyahıda var.")
        return

    contacts[name] = number
    bot.reply_to(message, f"{name} uğurla əlavə olundu.")

# `/delete` - Adı siyahıdan və /number nəticəsindən silmək
@bot.message_handler(commands=['delete'])
def delete_contact(message):
    if message.chat.id not in ADMINS:
        bot.reply_to(message, "Peysər, bot sənin üçün deyil.")
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "Zəhmət olmasa bir ad daxil edin: `/delete [ad]`")
        return

    name = args[1].strip().lower()
    match = next((key for key in contacts.keys() if key.lower() == name), None)

    if match:
        del contacts[match]
        bot.reply_to(message, f"{match} uğurla silindi.")
    else:
        bot.reply_to(message, "Bu adda məlumat tapılmadı.")

# `/elaqe` - Yalnız admin olmayanlar istifadə edə bilər
@bot.message_handler(commands=['elaqe'])
def contact_info(message):
    if message.chat.id in ADMINS:
        bot.reply_to(message, "Bu komut sadəcə admin olmayanlar üçündür.")
        return

    bot.reply_to(message, "@LostOrj")

# Admin olmayan şəxslər üçün bloklama mesajı
@bot.message_handler(func=lambda message: message.chat.id not in ADMINS)
def block_users(message):
    bot.reply_to(message, "Peysər, bot sənin üçün deyil.")

# Botu işə salırıq
bot.polling()