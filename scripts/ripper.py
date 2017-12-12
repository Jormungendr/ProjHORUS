

import requests
import newspaper
from bs4 import BeautifulSoup
from textrank4zh import TextRank4Keyword
url = 'http://news.baidu.com/ns?word=%E7%BA%A2%E9%BB%84%E8%93%9D&tn=news&from=news&cl=2&rn=20&ct=1'
headers = {
    'Cookie': 'BIDUPSID=961C93A7CFBBEC9E4B9144374A8E859C; PSTM=1500556476; BAIDUID=961C93A7CFBBEC9E4B9144374A8E859C:SL=0:NR=50:FG=1; __cfduid=d174b5a5af92633cc76a55e30006ac0a01504841743; MCITY=-%3A; SFSSID=eh03n8id6u5rdpc5vod14hh0g1; uc_login_unique=35e59f50df5df016ffe598979acb8455; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a02587503199; uc_recom_mark=cmVjb21tYXJrXzI0NDgxMDk0; locale=zh; BDRCVFR[C0p6oIjvx-c]=mk3SLVN4HKm; BD_CK_SAM=1; PSINO=1; BDSVRTM=265; H_PS_PSSID=',
    'Host': 'news.baidu.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
r = requests.get(url=url, headers=headers)
r.encoding = 'utf8'
soup = BeautifulSoup(r.text, 'lxml')
urls = [i.find('a').get('href') for i in soup.find(
    'div', {'id': 'content_left'}).find_all('h3', {'class': 'c-title'})]
for i in urls:
    a = newspaper.Article(i, language='zh')
    a.download()
    a.parse()
    text = a.text
    tr4w = TextRank4Keyword()
    tr4w.analyze(text=text, lower=True, window=2)
    print('<--------------------关键词-------------------->')
    for item in tr4w.get_keywords(20, word_min_len=1):
        print(item.word, item.weight)
    print('<--------------------关键短语-------------------->')
    for phrase in tr4w.get_keyphrases(keywords_num=20, min_occur_num=2):
        print(phrase)