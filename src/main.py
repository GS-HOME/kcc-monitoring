from datetime import datetime
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
    today = datetime.now().strftime('%Y-%m-%d')

    for name, params in BOARDS.items():
        posts = get_post_list(name, params)
        for p in posts:
            p_hash = get_hash(name, p['url'], p['title'], "date_ignored")
            if p_hash not in seen_hashes:
                detail_item = get_post_detail(p)
                if check_keywords(detail_item):
                    detail_item['summary'] = summarize(detail_item)
                    matched_items.append(detail_item)
                new_seen_hashes.append(p_hash)
                
    if matched_items or SEND_EMPTY_MAIL:
        print(f"메일 발송 시도: 발견된 신규 관심 항목 {len(matched_items)}건")
        send_mail(matched_items, today)
    else:
        print("발견된 신규 관심 항목이 없어 메일을 보내지 않았습니다.")
    save_seen(new_seen_hashes)

if __name__ == "__main__":
    main()