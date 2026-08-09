import os
import tempfile
import unittest

import pandas as pd

from services.excel_parser import ExcelParser
from services.report_generator import ReportGenerator


class ExcelParserTests(unittest.TestCase):
    def test_load_and_normalize_columns(self):
        data = pd.DataFrame(
            {
                "Hisob Raqami": ["1010", "4010"],
                "Nomi": ["Asosiy vosita", "Realizatsiya daromadi"],
                "Debet": [1000000, 0],
                "Kredit": [0, 800000],
            }
        )

        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as handle:
            temp_path = handle.name

        try:
            data.to_excel(temp_path, index=False)
            parser = ExcelParser(temp_path)
            self.assertTrue(parser.load_file())
            self.assertEqual(
                parser.df.columns.tolist(),
                ["hisob_raqami", "nomlanishi", "debet", "kredit"],
            )
            is_valid, errors = parser.validate_structure()
            self.assertTrue(is_valid, errors)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_report_generator_builds_balance_and_income_summary(self):
        parser = ExcelParser("dummy.xlsx")
        parser.df = pd.DataFrame(
            {
                "hisob_raqami": ["1010", "4010", "6010"],
                "nomlanishi": ["Asosiy vosita", "Daromad", "Xarajat"],
                "debet": [500000, 0, 180000],
                "kredit": [0, 300000, 0],
            }
        )

        generator = ReportGenerator(parser)
        balance_report = generator.generate_balance_sheet()
        income_report = generator.generate_income_statement()

        self.assertIn("Aktivlar", balance_report)
        self.assertIn("Majburiyatlar", balance_report)
        self.assertIn("Sof foyda", income_report)


if __name__ == "__main__":
    unittest.main()
