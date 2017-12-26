# -*- coding: utf-8 -*-
from projhorus import *
from flask import Flask, jsonify, render_template, request, redirect, Response, flash, session, send_file, abort, send_from_directory
# import db
# from conf import txt, const, cfg
# from tasks import runTask, taskFailed, taskFinished, taskSuccess, taskResult, executeSimulation, execute_simulation
# from projhorus import lib
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
@app.route('/get/zhihu_link')
def zhihu_exec():
    Qlink = request.form.get('Qlink', '')
    Client = zhihu_oauth.ZhihuClient()
    Client.load_token('token.pkl')
    me = Client.me()
    question = Client.question(Qlink)
    with open('question_%s_result.txt' % Qlink,'w') as f:
        for i in question.answers:
            tr4w = TextRank4Keyword()
            tr4w.analyze(text=i.content, lower=True, window=2)
            f.write('<--------------------关键词-------------------->\n')
            for item in tr4w.get_keywords(20, word_min_len=1):
                f.write(str(item.word) +'  '+ str(item.weight)+'\n')
            f.write('<--------------------关键短语-------------------->\n')
            for phrase in tr4w.get_keyphrases(keywords_num=20, min_occur_num=2):
                f.write(phrase+'\n')
    return 1