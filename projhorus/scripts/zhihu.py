import zhihu_oauth
import bs4 as BeautifulSoup
from textrank4zh import TextRank4Keyword
import requests
import newspaper
from wordcloud import WordCloud as wd
import matplotlib.pyplot as plt

Client = zhihu_oauth.ZhihuClient()
Client.load_token('token.pkl')
me = Client.me()
question = Client.question(27852694)
with open('question_27852694_result.txt','w') as f:
    for i in question.answers:
        tr4w = TextRank4Keyword()
        tr4w.analyze(text=i.content, lower=True, window=2)
        f.write('<--------------------关键词-------------------->\n')
        for item in tr4w.get_keywords(20, word_min_len=1):
            f.write(str(item.word) +'  '+ str(item.weight)+'\n')
        f.write('<--------------------关键短语-------------------->\n')
        for phrase in tr4w.get_keyphrases(keywords_num=20, min_occur_num=2):
            f.write(phrase+'\n')
