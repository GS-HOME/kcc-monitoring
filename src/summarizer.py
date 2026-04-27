import openai
from src.config import OPENAI_API_KEY

def summarize(item):
    # 2차 기능: OpenAI API Key가 있을 경우 AI 요약 실행
    if OPENAI_API_KEY:
        try:
            client = openai.OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "너는 뉴스 요약 전문가야. 핵심 내용을 3문장 이내로 요약해줘."},
                    {"role": "user", "content": f"제목: {item['title']}\n본문: {item['content'][:1000]}"}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"AI 요약 실패: {e}")

    # 1차 기능: 규칙 기반 요약 (무료)
    content = item['content']
    sentences = [s.strip() for s in content.split('.') if s.strip()]
    
    # 1. 제목 + 2. 첫 문단(첫 문장) + 3. 담당부서 정보 조합
    summary_parts = []
    summary_parts.append(f"[{item['dept']}] {item['title']}")
    if sentences:
        summary_parts.append(sentences[0][:100] + "...")
    
    if item['attachments']:
        summary_parts.append(f"첨부파일: {', '.join(item['attachments'])}")
        
    return "\n".join(summary_parts[:3])