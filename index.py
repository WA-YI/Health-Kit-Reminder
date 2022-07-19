import json
import time
import ntplib
import requests
from urllib import parse
from datetime import datetime, timezone

#全局变量按需修改
push = '已经'+str(hsDay)+'天没做核酸了' #企业微信PUSH文本
corp_id = '' #企业微信ID
corp_secret = '' #企业微信机器人密钥
agent_id = '' #企业微信机器人ID
personToken = '' #北京通打开小程序时认证URL中的personToken

#获取当前时间
client = ntplib.NTPClient()
response = client.request('ntp.aliyun.com')
now = datetime.fromtimestamp(response.tx_time).date()

#请求小程序Token
urlLogin = "https://bjt.beijing.gov.cn/renzheng/open/auth/authorize?client_id=100100000364&redirect_uri=https://static.beijingtoon.com/cstoon-health-query/m/index.html&response_type=code&scope=user_info&state=&toonType=102&personToken="+personToken+"&toonType=102"
urlMiniToken = "https://bjt.beijing.gov.cn/renzheng/inner/auth/getClientInfo"
token = requests.session()
tokenRes = token.head(urlLogin, stream=True)
if(tokenRes.status_code == 302):
    loginRes = token.post(urlMiniToken)
    loginJson = json.loads(loginRes.text)
    session = parse.parse_qs(parse.urlparse(loginJson['data']['redirectUrl']).query)['code'][0]
    print(session)
else:
    print("请求App Token失败!")
    exit()

#请求健康宝Token
urlHealthToken = 'https://service.beijingtoon.com/cstoon-health-query/session/getSessionId'
sessionJson = {"code":session,"toonType":"102"}
healthReq = requests.post(urlHealthToken,data=json.dumps(sessionJson),headers={'Content-Type':'application/json'})
if(healthReq.status_code == 200):
    healthJson = json.loads(healthReq.text)
    session = healthJson['data']['sessionId']
    print(session)
else:
    print("请求健康宝Token失败!")
    exit()

#请求核酸信息
urlHS = 'https://service.beijingtoon.com/cstoon-health-query/newHs/selNewHs'
hsReqJson = {"refresh":0,"selectType":1}
hsReq = requests.post(urlHS,data=json.dumps(hsReqJson),headers={'Content-Type':'application/json','sessionId':session})
if(hsReq.status_code == 200):
    hsJson = json.loads(hsReq.text)
    lastHs = hsJson['data']['detTime']
    lastHs = datetime.strptime(lastHs,'%Y-%m-%d %H:%M:%S').date()
    hsDay = (now-lastHs).days
else:
    print("请求核酸结果失败!")
    exit()

#发送微信企业消息
if(hsDay>=3):
    def get_access_token(corp_id, corp_secret):
        resp = requests.get(f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corp_id}&corpsecret={corp_secret}')
        js = json.loads(resp.text)
        print(js)
        if js["errcode"] == 0:
            access_token = js["access_token"]
            expires_in = js["expires_in"]
            return access_token, expires_in

    def wechat_push_text(agent_id, access_token, message):
        data = {
            "touser": "qy01e335e7bbc976002a8aa93f6c",
            "msgtype": 'text',
            "agentid": agent_id,
            "text": {
                "content": message
            },
            "safe": 0,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        resp = requests.post(f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}', json=data)
        js = json.loads(resp.text)
        print(js)
        if js["errcode"] == 0:
            return js

    access_token, expires_in = get_access_token(corp_id, corp_secret)
    wechat_push_text(agent_id=agent_id, access_token=access_token, message=push)
