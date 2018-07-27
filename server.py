#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import simplejson as json
from flask import Flask
# pip install -U flask-cors
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
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

        else:
            return {
                'code':500,'result':'param error'
            }

api.add_resource(performanceCalc, '/performanceCalc')
#  main 入口
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=7187)