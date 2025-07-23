from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import Application, ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import threading
import asyncio
import logging
import pytz
import os

auto_task = None

VIDEO_FILE_ID = "BAACAgUAAxkBAAIB2mhsD3ZVutH2tvrQssv6OmR08cfUAAIeFwACZ8VgV8aQehQGveLrNgQ"

# ID grup dan channel
API_TOKEN = os.environ["API_TOKEN"]
GRUP_INFO_FREEBET_ID = -1002658447462
GRUP_LINK_GACOR_ID = -1002255700000
CHANNEL_KOLONI4D_ID = -1002585588580
TARGET_CHAT_IDS = [GRUP_INFO_FREEBET_ID, GRUP_LINK_GACOR_ID]

# Daftar foto hot (URL gambar langsung)
FOTO_HOT_LIST = [
    "https://i.postimg.cc/CzfXRxr3/15.jpg",
    "https://i.postimg.cc/BtzRZKp5/16.jpg",
    "https://i.postimg.cc/VSzVZBsw/17.jpg",
    "https://i.postimg.cc/Yv6PxyH8/18.jpg",
    "https://i.postimg.cc/8Fwn2Js6/19.jpg",
    "https://i.postimg.cc/r0PZpB1y/20.jpg",
    "https://i.postimg.cc/9wDStmmq/3.jpg",
    "https://i.postimg.cc/87Q3Mgqj/6.jpg",
    "https://i.postimg.cc/c6CVNmR4/7.jpg",
    "https://i.postimg.cc/qhRZ4JCZ/A1.jpg"
]

FOTO_HOT_LIST2 = [
    "https://i.postimg.cc/rshD8ww2/5955226285280180500.jpg",
]

messages = (
    "🔥<b>GRUP HIBURAN DEWASA  +  SLOT GACOR 2025!</b>🔥\n"
    "———————————————\n"
    "🌟 <b>Satu tempat, dua kenikmatan</b>  —  hiburan + cuan!\n\n"

    "📂 <b>FULL LINK BOKEP UPDATE HARIAN</b>\n"
    "  • Lokal & internasional, kualitas HD\n"
    "  • Koleksi di‑update nonstop 🔄\n\n"
    "  • Live Vidio Hot 🔥\n\n"


    "🎰 <b>SLOT GACOR + RTP REAL‑TIME</b>\n"
    "  • Info bocoran pola JP tiap hari 💥\n"
    "  • Bukti WD asli member ✅\n\n"

    "👥 Grup ramai • Member aktif • Tanpa hoax\n"
    "🕵️‍♂️ Admin responsif 24 jam\n\n"

    "🚨 <u>BURUAN JOIN SEBELUM DILIMIT!</u> 🚨\n"
    "😈 <b>Gabung sekarang, rasakan sendiri bedanya!</b>"
)


PROMO_KEYBOARD = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("📥 BOT UTAMA", url="https://t.me/Idaman_warga62_bot"),
        InlineKeyboardButton("🔗 LINK ALTERNATIF", url="https://mez.ink/koloni4d"),
        InlineKeyboardButton("🔗 LINK ALTERNATIF", url="https://heylink.me/LinkAlternatifKoloni4D")
    ]
])

logging.basicConfig(level=logging.INFO)

async def is_member(bot: Bot, user_id: int, chat_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"[is_member] Error cek keanggotaan chat_id {chat_id}: {e}")
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("📸 Foto Hot 🔥", callback_data="foto_hot"),
            InlineKeyboardButton("🎞️ Video Hot 🎬", callback_data="video_hot")
        ],
        [
            InlineKeyboardButton("🔗 Situs Link Gacor 1 🚀", url="https://mez.ink/koloni4d/"),
            InlineKeyboardButton("🔥 Grup LiVe Omek", url="https://t.me/Livevideohot_Bot")
        ]
        
    ]

    welcome_text = (
        "💋 *Selamat Datang di Dunia Nakal Koloni4D!* 💋\n\n"
        "Siapkan jantungmu... karena di sini bukan tempat biasa.\n"
        "Konten panas, live menggoda, dan link-link rahasia — semuanya cuma buat kamu yang berani!\n\n"
        "📸 *FOTO HOT GILA!* — Cewek-cewek montok, pose gak pake malu-malu 😏\n"
        "🎥 *VIDEO HOT FULL AXXX!* — Aksi liar, tatapan nakal, suara desahan jelas!\n"
        "🔴 *LIVE OMEK NAKAL!* — Cewek real, live langsung, siap ajak kamu basah-basahan 🥵\n"
        "🔗 *LINK GACOR TEMBUS SORGA!* — Akses kilat ke tempat paling panas, anti sensor!\n\n"
        "🚨 _Wajib join grup & channel sebelum menikmati semua ini. Koloni4D gak main-main, bro!_"
    )

    if update.message:
        await update.message.reply_text(
            welcome_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            welcome_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data in ["foto_hot", "video_hot"]:
        verify_callback = "verify_foto_hot" if query.data == "foto_hot" else "verify_video_hot"
        keyboard = [
            [
                InlineKeyboardButton("📣 Join Grup Info Freebet4D", url="https://t.me/InfoFreebet4D"),
                InlineKeyboardButton("🧲 Join Grup Situs Link Gacor", url="https://t.me/SITUSLINKGACOR4D")
            ],
            [
                InlineKeyboardButton("📺 Join Channel Koloni4D", url="https://t.me/koloni4d_official1"),
                InlineKeyboardButton("✅ Saya Sudah Join, Verifikasi Sekarang", callback_data=verify_callback)
            ],
            [
                InlineKeyboardButton("🔙 Kembali", callback_data="back_to_start")
            ]
        ]
        await query.edit_message_text(
            """🚨 <b>Verifikasi Keanggotaan Dulu!</b>

⚠️ Untuk akses konten eksklusif, kamu wajib gabung di:
• 2 Grup VIP Telegram
• 1 Channel Resmi Koloni4D

➡️ Setelah bergabung, klik tombol 
✅ Saya Sudah Join untuk verifikasi keanggotaan kamu.
Terima kasih sudah bergabung dan selamat menikmati konten!""",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )

    elif query.data == "verify_foto_hot":
        is_in_grup1 = await is_member(context.bot, user_id, GRUP_INFO_FREEBET_ID)
        is_in_grup2 = await is_member(context.bot, user_id, GRUP_LINK_GACOR_ID)
        is_in_channel = await is_member(context.bot, user_id, CHANNEL_KOLONI4D_ID)
        if is_in_grup1 and is_in_grup2 and is_in_channel:
            await query.edit_message_text("✅ Kamu sudah gabung di semua grup & channel VIP!\nBerikut koleksi foto hot:")
            for url in FOTO_HOT_LIST:
                try:
                    await query.message.reply_photo(photo=url)
                except Exception as e:
                    print(f"Gagal kirim foto {url}: {e}")
            keyboard = [[InlineKeyboardButton("🔙 Kembali ke Menu Utama", callback_data="back_to_start")]]
            await query.message.reply_text("Pilih menu selanjutnya:", reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            keyboard = [
                [InlineKeyboardButton("📣 Join Grup Info Freebet4D", url="https://t.me/InfoFreebet4D")],
                [InlineKeyboardButton("🧲 Join Grup Situs Link Gacor", url="https://t.me/SITUSLINKGACOR4D")],
                [InlineKeyboardButton("📺 Join Channel Koloni4D", url="https://t.me/koloni4d_official1")],
                [InlineKeyboardButton("🔙 Kembali", callback_data="back_to_start")]
            ]
            await query.edit_message_text(
                "❌ Kamu belum gabung di semua grup & channel VIP.\n"
                "Silakan join dulu, lalu verifikasi ulang.",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

    elif query.data == "verify_video_hot":
        is_in_grup1 = await is_member(context.bot, user_id, GRUP_INFO_FREEBET_ID)
        is_in_grup2 = await is_member(context.bot, user_id, GRUP_LINK_GACOR_ID)
        is_in_channel = await is_member(context.bot, user_id, CHANNEL_KOLONI4D_ID)
        if is_in_grup1 and is_in_grup2 and is_in_channel:
            await query.edit_message_text("✅ Kamu sudah gabung di semua grup & channel VIP!\nBerikut koleksi video hot:")
            for url in FOTO_HOT_LIST2:
                try:
                    await query.message.reply_photo(photo=url)
                except Exception as e:
                    print(f"Gagal kirim video {url}: {e}")
            tombol_link = [
                [InlineKeyboardButton("🎥 Link Video Lengkap", url="https://dm.fandome.co/feed?wid=88ESU7NX")],
                [InlineKeyboardButton("🔙 Kembali ke Menu Utama", callback_data="back_to_start")]
            ]
            await query.message.reply_text(
                "🎬 Klik tombol di bawah untuk akses video lengkap dan konten menarik lainnya!",
                reply_markup=InlineKeyboardMarkup(tombol_link))
        else:
            keyboard = [
                [InlineKeyboardButton("📣 Join Grup Info Freebet4D", url="https://t.me/InfoFreebet4D")],
                [InlineKeyboardButton("🧲 Join Grup Situs Link Gacor", url="https://t.me/SITUSLINKGACOR4D")],
                [InlineKeyboardButton("📺 Join Channel Koloni4D", url="https://t.me/koloni4d_official1")],
                [InlineKeyboardButton("🔙 Kembali", callback_data="back_to_start")]
            ]
            await query.edit_message_text(
                "❌ Kamu belum gabung di semua grup & channel VIP.\n"
                "Silakan join dulu, lalu verifikasi ulang.",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

    elif query.data == "back_to_start":
        await start(update, context)

async def auto_send_messages(app: Application):
    while True:
        for chat_id in [GRUP_INFO_FREEBET_ID, GRUP_LINK_GACOR_ID]:
            try:
                await app.bot.send_video(chat_id=chat_id, video=VIDEO_FILE_ID)
                keyboard = InlineKeyboardMarkup([
                        [InlineKeyboardButton("📥 BOT UTAMA", url="https://t.me/Idaman_warga62_bot")],
                        [InlineKeyboardButton("🔗 LINK ALTERNATIF", url="https://mez.ink/koloni4d")],
                        [InlineKeyboardButton("🔗 TERBARU LIVE 0M3K", url="https://t.me/Livevideohot_Bot")]
                    ])
                await app.bot.send_message(
                    chat_id=chat_id,
                    text=messages,
                    parse_mode="HTML",
                    reply_markup=keyboard
                )
                logging.info(f"✅ Kirim video & teks ke {chat_id} berhasil.")
            except Exception as e:
                logging.error(f"❌ Gagal kirim video & teks ke {chat_id}: {e}")
        logging.info("⌛ Menunggu 2 jam sebelum pengiriman berikutnya...")
        await asyncio.sleep(7200)  # 2 jam = 7200 detik

async def on_startup(app: Application):
    global auto_task
    if auto_task is None:
        auto_task = asyncio.create_task(auto_send_messages(app))
        print("🚀 Auto-send promo dimulai...")
        
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is alive!")

    def do_HEAD(self):
        # Kirim response header yang sama seperti do_GET, tanpa body
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
        else:
            self.send_response(200)
            self.end_headers()


def start_ping_server():
    import os
    port = int(os.environ.get('PORT', 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

# Jalankan server HTTP di thread terpisah
threading.Thread(target=start_ping_server, daemon=True).start()

def main():
    application = Application.builder().token(API_TOKEN).post_init(on_startup).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
