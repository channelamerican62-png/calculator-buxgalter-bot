from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    keyboard = [
        [
            InlineKeyboardButton("📊 Balans", callback_data="balance"),
            InlineKeyboardButton("📈 Daromad", callback_data="income"),
        ],
        [
            InlineKeyboardButton("💰 Naqd pul", callback_data="cashflow"),
            InlineKeyboardButton("📁 Excel yuklash", callback_data="upload"),
        ],
        [
            InlineKeyboardButton("🔍 Tezkor tahlil", callback_data="quick"),
            InlineKeyboardButton("❓ Yordam", callback_data="help"),
        ],
    ]

    welcome_text = (
        f"🇺🇿 <b>Assalomu alaykum, {user.first_name}!</b>\n\n"
        f"<b>Bu bot O'zbekiston buxgalteriya hisob-kitoblarini tezkor tahlil qilish uchun yaratilgan.</b>\n\n"
        f"📋 Bu bot quyidagi imkoniyatlarni beradi:\n"
        f"• Excel fayllarni o'qib, ularni tahlil qilish\n"
        f"• Balans ko'rsatkichlarini umumiy shaklda ko'rsatish\n"
        f"• Moliyaviy natijalar hisobotini shakllantirish\n"
        f"• Naqd pul oqimlarini tezkor ko'rib chiqish\n"
        f"• Hisob-kitoblarni tekshirish va xatolarni aniqlash\n\n"
        f"🧾 <b>Excel fayl format:</b>\n"
        f"hisob_raqami | nomlanishi | debet | kredit\n"
        f"1010 | Asosiy vositalar | 500000000 | 0\n"
        f"4010 | Daromad | 0 | 300000000\n"
        f"6010 | Xarajat | 180000000 | 0\n\n"
        f"📎 Excel faylni yuboring yoki quyidagi tugmalardan foydalaning.\n\n"
        f"📌 <b>Buyruqlar:</b>\n"
        f"/balans - Buxgalteriya balansi\n"
        f"/daromad - Moliyaviy natijalar\n"
        f"/naqd - Naqd pul oqimlari\n"
        f"/tezkor - Tezkor tahlil\n"
        f"/cancel - Bekor qilish"
    )

    await update.message.reply_text(
        welcome_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML",
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "balance":
        from handlers.report_handler import balance_sheet_command

        await balance_sheet_command(update, context)
    elif data == "income":
        from handlers.report_handler import income_statement_command

        await income_statement_command(update, context)
    elif data == "cashflow":
        from handlers.report_handler import cash_flow_command

        await cash_flow_command(update, context)
    elif data == "upload":
        await query.edit_message_text(
            "📎 <b>Excel faylni yuboring</b>\n\n"
            "Fayl quyidagi ustunlarni o'z ichiga olishi kerak:\n"
            "• <code>hisob_raqami</code>\n"
            "• <code>nomlanishi</code>\n"
            "• <code>debet</code>\n"
            "• <code>kredit</code>\n\n"
            "📌 Misol uchun quyidagi formatdan foydalaning:\n"
            "1010 | Asosiy vositalar | 500000000 | 0\n"
            "4010 | Daromad | 0 | 300000000\n"
            "6010 | Xarajat | 180000000 | 0\n\n"
            "Faylni yuboring va men uni tahlil qilaman!",
            parse_mode="HTML",
        )
    elif data == "quick":
        from handlers.report_handler import quick_analysis_command

        await quick_analysis_command(update, context)
    elif data == "help":
        help_text = (
            "❓ <b>YORDAM</b>\n\n"
            "<b>Excel fayl namunasi:</b>\n"
            "hisob_raqami | nomlanishi | debet | kredit\n"
            "1010 | Asosiy vositalar | 500000000 | 0\n"
            "4010 | Daromad | 0 | 300000000\n"
            "6010 | Xarajat | 180000000 | 0\n\n"
            "<b>Muhim eslatmalar:</b>\n"
            "• Hisob raqamlari 4 xonali bo'lishi kerak\n"
            "• Debet va kredit qiymatlari son bo'lishi kerak\n"
            "• Fayl .xlsx yoki .xls formatida bo'lishi kerak\n"
            "• Agar ustun nomlari boshqacha bo'lsa, bot ularni avtomatik tanib oladi\n\n"
            "<b>Aloqa:</b> @admin_username"
        )
        await query.edit_message_text(help_text, parse_mode="HTML")
