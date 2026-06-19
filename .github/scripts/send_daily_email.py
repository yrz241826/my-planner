import smtplib, ssl, os, sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

qq_email = os.environ.get('QQ_EMAIL')
auth_code = os.environ.get('QQ_AUTH_CODE')

if not qq_email or not auth_code:
    print('❌ 邮箱配置缺失')
    sys.exit(1)

# 读取今日邮件正文（由 Hermes 生成的可读版本）
plan_path = '06_今日邮件正文.md'
if os.path.exists(plan_path):
    with open(plan_path, 'r', encoding='utf-8') as f:
        plan = f.read()
else:
    plan = '今日暂无计划安排。'

# 构建邮件内容
text_body = plan.replace('*', '').replace('#', '').replace('|', ' ')

html_body = f'''<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="font-family:-apple-system,BlinkMacSystemFont,sans-serif;font-size:14px;color:#222;max-width:800px;margin:20px auto;padding:20px;background:#fff;border:1px solid #e0e0e0;border-radius:6px">
<h2 style="color:#333">📋 Hermes 每日计划</h2>
<pre style="font-family:inherit;white-space:pre-wrap;line-height:1.6">{plan}</pre>
<hr style="border:none;border-top:1px solid #eee;margin:20px 0">
<p style="color:#999;font-size:12px">本邮件由 GitHub Actions · Hermes 自动发送</p>
</body></html>'''

msg = MIMEMultipart('alternative')
msg['From'] = Header('Hermes 每日计划', 'utf-8').encode() + f' <{qq_email}>'
msg['To'] = qq_email
msg['Subject'] = Header('📋 Hermes 每日计划', 'utf-8')

msg.attach(MIMEText(text_body, 'plain', 'utf-8'))
msg.attach(MIMEText(html_body, 'html', 'utf-8'))

context = ssl.create_default_context()
with smtplib.SMTP_SSL('smtp.qq.com', 465, timeout=15, context=context) as server:
    server.login(qq_email, auth_code)
    server.sendmail(qq_email, [qq_email], msg.as_string())

print(f'✅ 每日计划已发送至 {qq_email}')
