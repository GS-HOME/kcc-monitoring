from src.config import HIGH_PRIORITY_KEYWORDS, INCLUDE_KEYWORDS, EXCLUDE_KEYWORDS

def check_keywords(item):
    text_parts = [item.get('title', ''), item.get('content', '')]
    text_parts.extend(item.get('attachments', []))
    text_to_search = " ".join(text_parts)

    for ex in EXCLUDE_KEYWORDS:
        if ex in text_to_search:
            return False

    for high in HIGH_PRIORITY_KEYWORDS:
        if high in text_to_search:
            item['matched_keyword'] = high
            return True

    for inc in INCLUDE_KEYWORDS:
        if inc in text_to_search:
            item['matched_keyword'] = inc
            return True

    return False