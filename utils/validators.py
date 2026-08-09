def is_valid_account_code(value: str) -> bool:
    return len(str(value).strip()) == 4 and str(value).strip().isdigit()
