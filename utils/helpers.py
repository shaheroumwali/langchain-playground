def truncate_response(text: str, max_chars: int) -> str:
    if not isinstance(text, str):
        text = str(text)
    return text if len(text) <= max_chars else text[:max_chars] + "..."
