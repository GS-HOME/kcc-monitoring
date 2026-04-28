import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src.config import *

def send_mail(items, date_str):
    if not items and not SEND_EMPTY_MAIL:
        return
    
    count = len(items)
    subject = f"[방통위 모니터링] {date_str} 신규 자료 {count}건"
    
    html = f"<h2>{date_str} 모니터링 결과 (총 {count}건)</h2>"
    if count == 0:
        html += "<p style='color:red;'>새로운 관심 키워드 자료가 없습니다.</p>"
    else:
        for it in items:
            summary = it.get('content', '')[:200]
            html += f"<div style='border:1px solid #ddd; padding:15px; margin-bottom:15px; border-left:5px solid #0055ff;'>"
            html += f"<h3>[{it['board_name']}] {it['title']}</h3>"
            html += f"<p>{summary}...</p>"
            html += f"<p><a href='{it['url']}'>원문 바로가기</a></p></div>"

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = MAIL_TO
    msg.attach(MIMEText(html, 'html'))
    
    try:
        # 기존에 정상 작동하던 587 포트 방식으로 원복
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_APP_PASSWORD)
            server.sendmail(SMTP_USER, MAIL_TO, msg.as_string())
            print(f"메일 발송 성공! (수신: {MAIL_TO})")
    except Exception as e:
        print(f"Mail Error: {e}")