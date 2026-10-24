import feedparser
from bs4 import BeautifulSoup
import requests

print("--- MENJALANKAN SPION BERITA & KIRIM KE TELEGRAM ---")

# Konfigurasi Telegram Bot
TOKEN = "8395856668:AAESOOeW2OYG_xA5gxMY7R9mnZ8m2LbUN6k"
CHAT_ID = "7014098991"

def kirim_telegram(pesan):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": pesan
    }
    try:
        respon = requests.post(url, data=payload)
        print(f"Respon dari Telegram: {respon.text}")
    except Exception as e:
        print(f"Gagal kirim ke Telegram: {e}")

# Tarik RSS Sport (Bola) dan News (Nasional)
feed_sport = feedparser.parse("https://sport.detik.com/rss")
feed_news = feedparser.parse("https://news.detik.com/rss")

bola_internasional = []
berita_nasional = []

# Saring Bola Internasional
for entry in feed_sport.entries:
    judul = entry.title
    link = entry.link
    raw_summary = entry.summary if 'summary' in entry else ""
    ringkasan = BeautifulSoup(raw_summary, "html.parser").get_text(strip=True)
    judul_lower = judul.lower()
    
    if any(k in judul_lower for k in ['bola', 'liga', 'champions', 'madrid', 'barcelona', 'mu', 'arsenal', 'liverpool', 'eropa', 'skor', 'gol']) and not any(l in judul_lower for l in ['timnas', 'liga 1', 'pssi', 'persib', 'persija']):
        bola_internasional.append({'judul': judul, 'link': link, 'ringkasan': ringkasan})

# Saring Berita Nasional Non-Bola
for entry in feed_news.entries:
    judul = entry.title
    link = entry.link
    raw_summary = entry.summary if 'summary' in entry else ""
    ringkasan = BeautifulSoup(raw_summary, "html.parser").get_text(strip=True)
    judul_lower = judul.lower()
    
    if not 'bola' in judul_lower and not 'timnas' in judul_lower:
        berita_nasional.append({'judul': judul, 'link': link, 'ringkasan': ringkasan})

# Susun Format Pesan
pesan_telegram = "🚨 SPION BERITA OTOMATIS 🚨\n\n"

pesan_telegram += "⚽ BOLA INTERNASIONAL\n"
if bola_internasional:
    for i, b in enumerate(bola_internasional[:2], start=1):
        pesan_telegram += f"{i}. {b['judul']}\n{b['ringkasan'][:100]}...\nLink: {b['link']}\n\n"
else:
    pesan_telegram += "Belum ada berita bola internasional saat ini.\n\n"

pesan_telegram += "🇮🇩 BERITA NASIONAL (NON-BOLA)\n"
if berita_nasional:
    for i, b in enumerate(berita_nasional[:2], start=1):
        pesan_telegram += f"{i}. {b['judul']}\n{b['ringkasan'][:100]}...\nLink: {b['link']}\n\n"
else:
    pesan_telegram += "Belum ada berita nasional saat ini.\n\n"

# Kirim laporan ke Telegram
print("Mengirim laporan lengkap ke bot Telegram...")
kirim_telegram(pesan_telegram)

print("--- SELESAI ---")