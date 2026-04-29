from datetime import datetime, timedelta
from src.config import BOARDS, SEND_EMPTY_MAIL
from src.crawler import get_post_list, get_post_detail
from src.storage import load_seen, save_seen, get_hash
from src.filter import check_keywords
from src.summarizer import summarize
from src.mailer import send_mail

def main():
    # 중복 방지를 위한 기존 해시 로드
    seen_hashes = load_seen()
    new_seen_hashes = list(seen_hashes)
    matched_items = []

    # 한국 표준시(KST) 기준 설정
    kst_now = datetime.now() + timedelta(hours=9)
    today_str = kst_now.strftime('%Y-%m-%d')
    yesterday_str = (kst_now - timedelta(days=1)).strftime('%Y-%m-%d')

    print(f"KMCC 모니터링 시작 (기준 날짜: {yesterday_str} 이후)")

    for name, params in BOARDS.items():
        posts = get_post_list(name, params)
        for p in posts:
            # 해시를 통한 중복 여부 먼저 확인
            p_hash = get_hash(name, p['url'], p['title'], "date_ignored")
            
            if p_hash not in seen_hashes:
                detail_item = get_post_detail(p)
                post_date = detail_item.get('date', '1970-01-01')

                # 날짜 조건 충족 시 수집
                if post_date >= yesterday_str:
                    if name == "의사일정" or check_keywords(detail_item):
                        detail_item['summary'] = summarize(detail_item)
                        matched_items.append(detail_item)
                
                # 새로운 글이므로 해시 목록에 추가
                new_seen_hashes.append(p_hash)
            else:
                print(f"  -> 중복 항목 건너뜀: {p['title'][:15]}")
                
    if matched_items or SEND_EMPTY_MAIL:
        print(f"메일 발송 시도: 발견된 항목 {len(matched_items)}건")
        send_mail(matched_items, today_str)
    else:
        print(f"{yesterday_str} 이후 등록된 신규 항목이 없습니다.")
        
    save_seen(new_seen_hashes)

if __name__ == "__main__":
    main()