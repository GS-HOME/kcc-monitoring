import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import time
import random
import ssl
from src.config import RSS_BASE_URL

def get_post_list(board_name, params):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    url_with_params = RSS_BASE_URL + "?" + urllib.parse.urlencode(params)
    
    try:
        time.sleep(random.uniform(3.0, 7.0))
        req = urllib.request.Request(url_with_params, headers=headers)
        context = ssl._create_unverified_context()
        
        with urllib.request.urlopen(req, context=context, timeout=30) as response:
            html = response.read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            
            # 파이썬 리스트 슬라이싱을 이용해 가장 최근 게시글 1개만 추출
            items = soup.find_all('item')[:1]
            
            if not items:
                print(f"[{board_name}] 항목 없음 (응답 길이: {len(html)}바이트, 서버 차단 의심)")
                return []
                
            posts = []
            for item in items:
                title = item.find('title').get_text(strip=True) if item.find('title') else "제목 없음"
                link = item.find('link').get_text(strip=True) if item.find('link') else ""
                
                posts.append({
                    'board_name': board_name,
                    'title': title,
                    'url': link,
                    'content': "",
                    'attachments': []
                })
            print(f"[{board_name}] 최신글 1개 목록 수집 완료")
            return posts
    except Exception as e:
        print(f"[{board_name}] 목록 수집 에러: {e}")
        return []

def get_post_detail(item):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    try:
        time.sleep(random.uniform(4.0, 8.0))
        req = urllib.request.Request(item['url'], headers=headers)
        context = ssl._create_unverified_context()
        
        with urllib.request.urlopen(req, context=context, timeout=30) as response:
            html = response.read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            
            content_area = soup.select_one('.view_con') or soup.select_one('#contents')
            item['content'] = content_area.get_text(strip=True) if content_area else "본문 없음"
            
            files = []
            for f in soup.select('.fileList a'):
                files.append(f.get_text(strip=True))
            item['attachments'] = files
            
            print(f"  -> 상세 데이터 수집 완료: {item['title'][:15]}")
    except Exception as e:
        print(f"  -> 상세 페이지 접속 에러: {e}")
        item['content'] = "접속 에러로 본문 수집 실패"
    return item