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

    # 깃허브 액션(UTC) 환경을 고려하여 한국 표준시(KST)로 변환
    kst_now = datetime.now() + timedelta(hours=9)
    today_str = kst_now.strftime('%Y-%m-%d')
    yesterday_str = (kst_now - timedelta(days=1)).strftime('%Y-%m-%d')

    for name, params in BOARDS.items():
        posts = get_post_list(name, params)
        for p in posts:
            # 날짜를 확인하기 위해 상세 페이지 데이터 추출
            detail_item = get_post_detail(p)
            post_date = detail_item.get('date', '1970-01-01')

            # 등록일이 어제 또는 오늘인 경우에만 키워드 검사 및 수집 (중복 허용)
            if post_date >= yesterday_str:
                if check_keywords(detail_item):
                    detail_item['summary'] = summarize(detail_item)
                    matched_items.append(detail_item)

            # 기존 해시 데이터베이스 유지를 위해 기록
            p_hash = get_hash(name, p['url'], p['title'], "date_ignored")
            if p_hash not in new_seen_hashes:
                new_seen_hashes.append(p_hash)
                
    if matched_items or SEND_EMPTY_MAIL:
        print(f"메일 발송 시도: 발견된 관심 항목 {len(matched_items)}건 (어제/오늘 등록일 기준)")
        send_mail(matched_items, today_str)
    else:
        print("어제 및 오늘 등록된 관심 항목이 없어 메일을 보내지 않았습니다.")
        
    save_seen(new_seen_hashes)

if __name__ == "__main__":
    main()