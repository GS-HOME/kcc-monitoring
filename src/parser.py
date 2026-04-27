from bs4 import BeautifulSoup

def parse_list(html, board_name):
    soup = BeautifulSoup(html, 'html.parser')
    posts = []
    rows = soup.select('table.boardList tbody tr')
    
    for row in rows:
        cols = row.select('td')
        if len(cols) < 5: continue
        
        # 제목 및 링크 추출
        a_tag = cols[1].select_one('a')
        if not a_tag: continue
        
        title = a_tag.get_text(strip=True)
        link = a_tag['href']
        dept = cols[2].get_text(strip=True)
        date = cols[4].get_text(strip=True)
        # 첨부파일 아이콘 존재 여부
        has_file = "유" if cols[3].select_one('img') else "무"
        
        posts.append({
            'board_name': board_name,
            'title': title,
            'url': f"https://kcc.go.kr{link}" if link.startswith('/') else link,
            'dept': dept,
            'date': date,
            'has_file': has_file
        })
    return posts

def parse_detail(html):
    soup = BeautifulSoup(html, 'html.parser')
    # 방통위 상세페이지 본문 영역 선택자 (사이트 구조에 따라 조정 필요)
    content_area = soup.select_one('#contents') 
    content_text = content_area.get_text(strip=True) if content_area else "본문 없음"
    
    files = []
    file_tags = soup.select('.fileList a')
    for f in file_tags:
        files.append(f.get_text(strip=True))
        
    return content_text, files