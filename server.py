#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
<<<<<<< HEAD
# import pandas as pd
=======
>>>>>>> dev
import simplejson as json
from flask import Flask
# pip install -U flask-cors
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
<<<<<<< HEAD
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
=======
# 物性计算package
# pip install -vvv --pre --trusted-host www.coolprop.dreamhosters.com --find-links http://www.coolprop.dreamhosters.com/binaries/Python/ -U --force-reinstall CoolProp
from CoolProp.CoolProp import PropsSI
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# from bs4 import BeautifulSoup
# import urllib2
# flask-restful api 参数获取
parser = reqparse.RequestParser()
parser.add_argument('fluid',type=str)
parser.add_argument('steaming',type=float)
parser.add_argument('cooling',type=float)
parser.add_argument('overheating',type=float)
parser.add_argument('overcooling',type=float)
>>>>>>> dev
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
<<<<<<< HEAD
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
=======
        steaming = 0.0
        cooling = 0.0
        overheating = 0.0
        overcooling = 0.0
        args = parser.parse_args()
        if args.get('fluid'):
            fluid = args['fluid']
        if args.get('steaming'):
            steaming = args['steaming']
        if args.get('cooling'):
            cooling = args['cooling']
        if args.get('overheating'):
            overheating = args['overheating']   
        if args.get('overcooling'):
            overcooling = args['overcooling']

        if(fluid and steaming and cooling and overheating and overcooling):
            # Get Rou
            # 1. get Ps
            # 2. get Rou
            Ps = PropsSI('P','T',steaming + 273.15,'Q',1,'R22')
            Rou = PropsSI('D','T',steaming + 273.15 + overheating,'P',Ps,'R22')

            # Get Hs
            # 1. get Hs
            Hs = PropsSI('H','T',steaming + 273.15 + overheating,'P',Ps,'R22')

            # Get Hv
            # 1.Get Pd
            # 2.Get Hv
            Pd = PropsSI('P','T',cooling + 273.15,'Q',1,'R22')
            Hv = PropsSI('H','T',cooling + 273.15 - overcooling,'P',Pd,'R22')

            # Get Hd
            # 1.Get S
            # 2.Get Hd
            S = PropsSI('S','T',steaming + 273.15 + overheating,'P',Ps,'R22')
            Hd = PropsSI('H','P',Pd,'S',S,'R22')

            return {
                'code':200,'Ps':Ps,'Rou':Rou,'Hs':Hs,'Pd':Pd,'Hv':Hv,'S':S,'Hd':Hd
            }

>>>>>>> dev
        else:
            return {
                'code':500,'result':'param error'
            }

api.add_resource(performanceCalc, '/performanceCalc')
#  main 入口
if __name__ == '__main__':
<<<<<<< HEAD
    app.run(host="0.0.0.0",port=2552)
=======
    app.run(host="0.0.0.0",port=7187)
>>>>>>> dev
