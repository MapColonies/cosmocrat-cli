from datetime import datetime, timezone

def get_current_datetime():
    return datetime.now(tz=timezone.utc)

def datetime_to_string(datetime):
    return datetime.strftime(r'%Y-%m-%dT%H:%M:%SZ')
