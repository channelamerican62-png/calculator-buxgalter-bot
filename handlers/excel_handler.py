import os
import tempfile

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler

from services.excel_parser import ExcelParser
from services.report_generator import ReportGenerator

ASK_ANALYSIS_TYPE = 1

ANALYSIS_TYPES = [
    ["📊 Balans tahlili"],
    ["📈 Daromadlar/xarajatlar"],
    ["🔍 Xatolarni tekshirish"],
    ["📑 To'liq hisobot"],
    ["❌ Bekor qilish"],
]


async def receive_excel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document

    if document.file_size > 10 * 1024 * 1024:
        await update.message.reply_text("❌ Fayl hajmi 10 MB dan oshmasligi kerak!")
        return ConversationHandler.END

    if not document.file_name.endswith((".xlsx", ".xls")):
        await update.message.reply_text("❌ Faqat .xlsx yoki .xls formatidagi fayllarni qabul qilaman!")
        return ConversationHandler.END

    processing_msg = await update.message.reply_text("⏳ <b>Fayl yuklanmoqda...</b>", parse_mode="HTML")

    try:
        file = await context.bot.get_file(document.file_id)
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, f"accounting_{update.effective_user.id}_{document.file_name}")

        await file.download_to_drive(file_path)

        parser = ExcelParser(file_path)
        if not parser.load_file():
            await processing_msg.edit_text(
                "❌ <b>Faylni o'qishda xatolik yuz berdi!</b>\n\n"
                "Fayl to'g'ri Excel formatida ekanligini tekshiring."
            )
            return ConversationHandler.END

        is_valid, errors = parser.validate_structure()
        if not is_valid:
            error_text = "⚠️ <b>Fayl tuzilmasida xatolar:</b>\n\n"
            for index, error in enumerate(errors, 1):
                error_text += f"{index}. {error}\n"
            error_text += "\n📎 Iltimos, faylni to'g'ri formatda yuboring."
            await processing_msg.edit_text(error_text, parse_mode="HTML")
            return ConversationHandler.END

        context.user_data["excel_path"] = file_path
        context.user_data["parser"] = parser
        context.user_data["file_name"] = document.file_name

        keyboard = ReplyKeyboardMarkup(ANALYSIS_TYPES, resize_keyboard=True)
        balance_gap = abs(parser.get_total_debet() - parser.get_total_credit())
        await processing_msg.edit_text(
            f"✅ <b>Fayl muvaffaqiyatli yuklandi!</b>\n\n"
            f"📄 Fayl: <code>{document.file_name}</code>\n"
            f"📊 Yozuvlar soni: {parser.get_rows_count()}\n"
            f"💰 Debet jami: {parser.get_total_debet():,.2f} so'm\n"
            f"💳 Kredit jami: {parser.get_total_credit():,.2f} so'm\n"
            f"📌 Balans farqi: {balance_gap:,.2f} so'm\n\n"
            f"{'✅ Muvozanat yaxshi' if balance_gap < 1000 else '⚠️ Muvozanatda farq bor'}\n\n"
            f"Quyidagilardan birini tanlang:",
            reply_markup=keyboard,
            parse_mode="HTML",
        )
        return ASK_ANALYSIS_TYPE
    except Exception as exc:  # pylint: disable=broad-except
        await processing_msg.edit_text(
            f"❌ <b>Faylni qayta ishlashda xatolik yuz berdi:</b>\n\n{exc}",
            parse_mode="HTML",
        )
        return ConversationHandler.END


async def analyze_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text
    parser = context.user_data.get("parser")

    if not parser:
        await update.message.reply_text("📎 Avval Excel faylni yuboring.")
        return ConversationHandler.END

    generator = ReportGenerator(parser)

    if choice == "📊 Balans tahlili":
        report = generator.generate_balance_sheet()
    elif choice == "📈 Daromadlar/xarajatlar":
        report = generator.generate_income_statement()
    elif choice == "🔍 Xatolarni tekshirish":
        report = generator.generate_quick_analysis()
    elif choice == "📑 To'liq hisobot":
        report = (
            generator.generate_balance_sheet() + "\n\n" + generator.generate_income_statement() + "\n\n" + generator.generate_cash_flow()
        )
    else:
        await update.message.reply_text("❌ Jarayon bekor qilindi.", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
        return ConversationHandler.END

    await update.message.reply_text(report, parse_mode="HTML", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    return ConversationHandler.END


async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Jarayon bekor qilindi.", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    return ConversationHandler.END
