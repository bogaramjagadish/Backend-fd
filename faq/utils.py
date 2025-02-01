from googletrans import Translator
from .languages import SUPPORTED_LANGUAGES

translator = Translator()

def translate_text(target: str, text: str) -> str:
    if target not in SUPPORTED_LANGUAGES:
        return f"Error: Unsupported language '{target}'"

    try:
        translation = translator.translate(text, dest=target)
        return translation.text
    except Exception as e:
        print(f"Translation Error ({target}): {e}")
        return text
