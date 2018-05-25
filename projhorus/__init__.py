# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, request, redirect, Response, flash, session, send_file, abort, send_from_directory
# import db
# from conf import txt, const, cfg
# from tasks import runTask, taskFailed, taskFinished, taskSuccess, taskResult, executeSimulation, execute_simulation
# from projhorus import lib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import json
import requests
import pytz
from io import BytesIO
import time
import os
from flask_sslify import SSLify
import re
import openpyxl
import difflib
import cache
import base64
from bson.objectid import ObjectId
import datetime
import urllib3
import zhihu_oauth
import bs4 as BeautifulSoup
from textrank4zh import TextRank4Keyword
import newspaper

FLAG = ''
def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = os.urandom(24).encode('hex') 
    return session['_csrf_token']


def check_csrf_token(req):
    token = session.pop('_csrf_token', None)
    if not token or token != req.form.get('_csrf_token'):
        abort(403)


def check_ajax_csrf_token(req):
    token = session.pop('_csrf_token', None)
    return token and token == req.form.get('_csrf_token')


app = Flask(__name__)
app.debug = bool(int(os.environ.get('DEBUG', '0')))
SSLify(app, subdomains=True)
app.secret_key = 'xinpeng2o!s'  # os.urandom(24)
app.config['SESSION_COOKIE_SECURE'] = not app.debug
app.config['PERMANENT_SESSION_LIFE_TIME'] = 1800
app.jinja_env.globals['csrf_token'] = generate_csrf_token

tz = pytz.timezone('Asia/Shanghai')

# import projhorus.user

@app.after_request
def finish_headers(response):
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    return response

@app.route('/')
def index():
    global FLAG
    print (FLAG)
    return render_template('index.html',
                    flag = FLAG)

@app.route('/get/zhihu_link', methods=['POST'])
def zhihu_exec():
    Qlink = request.form.get('Qlink', '')
    Client = zhihu_oauth.ZhihuClient()
    Client.load_token('token.pkl')
    me = Client.me()
    question = Client.question(int(Qlink))
    with open(os.path.join(os.path.join('projhorus','static'),'question_%s_result.txt' % Qlink),'w') as f:
        for i in question.answers:
            tr4w = TextRank4Keyword()
            tr4w.analyze(text=i.content, lower=True, window=2)
            f.write(u'<--------------------关键词-------------------->\n')
            for item in tr4w.get_keywords(20, word_min_len=1):
                f.write(str(item.word) +'  '+ str(item.weight)+'\n')
            f.write(u'<--------------------关键短语-------------------->\n')
            for phrase in tr4w.get_keyphrases(keywords_num=20, min_occur_num=2):
                f.write(phrase+'\n')
    global FLAG
    FLAG = '/static/question_%s_result.txt' % Qlink
    return redirect('/')

@app.route('/robots.txt')
def serve_robots_txt():
    return send_from_directory(app.static_folder, 'robots.txt')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True, port=80)
