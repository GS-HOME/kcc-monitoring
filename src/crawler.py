import requests
from bs4 import BeautifulSoup
from src.config import BASE_URL

def get_post_list(board_name, params):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(BASE_URL, params=params, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        posts = []
        # 사이트 구조에 따른 선택자 (방통위 게시판 기준 예시)
        rows = soup.select('table.boardList tbody tr')
        for row in rows:
            cols = row.select('td')
            if len(cols) < 3: continue
            
            link_tag = cols[1].select_one('a')
            title = link_tag.get_text(strip=True)
            link = link_tag['href']
            dept = cols[2].get_text(strip=True)
            date = cols[4].get_text(strip=True)
            has_file = bool(cols[3].select_one('img'))
            
            posts.append({
                'board_name': board_name,
                'title': title,
                'url': f"https://kcc.go.kr{link}",
                'dept': dept,
                'date': date,
                'has_file': has_file
            })
        return posts
    except Exception as e:
        print(f"Error crawling {board_name}: {e}")
        return []

def get_post_detail(item):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        res = requests.get(item['url'], headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        content = soup.select_one('#contents').get_text(strip=True)
        files = []
        file_links = soup.select('.fileList a')
        for f in file_links:
            files.append(f.get_text(strip=True))
        
        item['content'] = content
        item['attachments'] = files
    except:
        item['content'] = ""
        item['attachments'] = []
    return item