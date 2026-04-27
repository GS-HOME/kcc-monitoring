import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src.config import *

def send_mail(items, date_str):
    if not items and not SEND_EMPTY_MAIL:
        return
    
    count = len(items)
    subject = f"[방미통위 모니터링] {date_str} 신규 관심자료 {count}건"
    
    html = f"<h2>{date_str} 모니터링 결과</h2>"
    if count == 0:
        html += "<p>신규 관심자료가 없습니다.</p>"
    else:
        for it in items:
            html += f"<div style='border:1px solid #ddd; padding:10px; margin-bottom:10px;'>"
            html += f"<h3>[{it['board_name']}] {it['title']}</h3>"
            html += f"<p>요약: {it['summary']}</p>"
            html += f"<p><a href='{it['url']}'>원문 보기</a></p></div>"

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = MAIL_TO
    msg.attach(MIMEText(html, 'html'))
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_APP_PASSWORD)
            server.sendmail(SMTP_USER, MAIL_TO, msg.as_string())
    except Exception as e:
        print(f"Mail Error: {e}")