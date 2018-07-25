#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# import pandas as pd
import simplejson as json
from flask import Flask
# pip install -U flask-cors
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from bs4 import BeautifulSoup
import urllib2
# flask-restful api 参数获取
parser = reqparse.RequestParser()
parser.add_argument('fluid',type=str)
parser.add_argument('name1',type=str)
parser.add_argument('name2',type=str)
parser.add_argument('value1',type=float)
parser.add_argument('value2',type=float)
# def get_url_args(args):
#     return args

# 启动app
app = Flask(__name__)
CORS(app)
api = Api(app)

# flask-restful api 设置
class performanceCalc(Resource):
    def get(self):
        fluid = ''
        name1 = ''
        name2 = ''
        value1 = 0.0
        value2 = 0.0
        args = parser.parse_args()
        if args.get('fluid'):
            fluid = args['fluid']
        if args.get('name1'):
            name1 = args['name1']
        if args.get('name2'):
            name2 = args['name2']
        if args.get('value1'):
            value1 = args['value1']   
        if args.get('value2'):
            value2 = args['value2']

        if(fluid and name1 and name2 and value1 and value2):
            params = {'fluid':fluid,'name1':name1,'name2':name2,'value1':value1,'value2':value2}
            fullUrl = 'http://ibell.pythonanywhere.com/next?fluid=%s&name1=%s&name2=%s&unit_system=Mass-based&value1=%f&value2=%f#' % (fluid,name1,name2,value1,value2)
            # 读取HTML内容
            req = urllib2.Request(fullUrl)
            res = urllib2.urlopen(req)
            html = res.read()
            res.close()
            # HTML美化
            html=BeautifulSoup(html,'html.parser')
            # 提取数据，转为json
            datalist = [data.string for data in html.select('td')]
            result = dict(zip(datalist[0::2],datalist[1::2]))
            # result = json.dumps(result,ensure_ascii=False)
            return {
                'code':res.code,'params':params,'fullUrl':fullUrl,'result':result
            }
        else:
            return {
                'code':500,'result':'param error'
            }

api.add_resource(performanceCalc, '/performanceCalc')
#  main 入口
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=2552)