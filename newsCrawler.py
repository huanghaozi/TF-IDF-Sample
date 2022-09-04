import requests
import lxml.html
from datetime import datetime
from datetime import timedelta

# 获取新闻联播文字版HTML字符串
# 数据源：http://mrxwlb.com
def get_news_html(date):
    url = 'http://mrxwlb.com/{}新闻联播文字版/'.format(date)
    response = requests.get(url)
    return response.text


# 从HTML提取正文内容
def extract_content(htmlStr):
    tree = lxml.html.fromstring(htmlStr)
    content = tree.xpath('//section[@class="entry-content"]/p/text()')
    return '\n'.join(content)

# 写入文本文件
def  write_to_txt(filename, content):
    with open('data/{}.txt'.format(filename), 'w', encoding='utf-8') as f:
        f.write(content)

startDate = datetime(2022, 8, 1)
endDate = datetime(2022, 9, 1)

currentDate = startDate
while not currentDate.strftime('%Y-%m-%d') == endDate.strftime('%Y-%m-%d'):
    date = '{}年{}月{}日'.format(currentDate.year, currentDate.month, currentDate.day)
    html = get_news_html(date)
    content = extract_content(html)
    write_to_txt(date, content)
    currentDate = currentDate + timedelta(days=1)
