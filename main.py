import asyncio
import requests
from aiogram import Bot

# === BUYERGA O'ZINGIZNING MA'LUMOTLARINGIZNI YOZING ===
BOT_TOKEN = "8691623183:AAGkDd6HFf3lLDuHfioqPmPKI3sHdca7wh0"
CHANNEL_ID = "@futbol_ultra"
FOOTBALL_API_KEY = "ab942a3e909f4e54ad59761aa0b9afa1"

bot = Bot(token=BOT_TOKEN)

def get_todays_matches():
    url = "https://api.football-data.org/v4/matches"
    headers = {"X-Auth-Token": FOOTBALL_API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        matches = data.get('matches', [])

        if not matches:
            return "⚽️ Bugun rejalashtirilgan o'yinlar topilmadi."

        text = "📅 <b>BUGUNGI O'YINLAR JADVALI</b>\n\n"

        for match in matches[:10]:
            home = match['homeTeam']['name']
            away = match['awayTeam']['name']
            utc_time = match['utcDate'][11:16]
            league = match['competition']['name']
            
            text += f"🏆 <b>{league}</b>\n"
            text += f"⚔️ <b>{home}</b> vs <b>{away}</b>\n"
            text += f"⏰ Vaqti: {utc_time} (UTC)\n"
            text += "───────────────\n"

        text += "\n🔥 <i>Sevimli jamoangizga omad!</i>"
        return text

    except Exception as e:
        print(f"Xatolik: {e}")
        return None

async def main():
    print("Bot ishga tushdi va xabar tayyorlanmoqda...")
    post_text = get_todays_matches()

    if post_text:
        await bot.send_message(
            chat_id=CHANNEL_ID, 
            text=post_text, 
            parse_mode="HTML"
        )
        print("✅ Post Telegram kanalga muvaffaqiyatli joylandi!")
    
    await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())