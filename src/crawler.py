import requests
from bs4 import BeautifulSoup
import time
import random
import urllib3
from src.config import RSS_BASE_URL

# SSL 경고 무시
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_post_list(board_name, params):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }
    
    # 에러 발생 시 최대 3번까지 다시 시도
    for i in range(3):
        try:
            # 게시판별로 요청 간격을 다르게 하여 차단 회피 (5~12초)
            time.sleep(random.uniform(5.0, 12.0))
            
            response = requests.get(RSS_BASE_URL, params=params, headers=headers, timeout=40, verify=False)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                items = soup.find_all('item')
                
                posts = []
                for item in items:
                    title = item.find('title').get_text(strip=True) if item.find('title') else "제목 없음"
                    link = item.find('link').get_text(strip=True) if item.find('link') else ""
                    desc = item.find('description').get_text(strip=True) if item.find('description') else ""
                    
                    posts.append({
                        'board_name': board_name,
                        'title': title,
                        'url': link,
                        'content': desc,
                        'attachments': []
                    })
                print(f"[{board_name}] {len(posts)}개 항목 수집 완료")
                return posts
            else:
                print(f"[{board_name}] 시도 {i+1}: 접속 실패({response.status_code})")
                
        except Exception as e:
            print(f"[{board_name}] 시도 {i+1} 에러: {e}")
            # 에러 발생 시 대기 시간을 늘림
            time.sleep(10)
            
    return []

def get_post_detail(item):
    return item