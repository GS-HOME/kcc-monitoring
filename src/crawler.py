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
        time.sleep(random.uniform(2.0, 4.0))
        with requests.Session() as session:
            response = session.get(RSS_BASE_URL, params=params, headers=headers, timeout=30)
            if response.status_code != 200:
                print(f"[{board_name}] 접속 실패: {response.status_code}")
                return []

            # lxml 파서를 사용하여 XML 데이터 해석
            soup = BeautifulSoup(response.text, 'lxml')
            items = soup.find_all('item')
            
            posts = []
            for item in items:
                title = item.find('title').get_text(strip=True) if item.find('title') else "제목 없음"
                link = item.find('link').get_text(strip=True) if item.find('link') else ""
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
        print(f"[{board_name}] 수집 중 에러: {e}")
        return []

def get_post_detail(item):
    return item