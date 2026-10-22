import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# =========================================================================
# 1. MASUKKAN TOKEN BOT TELEGRAM ANDA DI BAWAH INI
# =========================================================================
TOKEN = "8604298054:AAEPyfYXXVDwhSsR32Y2dSGJGoEsl4e8IQI"

# =========================================================================
# 2. FUNGSI UNTUK MENGAMBIL DATA TULISAN JAWI DARI WEB PRPM DBP
# =========================================================================
def cari_jawi_prpm(perkataan):
    url = f"https://dbp.gov.my{perkataan}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return "Maaf, gagal menghubungi pelayan PRPM DBP."
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Mencari element span yang mengandungi tulisan Jawi di laman web PRPM
        jawi_element = soup.find('span', {'class': 'jawi'}) or soup.find('span', {'style': lambda x: x and 'Traditional Arabic' in x})
        
        if jawi_element:
            return jawi_element.text.strip()
        else:
            return f"Ejaan Jawi untuk '{perkataan}' tidak ditemui di PRPM DBP. Sila pastikan ejaan Rumi anda betul."
            
    except Exception as e:
        return "Ralat teknikal berlaku semasa membuat carian ke PRPM DBP."

# =========================================================================
# 3. FUNGSI UNTUK MENGENDALIKAN ARAHAN DAN MESEJ TELEGRAM
# =========================================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Mesej selamat datang apabila pengguna tekan butang /start
    tanya_user = "Salam! Sila taip sebarang perkataan Rumi (contoh: kereta) untuk saya carikan ejaan Jawi rasmi dari PRPM DBP."
    await update.message.reply_text(tanya_user)

async def kendali_mesej(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teks_pengguna = update.message.text.strip()
    
    # Menunjukkan status 'typing...' pada Telegram tanda bot sedang bekerja
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # Memproses carian tulisan Jawi
    hasil_jawi = cari_jawi_prpm(teks_pengguna)
    
    # Menghantar semula jawapan kepada pengguna
    mesej_balasan = f"Rumi: {teks_pengguna}\nJawi: {hasil_jawi}"
    await update.message.reply_text(mesej_balasan)

# =========================================================================
# 4. BAHAGIAN UTAMA UNTUK MENGHIDUPKAN BOT
# =========================================================================
def main():
    # Membina aplikasi bot menggunakan Token anda
    app = Application.builder().token(TOKEN).build()
    
    # Mendaftarkan arahan /start dan fungsi membaca mesej teks
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, kendali_mesej))
    
    print("Bot Jawi anda sedang berjalan... Sila uji bot anda di Telegram sekarang!")
    app.run_polling()

if __name__ == '__main__':
    main()
