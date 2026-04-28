def summarize(item):
    content = item.get('content', '')
    if not content or len(content) < 10:
        return "상세 내용이 없거나 요약할 수 없는 형식입니다."
    summary = content[:200].strip()
    if len(content) > 200: summary += "..."
    return summary