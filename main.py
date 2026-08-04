import os
from threading import Thread
from flask import Flask

# --- FLASK SERVER (ENG TEPASIGA QO'SHILADI) ---
app = Flask('')


@app.route('/')
def home():
  return 'Bot backend is running!'


def run():
  port = int(os.environ.get('PORT', 10000))
  app.run(host='0.0.0.0', port=port)


def keep_alive():
  t = Thread(target=run)
  t.start()


# Servisni ishga tushiramiz
keep_alive()
# ---------------------------------------------

# 👇 SIZNING ESKI KODLARINGIZ SHU YERDAN DAVOM ETADI (HECH NARSANI O'CHIRMANG):
import telebot  # yoki aiogram / python-telegram-bot

# sizning bot tokeningiz, xandlerlar va barcha eski kodingiz...s
import asyncio
import datetime
import requests
from aiogram import Bot
from openai import OpenAI
# ==================== SOZLAMALAR ====================
BOT_TOKEN = "8691623183:AAGkDd6HFf3lLDuHfioqPmPKI3sHdca7wh0"
CHANNEL_ID = "@futbol_ultra"                             # Kanalingiz usernamesi
CHANNEL_LINK = "https://t.me/futbol_ultra"             # Kanalingiz havolasi
FOOTBALL_DATA_API_KEY = "ab942a3e909f4e54ad59761aa0b9afa1"   # Football-Data.org API kaliti
OPENAI_API_KEY = "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"                 # OpenAI API kaliti
# Standart futbol rasmi
DEFAULT_IMAGE = "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?q=80&w=1000"
# ====================================================
bot = Bot(token=BOT_TOKEN)
ai_client = OpenAI(api_key=OPENAI_API_KEY)
# --- AI SHARH TAYYORLASH FUNKSIYASI --
def generate_ai_caption(prompt_text):
    try:
        response = ai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Siz futbol bo'yicha ekspert va 'Futbol Ultra' kanalining adminisiz. Matnlarni o'zbek tilida chiroyli, jozibali, emojilar va heshteglar bilan bezatib berishingiz kerak."},
                {"role": "user", "content": prompt_text}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"AI Xatolik: {e}")
        return None
# --- A) TRANSFERLAR MODULI --
async def send_transfer_post(player, old_club, new_club, fee, contract_years):
    raw_prompt = f"Ushbu transfer haqida post tayyorlang:\nO'yinchi: {player}\nEski klub: {old_club} -> 
Yangi klub: {new_club}\nSumma: {fee}\nShartnoma: {contract_years} yil\n\nTalablar:\n1. Post boshida 
#transfer heshtegi bo'lsin.\n2. Alohida qatorda va ajralib turadigan stilda 'HERE WE GO!' iborasi 
yozilsin.\n3. Transfer haqida qisqacha, ta'sirli ma'lumot berilsin."
    caption = generate_ai_caption(raw_prompt)
    if caption:
        caption += f"\n\n📲 **Bizga qoʻshiling:** [{CHANNEL_ID}]({CHANNEL_LINK})"
        await bot.send_photo(chat_id=CHANNEL_ID, photo=DEFAULT_IMAGE, caption=caption, 
parse_mode="Markdown")
# --- B) YANGILIKLAR MODULI --
async def send_news_post(news_title, news_details):
    raw_prompt = f"Ushbu futbol yangiligini o'zbek tilida sodda va qiziqarli holga keltiring:\nSarlavha: 
{news_title}\nTafsilot: {news_details}\n\nTalablar:\n1. Post boshida #yangiliklar heshtegi bo'lsin.\n2. 
Qisqa va ta'sirli shaklda yozilsin."
    caption = generate_ai_caption(raw_prompt)
    if caption:
        caption += f"\n\n📲 **Bizga qoʻshiling:** [{CHANNEL_ID}]({CHANNEL_LINK})"
        await bot.send_photo(chat_id=CHANNEL_ID, photo=DEFAULT_IMAGE, caption=caption, 
parse_mode="Markdown")
# --- C) O'YINLAR MODULI (API orqali) --
def get_today_matches():
    today = datetime.date.today().strftime('%Y-%m-%d')
    url = f"https://api.football-data.org/v4/matches?dateFrom={today}&dateTo={today}"
    headers = {"X-Auth-Token": FOOTBALL_DATA_API_KEY}
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            data = res.json()
            matches = []
            for m in data.get("matches", []):
                home = m["homeTeam"]["name"]
                away = m["awayTeam"]["name"]
                league = m["competition"]["name"]
                utc_time = datetime.datetime.strptime(m["utcDate"], "%Y-%m-%dT%H:%M:%SZ")
                time_str = (utc_time + datetime.timedelta(hours=5)).strftime("%H:%M")
                matches.append(f"{home} vs {away} ({time_str} - {league})")
            return matches
    except Exception as e:
        print(f"API xato: {e}")
    return []
async def check_and_send_daily_matches():
    matches = get_today_matches()
    if matches:
        matches_text = "\n".join(matches)
        raw_prompt = f"Bugun bo'lib o'tadigan futbol o'yinlari ro'yxati:\n{matches_text}\n\nTalablar:\n1. 
Post boshida #o'yinlar heshtegi bo'lsin.\n2. O'yinlarni 'Klub A 🆚 Klub B' formatida chiroyli dizayn bilan 
joylang.\n3. Bugungi markaziy o'yinlarga 1-2 jumla qiziqarli AI sharhi qo'shing."
        caption = generate_ai_caption(raw_prompt)
        if caption:
            caption += f"\n\n📲 **Bizga qoʻshiling:** [{CHANNEL_ID}]({CHANNEL_LINK})"
            await bot.send_photo(chat_id=CHANNEL_ID, photo=DEFAULT_IMAGE, caption=caption, 
parse_mode="Markdown")
async def main():
    print("Bot muvaffaqiyatli ishga tushdi!")
    await check_and_send_daily_matches()
if __name__ == "__main__":
    asyncio.run(main())
