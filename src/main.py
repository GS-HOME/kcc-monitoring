from datetime import datetime, timedelta
from src.config import BOARDS, SEND_EMPTY_MAIL
from src.crawler import get_post_list, get_post_detail
from src.filter import check_keywords
from src.summarizer import summarize
from src.mailer import send_mail

def main():
    matched_items = []

    # 한국 표준시(KST) 기준 설정
    kst_now = datetime.now() + timedelta(hours=9)
    today_str = kst_now.strftime('%Y-%m-%d')
    yesterday_str = (kst_now - timedelta(days=1)).strftime('%Y-%m-%d')

    print(f"모니터링 시작 (기준 날짜: {yesterday_str} 이후)")

    for name, params in BOARDS.items():
        posts = get_post_list(name, params)
        for p in posts:
            detail_item = get_post_detail(p)
            post_date = detail_item.get('date', '1970-01-01')

            # 어제 또는 오늘 게시글만 수집
            if post_date >= yesterday_str:
                # 의사일정 게시판은 키워드 무시, 그 외 게시판은 키워드 검사 진행
                if name == "의사일정" or check_keywords(detail_item):
                    detail_item['summary'] = summarize(detail_item)
                    matched_items.append(detail_item)
                
    if matched_items or SEND_EMPTY_MAIL:
        print(f"메일 발송 시도: 발견된 항목 {len(matched_items)}건 (날짜 필터링 결과)")
        send_mail(matched_items, today_str)
    else:
        print(f"{yesterday_str} 이후에 등록된 항목이 없습니다.")

if __name__ == "__main__":
    main()