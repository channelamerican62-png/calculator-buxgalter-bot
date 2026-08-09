import os

import pandas as pd


class ExcelParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None

    def _normalize_columns(self):
        if self.df is None:
            return

        normalized = {}
        for column in self.df.columns:
            key = str(column).strip().lower()
            key = key.replace(" ", "_")
            key = key.replace("-", "_")
            if key in {"hisob_raqami", "hisob_raqami_"}:
                normalized[column] = "hisob_raqami"
            elif key in {"nomi", "nomlanishi", "nomi_"}:
                normalized[column] = "nomlanishi"
            elif key in {"debet", "debet_"}:
                normalized[column] = "debet"
            elif key in {"kredit", "kredit_"}:
                normalized[column] = "kredit"
            else:
                normalized[column] = key

        self.df = self.df.rename(columns=normalized)
        self.df = self.df[[col for col in ["hisob_raqami", "nomlanishi", "debet", "kredit"] if col in self.df.columns]]

    def load_file(self):
        try:
            self.df = pd.read_excel(self.file_path)
            self._normalize_columns()
            return True
        except Exception:
            return False

    def validate_structure(self):
        if self.df is None:
            return False, ["Excel fayl o'qilmadi."]

        required_columns = {"hisob_raqami", "nomlanishi", "debet", "kredit"}
        actual_columns = set(self.df.columns.astype(str).str.strip().str.lower())
        missing = required_columns - actual_columns

        errors = []
        if missing:
            errors.append(f"Kerakli ustunlar yo'q: {', '.join(sorted(missing))}")

        if self.df.empty:
            errors.append("Excel fayl bo'sh.")

        for column in ["debet", "kredit"]:
            if column in self.df.columns:
                try:
                    self.df[column] = pd.to_numeric(self.df[column], errors="coerce")
                except Exception:
                    pass

        return len(errors) == 0, errors

    def get_rows_count(self):
        return len(self.df) if self.df is not None else 0

    def get_total_debet(self):
        if self.df is None or "debet" not in self.df.columns:
            return 0.0
        return float(self.df["debet"].fillna(0).sum())

    def get_total_credit(self):
        if self.df is None or "kredit" not in self.df.columns:
            return 0.0
        return float(self.df["kredit"].fillna(0).sum())
