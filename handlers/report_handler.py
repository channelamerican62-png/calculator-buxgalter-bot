from telegram import Update
from telegram.ext import ContextTypes

from services.report_generator import ReportGenerator


async def balance_sheet_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    parser = context.user_data.get("parser")
    if not parser:
        await update.effective_message.reply_text("📎 Avval Excel faylni yuboring. Men uni tahlil qilaman.")
        return

    report = ReportGenerator(parser).generate_balance_sheet()
    await update.effective_message.reply_text(report, parse_mode="HTML")


async def income_statement_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    parser = context.user_data.get("parser")
    if not parser:
        await update.effective_message.reply_text("📎 Avval Excel faylni yuboring.")
        return

    report = ReportGenerator(parser).generate_income_statement()
    await update.effective_message.reply_text(report, parse_mode="HTML")


async def cash_flow_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    parser = context.user_data.get("parser")
    if not parser:
        await update.effective_message.reply_text("📎 Avval Excel faylni yuboring.")
        return

    report = ReportGenerator(parser).generate_cash_flow()
    await update.effective_message.reply_text(report, parse_mode="HTML")


async def quick_analysis_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    parser = context.user_data.get("parser")
    if not parser:
        await update.effective_message.reply_text("📎 Avval Excel faylni yuboring.")
        return

    report = ReportGenerator(parser).generate_quick_analysis()
    await update.effective_message.reply_text(report, parse_mode="HTML")

