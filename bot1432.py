cd ~
rm bot143.py
cat > bot143.py << 'EOF'
import telebot, json, os
from telebot import types
TOKEN = "8992497642:AAHahvPHC1NkkNiPYVPdghByI1FugP_aAxw"
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = 6688173154
CHANNELS = [
    {"id": "@mmmsleaker", "name": "Mmm Sleaker", "link": "https://t.me/mmmsleaker"},
    {"id": -1003527575059, "name": "RAVI PRIVATE", "link": "https://t.me/+eV5sgLcYBuE1MDI1"},
    {"id": -1004359222295, "name": "Pankaj X Private", "link": "https://t.me/+3lS1Yc_jbAwzMzhl"}
]
DB_FILE = "database.json"
if os.path.exists(DB_FILE):
    with open(DB_FILE, "r") as f:
        UPLOADS = json.load(f)
else:
    UPLOADS = {}
def save_db():
    with open(DB_FILE, "w") as f:
        json.dump(UPLOADS, f)
def get_next_code():
    if not UPLOADS:
        return "v1"
    nums = [int(k[1:]) for k in UPLOADS.keys() if k.startswith("v") and k[1:].isdigit()]
    return f"v{max(nums)+1 if nums else 1}"
def check_sub(user_id):
    for ch in CHANNELS:
        try:
            m = bot.get_chat_member(ch["id"], user_id)
            if m.status not in ["member", "administrator", "creator"]:
                return False
        except:
            return False
    return True
@bot.message_handler(commands=['start'])
def start(message):
    uid = message.from_user.id
    parts = message.text.split()
    code = parts[1] if len(parts) > 1 else None
    if not code:
        bot.send_message(uid, "Welcome! Please use the video link from channel.")
        return
    if not check_sub(uid):
        markup = types.InlineKeyboardMarkup()
        for ch in CHANNELS:
            markup.add(types.InlineKeyboardButton(f"Join {ch['name']}", url=ch["link"]))
        markup.add(types.InlineKeyboardButton("Joined All, Verify Now", callback_data="verify_" + code))
        bot.send_message(uid, "You must join all 3 channels to get the video:", reply_markup=markup)
    else:
        send_video(uid, code)
@bot.callback_query_handler(func=lambda call: call.data.startswith("verify_"))
def verify(call):
    code = call.data.split("_")[1]
    if check_sub(call.from_user.id):
        bot.answer_callback_query(call.id, "Verified Successfully!")
        send_video(call.from_user.id, code)
    else:
        bot.answer_callback_query(call.id, "You haven't joined all channels yet!", show_alert=True)
def send_video(uid, code):
    fid = UPLOADS.get(code)
    if fid:
        bot.send_video(uid, fid, caption="Here is your video")
    else:
        bot.send_message(uid, "Video not found! Contact admin.")
@bot.message_handler(commands=['upload'])
def up_cmd(message):
    if message.from_user.id!= ADMIN_ID:
        return
    bot.send_message(message.chat.id, "Send the video/photo now and I will generate link for you")
@bot.message_handler(content_types=['video', 'document', 'photo'])
def save_video(message):
    if message.from_user.id!= ADMIN_ID:
        return
    if message.video:
        fid = message.video.file_id
    elif message.document:
        fid = message.document.file_id
    else:
        fid = message.photo[-1].file_id
    code = get_next_code()
    UPLOADS[code] = fid
    save_db()
    bot_username = bot.get_me().username
    link = f"https://t.me/{bot_username}?start={code}"
    bot.send_message(message.chat.id, f"Upload Successful!\n\nCode: {code}\nLink: {link}\nTotal Videos: {len(UPLOADS)}")
print("Bot Started...")
bot.infinity_polling()
EOF
echo "pyTelegramBotAPI" > requirements.txt
ls -l