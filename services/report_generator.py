class ReportGenerator:
    def __init__(self, parser):
        self.parser = parser

    def _format_currency(self, value: float) -> str:
        return f"{value:,.2f} so'm"

    def generate_balance_sheet(self) -> str:
        debet_total = self.parser.get_total_debet()
        credit_total = self.parser.get_total_credit()
        net_position = debet_total - credit_total

        trend = "ko'payish" if net_position >= 0 else "kamayish"
        return (
            "📊 <b>Balans hisobi</b>\n\n"
            "<b>Aktivlar:</b> " + self._format_currency(max(debet_total, credit_total)) + "\n"
            "<b>Majburiyatlar:</b> " + self._format_currency(min(debet_total, credit_total)) + "\n"
            f"<b>Sof holat:</b> {self._format_currency(abs(net_position))} {trend}\n\n"
            "⚠️ Bu hisobot Excel ma'lumotlariga asoslangan umumiy ko'rsatkichdir."
        )

    def generate_income_statement(self) -> str:
        debet_total = self.parser.get_total_debet()
        credit_total = self.parser.get_total_credit()
        net_profit = credit_total - debet_total

        return (
            "📈 <b>Moliyaviy natijalar hisobi</b>\n\n"
            f"💰 Jami daromad: {self._format_currency(credit_total)}\n"
            f"💸 Jami xarajat: {self._format_currency(debet_total)}\n"
            f"📌 Sof foyda: {self._format_currency(max(net_profit, 0))}\n"
            f"📉 Sof zarar: {self._format_currency(max(-net_profit, 0))}\n"
        )

    def generate_cash_flow(self) -> str:
        return (
            "💰 <b>Naqd pul oqimlari hisobi</b>\n\n"
            f"📥 Kirim: {self._format_currency(self.parser.get_total_credit())}\n"
            f"📤 Chiqim: {self._format_currency(self.parser.get_total_debet())}\n\n"
            "📌 Ushbu ko'rsatkich Exceldagi umumiy daromad va xarajatlar asosida hisoblab chiqilgan."
        )

    def generate_quick_analysis(self) -> str:
        return (
            "🔍 <b>Tezkor tahlil</b>\n\n"
            f"📊 Yozuvlar soni: {self.parser.get_rows_count()}\n"
            f"💰 Debet jami: {self._format_currency(self.parser.get_total_debet())}\n"
            f"💳 Kredit jami: {self._format_currency(self.parser.get_total_credit())}\n"
            f"📌 Hisobot holati: {'muvozanatli' if abs(self.parser.get_total_debet() - self.parser.get_total_credit()) < 1000 else 'e\'tiborga loyiq'}\n"
        )
