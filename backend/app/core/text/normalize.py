import unicodedata

def normalize_sanskrit(text: str) -> str:
    if not text:
        return ""
    text = unicodedata.normalize("NFC", text)
    return " ".join(text.split())
