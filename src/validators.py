from datetime import datetime


def validate_iso_date(v: str):
    try:
        return datetime.fromisoformat(v)
    except:
        raise ValueError("Wrong iso date format.")
