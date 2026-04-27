import requests
from bs4 import BeautifulSoup
import time
import random
from src.config import BASE_URL

def get_post_list(board_name, params):
    # 실제 크롬 브라우저와 거의 동일한 헤더 설정
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://kcc.go.kr/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
    }

    session = requests.Session()
    
    try:
        # 서버 부하 방지 및 차단 회피를 위한 랜덤 지연 (1~3초)
        time.sleep(random.uniform(1.0, 3.0))
        
        response = session.get(BASE_URL, params=params, headers=headers, timeout=30)
        
        if response.status_code != 200:
            print(f"[{board_name}] 접속 실패: {response.status_code}")
            return []
            
        soup = BeautifulSoup(response.text, 'html.parser')
        posts = []
        
        # 선택자 재검증: 방통위 게시판 구조
        rows = soup.select('table.boardList tbody tr')
        if not rows:
            # 게시글이 없는 경우 혹은 선택자 문제일 때 로그 출력
            print(f"[{board_name}] 게시글 행(tr)을 찾을 수 없습니다. (구조 변경 확인 필요)")
            return []

        for row in rows:
            cols = row.select('td')
            # '데이터가 없습니다' 메시지 처리
            if len(cols) < 3: continue
            
            a_tag = cols[1].select_one('a')
            if not a_tag: continue
            
            title = a_tag.get_text(strip=True)
            link = a_tag['href']
            dept = cols[2].get_text(strip=True)
            # 날짜 컬럼 위치 유동적 대응
            date = cols[-1].get_text(strip=True) if len(cols) >= 5 else "0000-00-00"
            
            posts.append({
                'board_name': board_name,
                'title': title,
                'url': f"https://kcc.go.kr{link}" if link.startswith('/') else link,
                'dept': dept,
                'date': date,
                'attachments': []
            })
        
        print(f"[{board_name}] {len(posts)}개의 게시글 수집 성공")
        return posts

    except Exception as e:
        print(f"[{board_name}] 연결 오류 발생: {e}")
        return []

def get_post_detail(item):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    }
    try:
        time.sleep(random.uniform(0.5, 1.5))
        res = requests.get(item['url'], headers=headers, timeout=30)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        content_area = soup.select_one('.view_con') or soup.select_one('#contents')
        item['content'] = content_area.get_text(strip=True) if content_area else "본문 내용을 읽을 수 없습니다."
        
        files = []
        file_links = soup.select('.fileList a')
        for f in file_links:
            files.append(f.get_text(strip=True))
        item['attachments'] = files
    except:
        item['content'] = "상세 페이지 접속 오류"
        item['attachments'] = []
    return item