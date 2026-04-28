from datetime import datetime
from src.config import BOARDS, SEND_EMPTY_MAIL
from src.crawler import get_post_list, get_post_detail
from src.storage import load_seen, save_seen, get_hash
from src.summarizer import summarize
from src.mailer import send_mail

def main():
    seen_hashes = load_seen()
    new_seen_hashes = seen_hashes.copy()
    matched_items = []
    today = datetime.now().strftime('%Y-%m-%d')

    for name, params in BOARDS.items():
        posts = get_post_list(name, params)
        for p in posts:
            print(f"[{name}] 상세 페이지 테스트 접속 진행...")
            # 1개만 크롤링하므로 무조건 상세 페이지 접속
            detail_item = get_post_detail(p)
            
            # 필터링을 생략하고 테스트를 위해 강제로 매칭된 것으로 처리
            detail_item['matched_keyword'] = "테스트 강제 통과"
            detail_item['summary'] = summarize(detail_item)
            matched_items.append(detail_item)
            
            p_hash = get_hash(name, p['url'], p['title'], "date_ignored")
            if p_hash not in new_seen_hashes:
                new_seen_hashes.append(p_hash)
                
    if matched_items or SEND_EMPTY_MAIL:
        print(f"메일 발송 시도: 테스트 항목 {len(matched_items)}건")
        send_mail(matched_items, today)
    else:
        print("발견된 테스트 항목이 없습니다.")
        
    save_seen(new_seen_hashes)

if __name__ == "__main__":
    main()