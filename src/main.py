from datetime import datetime, timedelta
from src.config import BOARDS, SEND_EMPTY_MAIL
from src.crawler import get_post_list, get_post_detail
from src.storage import load_seen, save_seen, get_hash
from src.filter import check_keywords
from src.summarizer import summarize
from src.mailer import send_mail

def main():
    # 중복 방지를 위한 기존 기록 로드
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
            # 상세 페이지 분석 및 날짜 확인
            detail_item = get_post_detail(p)
            post_date = detail_item.get('date', '1970-01-01')

            # 어제 또는 오늘 게시글인 경우에만 진행
            if post_date >= yesterday_str:
                # 의사일정은 무조건 통과, 그 외는 키워드 검사
                if name == "의사일정" or check_keywords(detail_item):
                    # 요약문 생성
                    detail_item['summary'] = summarize(detail_item)
                    
                    # [중요] 요약문 내용을 기반으로 해시 생성 (URL 변경에 영향받지 않음)
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
        
    # 새로운 해시 목록 저장
    save_seen(new_seen_hashes)

if __name__ == "__main__":
    main()