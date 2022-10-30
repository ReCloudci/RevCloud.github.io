import requests
import re
import smtplib
from email.mime.text import MIMEText
import pandas as pd
import xlwt
from email.header import Header
import codecs

url = 'http://jw1.hustwenhua.net/jwglxt/cjcx/cjcx_cxXsgrcj.html?doType=query&gnmkdm=N305005&su=210501050094'
header = {
    'Cookie': 'JSESSIONID=DC2D6C604562DBC9BD1FE37801DB037A; '
              'UM_distinctid=18266564b372a4-07d2c60d37ed13-76492e2f-144000-18266564b38f11; '
              'route=a138b0bc9b8717421caf582eaeb7ceb0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 '
                  'Safari/537.36 Edg/107.0.1418.24 '
}
data = {
    "xnm": "2021",
    "xqm": "12",
    "_search": "false",
    "nd": "1667095409650",
    "queryModel.showCount": "15",
    "queryModel.currentPage": "1",
    "queryModel.sortName": "",
    "queryModel.sortOrder": "asc",
    "time": "1"
}

resp = requests.post(url=url, headers=header, data=data)
String = resp.json()

itname = re.compile(r"'kcmc': '(?P<name>.*?)', 'kcxzdm'", re.S)  # 提取课程名称
itcj = re.compile("'bfzcj': '(?P<cj>.*?)', 'bh': '01052103'", re.S)  # 提取成绩
itTeacher = re.compile(" 'jsxm': '(?P<teacher>.*?)', 'jxb_id':", re.S)  # 提取任课老师
course = itname.finditer(str(String))
performance = itcj.finditer(str(String))
teacher = itTeacher.finditer(str(String))

courseList = []
performanceList = []
teacherList = []
for i in course:
    courseList.append(i.group('name'))
for i in performance:
    performanceList.append(i.group('cj'))
for i in teacher:
    teacherList.append(i.group('teacher'))
book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('sheet1', cell_overwrite_ok=True)
col = ('课程名称', '老师', '成绩')
for i in range(0, 3):
    sheet.write(0, i, col[i])
for i in range(0, len(courseList)):
    sheet.write(i + 1, 0, courseList[i])
for i in range(0, len(teacherList)):
    sheet.write(i + 1, 1, teacherList[i])
for i in range(0, len(performanceList)):
    sheet.write(i + 1, 2, performanceList[i])
savepath = 'info.xls'
book.save(savepath)

xd = pd.ExcelFile('info.xls')
df = xd.parse()
html_str = df.to_html(header=True, index=False, col_space=100)
style = '''
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
</head>
<style>
    table{
        border-spacing:0;
    }
    th{
        text-align:center;vertical-align:middle;
    }
    td{
        text-align:center;vertical-align:middle;
    }
</style>
'''
html_str = style + html_str
with codecs.open('123test.html', 'w', 'utf-8') as html_file:
    html_file.write(html_str)

html = html_str

message = MIMEText(html, 'html', 'utf-8')
# 发信方的信息：发信邮箱，QQ 邮箱授权码
from_addr = '2598609717@qq.com'
password = 'xdyggfksymecdjif'
# 收信方邮箱
to_addr = '2429468825@qq.com'
# 发信服务器
smtp_server = 'smtp.qq.com'

# 邮件头信息
message['From'] = from_addr  # 发送者
message['To'] = to_addr  # 接收者
subject = '成绩单'
message['Subject'] = Header(subject, 'utf-8')  # 邮件主题

smtpObj = smtplib.SMTP_SSL("smtp.qq.com", 465)
smtpObj.login(from_addr, password)
smtpObj.sendmail(from_addr, [to_addr], message.as_string())
smtpObj.quit()
print("ok")

