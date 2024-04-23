import re
import translators as ts
from backend.settings import config

__language = config.translation_language
__limit = config.translation_length_limit
__service = config.translation_service

def __cutStringToLimitStrings(text: str, limit: int) -> list[str]:
    return re.findall("(.{{1,{limit}}})(?:\s|$)".format(limit = limit), text, flags=re.IGNORECASE | re.MULTILINE)

def translate(text: str) -> str:
    str_list = __cutStringToLimitStrings(text, __limit)
    try:
        result = ""
        for elem in str_list:
            part = ts.translate_text(
                query_text= elem,
                translator= __service,
                from_language= "auto",
                to_language= __language
            )
            result += part
        return result
    except:
        return "[Unable to translate]" + text