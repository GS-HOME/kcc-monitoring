import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import time
import random
import ssl
from src.config import RSS_BASE_URL

def get_post_list(board_name, params):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    
    url_with_params = RSS_BASE_URL + "?" + urllib.parse.urlencode(params)
    
    try:
        time.sleep(random.uniform(5.0, 15.0))
        
        req = urllib.request.Request(url_with_params, headers=headers)
        context = ssl._create_unverified_context()
        
        with urllib.request.urlopen(req, context=context, timeout=30) as response:
            html = response.read().decode('utf-8')
            
            soup = BeautifulSoup(html, 'html.parser')
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
    except Exception as e:
        print(f"[{board_name}] 수집 중 에러: {e}")
        return []

def get_post_detail(item):
    return item