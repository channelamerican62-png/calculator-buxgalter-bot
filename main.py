import logging
import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from config.settings import BOT_TOKEN
from handlers.excel_handler import (
    ASK_ANALYSIS_TYPE,
    analyze_data,
    cancel_handler,
    receive_excel,
)
from handlers.report_handler import (
    balance_sheet_command,
    cash_flow_command,
    income_statement_command,
    quick_analysis_command,
)
from handlers.start import button_handler, start_command

load_dotenv()

IS_RENDER = bool(os.getenv("RENDER") or os.getenv("PORT"))

log_handlers: list = [logging.StreamHandler(sys.stdout)]
if not IS_RENDER:
    log_handlers.append(logging.FileHandler("bot.log", encoding="utf-8"))

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=log_handlers,
)
logger = logging.getLogger(__name__)


class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

    def log_message(self, format, *args):
        pass


def run_bot():
    """Bot polling ni alohida thread da ishga tushiradi."""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN topilmadi! .env faylni tekshiring.")
        sys.exit(1)

    logger.info("Bot ishga tushirilmoqda...")
    application = Application.builder().token(BOT_TOKEN).build()

    excel_conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(
                filters.Document.FileExtension("xlsx") | filters.Document.FileExtension("xls"),
                receive_excel,
            )
        ],
        states={
            ASK_ANALYSIS_TYPE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, analyze_data),
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel_handler),
            MessageHandler(filters.COMMAND, cancel_handler),
        ],
    )

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("balans", balance_sheet_command))
    application.add_handler(CommandHandler("daromad", income_statement_command))
    application.add_handler(CommandHandler("naqd", cash_flow_command))
    application.add_handler(CommandHandler("tezkor", quick_analysis_command))
    application.add_handler(CommandHandler("yordam", start_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(excel_conv_handler)
    application.add_error_handler(error_handler)

    logger.info("Bot muvaffaqiyatli ishga tushdi!")
    application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Xatolik yuz berdi: %s", context.error, exc_info=True)
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "❌ <b>Xatolik yuz berdi!</b>\n\nIltimos, qaytadan urinib ko'ring.",
            parse_mode="HTML",
        )


def main() -> None:
    if IS_RENDER:
        # Render Web Service: bot background threadda, HTTP server asosiy threadda
        bot_thread = threading.Thread(target=run_bot, daemon=True)
        bot_thread.start()

        port = int(os.getenv("PORT", 10000))
        logger.info("Health check server %d-portda ishga tushdi.", port)
        server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
        server.serve_forever()
    else:
        # Local ishga tushirish
        run_bot()


if __name__ == "__main__":
    main()
