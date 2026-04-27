import requests
from bs4 import BeautifulSoup
import time
import random
from src.config import RSS_BASE_URL

def get_post_list(board_name, params):
    # 실제 최신 크롬 브라우저와 동일한 헤더
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    try:
        # 서버 부하 방지를 위해 랜덤 지연 시간 증가
        time.sleep(random.uniform(3.0, 6.0))
        
        with requests.Session() as session:
            # 세션을 유지하며 요청
            response = session.get(RSS_BASE_URL, params=params, headers=headers, timeout=30)
            
            if response.status_code != 200:
                print(f"[{board_name}] 접속 실패: {response.status_code}")
                return []

            # lxml 엔진을 명시적으로 사용하여 파서 에러 방지
            # 설치가 안 되어 있을 경우를 대비해 html.parser를 백업으로 사용
            try:
                soup = BeautifulSoup(response.text, 'lxml')
            except:
                soup = BeautifulSoup(response.text, 'html.parser')
                
            items = soup.find_all('item')
            
            posts = []
            for item in items:
                title = item.find('title').get_text(strip=True) if item.find('title') else "제목 없음"
                link = item.find('link').get_text(strip=True) if item.find('link') else ""
                # pubDate 대소문자 구분 없이 대응
                date_tag = item.find('pubDate') or item.find('pubdate')
                date = date_tag.get_text(strip=True) if date_tag else ""
                desc = item.find('description').get_text(strip=True) if item.find('description') else ""
                
                posts.append({
                    'board_name': board_name,
                    'title': title,
                    'url': link,
                    'date': date,
                    'content': desc,
                    'attachments': []
                })
                
            print(f"[{board_name}] {len(posts)}개 항목 수집 성공")
            return posts
            
    except Exception as e:
        print(f"[{board_name}] RSS 수집 중 에러: {e}")
        return []

def get_post_detail(item):
    # 상세 페이지 접속 시 차단 위험이 크므로 RSS 본문을 우선 활용
    return item