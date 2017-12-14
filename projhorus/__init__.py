# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, request, redirect, Response, flash, session, send_file, abort, send_from_directory
# import db
# from conf import txt, const, cfg
# from tasks import runTask, taskFailed, taskFinished, taskSuccess, taskResult, executeSimulation, execute_simulation
# import lib
import json
import requests
import pytz
from io import BytesIO
import time
import jwt
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
    if not lib.is_im_staff(session):
        if session.get(const.SESSION_COMPANY[0], '') == 'mundi' or session.get(const.SESSION_COMPANY[0], '') == 'mundi-test':
            if lib.is_employee(session):
                return redirect('/appeal')
            else:
                return redirect('/signin')
        if lib.is_employee(session):
            return redirect('/search')
        else:
            return redirect('/signin')
    events = []  # db.get_calc_events(session.get(const.SESSION_USERNAME[0], ''))
    event_cnt = {}
    for evt in events:
        if evt['start'] not in event_cnt:
            event_cnt[evt['start']] = 0
        event_cnt[evt['start']] += 1
    today = lib.now_date()
    latest_policy = [p for p in db.get_latest_policies(session.get(const.SESSION_USERNAME[0], ''))]
    latest_kpi = [k for k in db.get_latest_kpis(session.get(const.SESSION_USERNAME[0], ''))]
    latest_data = []
    r = requests.get(lib.data_api(cfg.DATA_API_ALLVERSIONS,
                                  session.get(const.SESSION_COMPANY[0], ''),
                                  session.get(const.SESSION_ENV[0], '')), verify=False)
    if r.status_code == 200 and r.json().get('success', False):
        latest_data = r.json().get('data', [])[:6] 
    else:
        print ('Get latest data fail: [%d]%s' % (r.status_code, r.json().get('message', '')))
    status = db.get_status(session.get(const.SESSION_USERNAME[0], ''))
    statistic = {k: status[k] if status and k in status else 0 for k in const.INDEX_STATISTIC}
    quota = [] 
    quota_data = db.get_quota(session.get(const.SESSION_COMPANY[0], ''))
    for qn in const.QUOTA_DISPLAY:
        this_qt = quota_data.get(qn, {}).get(session.get(const.SESSION_ENV[0], ''), {})
        this_qt['label'] = const.QUOTA_LABEL.get(qn, '')
        this_qt['bar_used'] = {'class': 'info', 'width': '0'}
        this_qt['bar_remain'] = {'class': 'success'}
        # No limit
        if this_qt['limit'] < 0:
            this_qt['note'] = '%d / &infin;' % this_qt['usage']
        # Has limit
        else:
            this_qt['note'] = '%d / %d' % (this_qt['usage'], this_qt['limit'])
            use_rate = 1 if this_qt['limit'] == 0 else float(this_qt['usage']) / float(this_qt['limit'])
            if use_rate > 1:
                use_rate = 1
            this_qt['bar_used']['width'] = '%d%%' % (use_rate * 100)
            if use_rate > 0.7:
                this_qt['bar_used']['class'] = 'danger'
                
        quota.append(this_qt)
    return render_template('index.html',
                           today=lib.now_date(),
                           policies=latest_policy,
                           kpis=latest_kpi,
                           data=latest_data,
                           events=events,
                           event_cnt=event_cnt,
                           events_display=[event for event in events if event['start'][:7] == today[:7]],
                           statistic=statistic,
                           quota=quota,
                           status_class=const.POLICY_STATUS_CLASS,
                           STATISTIC_EMPLOYEE=const.STATISTIC_EMPLOYEE,
                           STATISTIC_PAYOUT=const.STATISTIC_PAYOUT,
                           STATISTIC_POSTPONED=const.STATISTIC_POSTPONED,
                           STATISTIC_ACCURATE=const.STATISTIC_ACCURATE,
                           STATISTIC_POLICY=const.STATISTIC_POLICY,
                           STATISTIC_DATA=const.STATISTIC_DATA,
                           STATISTIC_KPI=const.STATISTIC_KPI,
                           STATISTIC_REPORT=const.STATISTIC_REPORT,
                           nodata=txt.NO_DATA_HTML)


@app.route('/robots.txt')
def serve_robots_txt():
    return send_from_directory(app.static_folder, 'robots.txt')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True, port=5000)
