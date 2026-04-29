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
            # 상세 페이지 분석 (날짜 확인 포함)
            detail_item = get_post_detail(p)
            post_date = detail_item.get('date', '1970-01-01')

            # 등록일/작성일이 어제(28일) 또는 오늘(29일)인 경우에만 수집
            if post_date >= yesterday_str:
                if check_keywords(detail_item):
                    detail_item['summary'] = summarize(detail_item)
                    matched_items.append(detail_item)
                
    if matched_items or SEND_EMPTY_MAIL:
        print(f"메일 발송 시도: 발견된 관심 항목 {len(matched_items)}건 (날짜 필터링 결과)")
        send_mail(matched_items, today_str)
    else:
        print(f"{yesterday_str} 이후에 등록된 관심 항목이 없어 메일을 보내지 않았습니다.")

if __name__ == "__main__":
    main()