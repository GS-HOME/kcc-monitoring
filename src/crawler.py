from bs4 import BeautifulSoup
import time
import random
import urllib.parse
from curl_cffi import requests
from src.config import RSS_BASE_URL

def get_post_list(board_name, params):
    url_with_params = RSS_BASE_URL + "?" + urllib.parse.urlencode(params)
    
    try:
        # 서버 부하를 줄이고 봇 탐지를 피하기 위한 대기 시간
        time.sleep(random.uniform(4.0, 8.0))
        
        # impersonate="chrome110" 옵션으로 최신 크롬 브라우저의 통신 지문을 완벽히 모방
        response = requests.get(url_with_params, impersonate="chrome110", timeout=30)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('item')
        
        if not items:
            print(f"[{board_name}] 항목을 찾을 수 없습니다. (응답 크기: {len(response.text)}바이트)")
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
        print(f"[{board_name}] {len(posts)}개 항목 수집 완료")
        return posts
    except Exception as e:
        print(f"[{board_name}] 목록 수집 에러: {e}")
        return []

def get_post_detail(item):
    try:
        time.sleep(random.uniform(5.0, 10.0))
        # 상세 페이지 접속 시에도 크롬 브라우저 위장 유지
        response = requests.get(item['url'], impersonate="chrome110", timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        content_area = soup.select_one('.view_con') or soup.select_one('#contents')
        item['content'] = content_area.get_text(strip=True) if content_area else "본문 없음"
        
        files = []
        for f in soup.select('.fileList a'):
            files.append(f.get_text(strip=True))
        item['attachments'] = files
        
        print(f"  -> 상세 데이터 수집 완료: {item['title'][:15]}...")
    except Exception as e:
        print(f"  -> 상세 페이지 접속 에러: {e}")
        item['content'] = "접속 에러로 본문 수집 실패"
    return item