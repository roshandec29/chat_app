import hashlib
from datetime import datetime


def hash_user_ids(user_ids: list):
    if not user_ids:
        return None

    concatenated_ids = ''.join(map(str, user_ids))
    sha256 = hashlib.sha256()
    sha256.update(concatenated_ids.encode('utf-8'))
    hashed_ids = sha256.hexdigest()
    return hashed_ids


def timestamp_to_date_format(timestamp: float):
    # Convert timestamp to datetime
    dt = datetime.utcfromtimestamp(timestamp)

    # Get today's date
    today_date = datetime.utcnow().date()

    if dt.date() < today_date:
        formatted_date = dt.strftime("%d/%m/%Y")
    else:
        formatted_date = dt.strftime("%H:%M")
    return formatted_date

