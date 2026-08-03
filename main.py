import asyncio
from aiogram import Bot

# ==================== SOZLAMALAR ====================
BOT_TOKEN = "8691623183:AAGkDd6HFf3lLDuHfioqPmPKI3sHdca7wh0"
CHANNEL_ID = "@futbol_ultra"  # Masalan: @footbol_news
CHANNEL_LINK = "https://t.me/futbol_ultra"  # Kanalingizning to'liq havolasi
# ====================================================

bot = Bot(token=BOT_TOKEN)

# 1. O'YINLARNI TEKSHIRISH VA YUBORISH
async def send_daily_matches():
    # Saytdan/API'dan olinadigan o'yinlar ro'yxati (namuna)
    matches = [
        # "⚽️ Real Madrid vs Barcelona - 23:00",
        # "⚽️ Arsenal vs Chelsea - 20:30"
    ]
    source_site = "Flashscore.com"  # Ma'lumot olingan manba

    # FAQAT O'YIN BOR KUNLARI YUBORILADI
    if matches:
        text = "🔥 BUGUNGI SHOU-OʻYINLAR ROʻYXATI 🔥\n\n"
        text += "\n".join(matches)
        text += f"\n\nℹ️ *Manba: {source_site}*"
        text += f"\n\n📲 Bizga qoʻshiling: [{CHANNEL_ID}]({CHANNEL_LINK})"

        # Futbol mavzusidagi umumiy rasm
        match_image = "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?q=80&w=1000"

        await bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=match_image,
            caption=text,
            parse_mode="Markdown"
        )
        print("O'yinlar haqida post tashlandi!")
    else:
        print("Bugun o'yinlar yo'q, kanalga hech narsa yuborilmadi.")

# 2. TRANSFER XABARLARINI YUBORISH
async def send_transfer_news(player_name, old_club, new_club, fee, image_url, source):
    """
    Transferlar haqida post yuboruvchi maxsus funksiya
    """
    text = f"🚨 RASMAN / TRANSFER! 🚨\n\n"
    text += f"👤 Futbolchi: {player_name}\n"
    text += f"🔄 Oʻtish: {old_club} ➡️ {new_club}\n"
    text += f"💰 Transfer summasi: {fee}\n\n"
    text += f"ℹ️ *Manba: {source}*\n\n"
    text += f"📲 Kanalimizga obuna boʻling: [{CHANNEL_ID}]({CHANNEL_LINK})"

    await bot.send_photo(
        chat_id=CHANNEL_ID,
        photo=image_url,  # Bu yerga futbolchining eski va yangi formasi aks etgan rasm havolasi qo'yiladi
        caption=text,
        parse_mode="Markdown"
    )
    print(f"{player_name} transferi haqida post yuborildi!")

# BOTNING ASOSIY ISHCHILAR TAYMERI
async def main():
    while True:
        # Kunlik o'yinlarni tekshiradi
        await send_daily_matches()
        
        # Har 12 soatda bir marta ishlaydi
        await asyncio.sleep(43200)

if __name__ == "__main__":
    asyncio.run(main())
