from bs4 import BeautifulSoup
import time
import random
import urllib.parse
from curl_cffi import requests
from src.config import RSS_BASE_URL
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive"
}

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
        items = soup.select('table tbody tr') 
        
        if not items:
            print(f"[{board_name}] 게시글 목록 추출 실패")
            return []
            
        posts = []
        for item in items:
            a_tag = item.select_one('a') 
            title = a_tag.get_text(strip=True) if a_tag else "제목 없음"
            
            # 링크가 없는 경우(심결정보 등) 처리
            href = a_tag.get('href', '') if a_tag else ""
            link = urllib.parse.urljoin(RSS_BASE_URL, href) if href else target_url
            
            # 리스트 페이지에 날짜가 보이는 경우 미리 추출 시도 (YYYY-MM-DD 형식)
            list_date_match = re.search(r'\d{4}-\d{2}-\d{2}', item.get_text())
            list_date = list_date_match.group(0) if list_date_match else None

            posts.append({
                'board_name': board_name, 'title': title, 'url': link,
                'content': "", 'attachments': [], 'date': list_date
            })
        print(f"[{board_name}] {len(posts)}개 항목 수집 완료")
        return posts
    except Exception as e:
        print(f"[{board_name}] 목록 수집 에러: {e}")
        return []

def get_post_detail(item):
    # 이미 리스트에서 날짜를 찾았고, 상세 링크가 리스트 페이지와 같다면(클릭 불가 게시판) 상세 접속 생략
    if item.get('date') and item['url'].endswith('boardId=1119'): # 심결정보 boardId 기준
        print(f"  -> [심결정보] 리스트 데이터 사용 (작성일: {item['date']}): {item['title'][:15]}")
        return item

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
        
        content_area = soup.select_one('.view_con') or soup.select_one('#contents') or soup.select_one('.board_view')
        raw_text = content_area.get_text(strip=True) if content_area else soup.get_text(strip=True)
        
        # "제목" 이후 텍스트 분리
        content_after_title = raw_text.split("제목", 1)[1] if "제목" in raw_text else raw_text

        # "등록일" 또는 "작성일" 뒤의 날짜 추출
        date_match = re.search(r'(등록일|작성일).*?(\d{4}-\d{2}-\d{2})', content_after_title)
        if date_match:
            item['date'] = date_match.group(2)
        elif not item.get('date'):
            # 리스트에서도 못 찾았고 상세에서도 키워드가 없으면 날짜 형식만 단독 추출
            backup_match = re.search(r'(\d{4}-\d{2}-\d{2})', raw_text)
            item['date'] = backup_match.group(1) if backup_match else "1970-01-01"

        item['content'] = content_after_title.strip()
        
        files = []
        for f in soup.select('.fileList a'):
            files.append(f.get_text(strip=True))
        item['attachments'] = files
        
        print(f"  -> 상세 데이터 수집 완료 (날짜: {item['date']}): {item['title'][:15]}")
    except Exception as e:
        print(f"  -> 상세 페이지 접속 에러: {e}")
        if not item.get('date'): item['date'] = "1970-01-01"
    return item