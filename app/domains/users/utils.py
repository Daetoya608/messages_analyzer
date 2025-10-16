

def get_full_name(first_name: str | None, last_name: str | None):
    result = first_name if first_name else ""
    result += " " if len(result) > 0 and last_name else ""
    result += last_name if last_name else ""
    return result
