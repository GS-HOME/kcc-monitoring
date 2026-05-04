import re
from datetime import datetime, timedelta
from src.config import BOARDS, SEND_EMPTY_MAIL
from src.crawler import get_post_list, get_post_detail
from src.storage import load_seen, save_seen, get_hash
from src.filter import check_keywords
from src.summarizer import summarize
from src.mailer import send_mail

def main():
    seen_hashes = load_seen()
    new_seen_hashes = list(seen_hashes)
    matched_items = []

    kst_now = datetime.now() + timedelta(hours=9)
    today_str = kst_now.strftime('%Y-%m-%d')
    yesterday_str = (kst_now - timedelta(days=1)).strftime('%Y-%m-%d')

    print(f"KMCC 모니터링 시작 (기준 날짜: {yesterday_str} 이후)")

    for name, params in BOARDS.items():
        posts = get_post_list(name, params)
        for p in posts:
            detail_item = get_post_detail(p)
            post_date = detail_item.get('date', '1970-01-01')

            if post_date >= yesterday_str:
                # 보도자료 게시판의 '####년 제##차 위원회' 제목 패턴 검사
                is_mandatory_press = False
                if name == "보도자료" and re.search(r'\d{4}년 제\d+차 위원회', detail_item['title']):
                    is_mandatory_press = True

                # 의사일정이거나, 필수 보도자료이거나, 키워드 검사를 통과한 경우 수집
                if name == "의사일정" or is_mandatory_press or check_keywords(detail_item):
                    detail_item['summary'] = summarize(detail_item)
                    
                    p_hash = get_hash(name, detail_item['title'], detail_item['summary'], "summary_v1")
                    
                    if p_hash not in new_seen_hashes:
                        matched_items.append(detail_item)
                        new_seen_hashes.append(p_hash)
                        print(f"  -> 신규 항목 수집: {detail_item['title'][:15]}")
                    else:
                        print(f"  -> 중복 항목 건너뜀 (요약 기준): {detail_item['title'][:15]}")
                
    if matched_items or SEND_EMPTY_MAIL:
        print(f"메일 발송 시도: 발견된 항목 {len(matched_items)}건")
        send_mail(matched_items, today_str)
    else:
        print(f"{yesterday_str} 이후 등록된 신규 항목이 없습니다.")
        
    save_seen(new_seen_hashes)

if __name__ == "__main__":
    main()