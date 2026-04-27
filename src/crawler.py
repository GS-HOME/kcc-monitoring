import requests
from bs4 import BeautifulSoup
import time
import random
from src.config import RSS_BASE_URL

def get_post_list(board_name, params):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }

    try:
        time.sleep(random.uniform(1.0, 2.0))
        # RSS 뷰로 요청
        response = requests.get(RSS_BASE_URL, params=params, headers=headers, timeout=30)
        
        if response.status_code != 200:
            print(f"[{board_name}] RSS 접속 실패: {response.status_code}")
            return []

        # RSS(XML) 파싱
        soup = BeautifulSoup(response.text, 'xml') # lxml-xml 혹은 xml 파서 사용
        items = soup.find_all('item')
        
        if not items:
            # XML 구조가 다를 경우 일반 html 파서로 재시도
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.find_all('item')

        posts = []
        for item in items:
            title = item.find('title').get_text(strip=True) if item.find('title') else ""
            link = item.find('link').get_text(strip=True) if item.find('link') else ""
            date = item.find('pubDate').get_text(strip=True) if item.find('pubDate') else ""
            description = item.find('description').get_text(strip=True) if item.find('description') else ""
            
            posts.append({
                'board_name': board_name,
                'title': title,
                'url': link,
                'date': date,
                'content': description, # RSS는 본문 일부를 포함함
                'attachments': []
            })
            
        print(f"[{board_name}] RSS 통해 {len(posts)}개 수집 성공")
        return posts
    except Exception as e:
        print(f"[{board_name}] RSS 에러: {e}")
        return []

def get_post_detail(item):
    # RSS에서 이미 description을 가져왔으므로 추가 접속 없이 반환 (차단 위험 감소)
    if not item.get('content'):
        item['content'] = "본문 요약 없음 (원문 링크 참조)"
    return item