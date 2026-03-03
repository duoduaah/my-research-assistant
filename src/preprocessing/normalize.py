def normalize_enum(value, allowed, default="unclear"):
    if not value:
        return default
    value = value.strip().lower()
    return value if value in allowed else default