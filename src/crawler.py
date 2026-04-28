from bs4 import BeautifulSoup
import time
import random
import urllib.parse
from curl_cffi import requests
from src.config import RSS_BASE_URL
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive"
}

# 해외 IP 차단 시 한국 프록시 주소를 입력하십시오. (형식: http://IP:PORT)
# PROXY = {"http": "http://한국프록시IP:포트", "https": "http://한국프록시IP:포트"}
PROXY = None

def get_post_list(board_name, params):
    target_url = params['url']
    try:
        time.sleep(random.uniform(4.0, 8.0))
        response = requests.get(
            target_url, 
            impersonate="chrome116", 
            headers=DEFAULT_HEADERS,
            proxies=PROXY,
            timeout=30, 
            verify=False
        )
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # HTML 웹페이지에서 게시글 목록을 추출하는 로직 (게시판 구조에 맞춰 수정 필수)
        # 추측: 공공기관 게시판은 주로 <tbody> 내의 <tr> 또는 <li> 태그를 사용합니다.
        items = soup.select('table tbody tr') 
        
        if not items:
            print(f"[{board_name}] 게시글 목록을 추출하지 못했습니다. HTML 구조 확인이 필요합니다.")
            return []
            
        posts = []
        for item in items:
            # 추측: 제목이 있는 <a> 태그를 찾습니다. 실제 클래스명으로 변경하십시오.
            a_tag = item.select_one('a') 
            if not a_tag:
                continue
                
            title = a_tag.get_text(strip=True)
            href = a_tag.get('href', '')
            
            # 상대 경로를 절대 경로로 변환
            link = urllib.parse.urljoin(RSS_BASE_URL, href)
            
            posts.append({
                'board_name': board_name, 'title': title, 'url': link,
                'content': "", 'attachments': []
            })
        print(f"[{board_name}] {len(posts)}개 항목 수집 완료")
        return posts
    except Exception as e:
        print(f"[{board_name}] 목록 수집 에러: {e}")
        return []

def get_post_detail(item):
    try:
        time.sleep(random.uniform(5.0, 10.0))
        response = requests.get(
            item['url'], 
            impersonate="chrome116", 
            headers=DEFAULT_HEADERS,
            proxies=PROXY,
            timeout=30, 
            verify=False
        )
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 본문 내용 추출 태그 (실제 게시판 상세페이지의 본문 클래스명으로 변경 필수)
        content_area = soup.select_one('.view_con') or soup.select_one('#contents') or soup.select_one('.board_view')
        item['content'] = content_area.get_text(strip=True) if content_area else "본문 추출 실패"
        
        files = []
        for f in soup.select('.fileList a'):
            files.append(f.get_text(strip=True))
        item['attachments'] = files
        
        print(f"  -> 상세 데이터 수집 완료: {item['title'][:15]}")
    except Exception as e:
        print(f"  -> 상세 페이지 접속 에러: {e}")
        item['content'] = "접속 에러로 본문 수집 실패"
    return item