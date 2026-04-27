from src.config import HIGH_PRIORITY_KEYWORDS, INCLUDE_KEYWORDS, EXCLUDE_KEYWORDS

def check_keywords(item):
    text = f"{item['title']} {item['content']} {' '.join(item['attachments'])}"
    is_high = any(k in text for k in HIGH_PRIORITY_KEYWORDS)
    is_include = any(k in text for k in INCLUDE_KEYWORDS)
    is_exclude = any(k in text for k in EXCLUDE_KEYWORDS)
    
    if is_high:
        item['matched_keyword'] = "우선순위 포함"
        return True
    if is_include and not is_exclude:
        item['matched_keyword'] = "일반 키워드 포함"
        return True
    return False