#!/usr/bin/python
# -*- coding: utf-8 -*-
import xmpp
import urllib2,urllib
import simplejson as json
import utils.db as db
import pywapi
import xml

def init(bot):
  db.execNonQuery(bot.dbpath,"CREATE TABLE IF NOT EXISTS picture_cash(path text, img_base64 text, ext text, PRIMARY KEY(path))")
  return 10

def description():
  return 'прогноз погоды'
  
def help():
  txt = 'Прогноз погоды(v0.2)\n\n'
  return txt

proxy_enabled = True

class ProxyPasswordMgr:    
 def __init__(self):        
    self.user = self.passwd = None    
 def add_password(self, realm, uri, user, passwd):
    self.user = user        
    self.passwd = passwd    
 def find_user_password(self, realm, authuri): 
    return self.user, self.passwd
 
  
def run(bot,mess):
    text = mess.getBody()
    text = text[len('gweather')+1:]
    user = mess.getFrom()
    user=str(user).split('/')[0]
    if text:
        if proxy_enabled:
            proxy = "128.0.20.5:80"
            user = "ИсуповА"
            password = "Fylhtq"
            proxy = urllib2.ProxyHandler({"http" : proxy})
            proxy_auth_handler = urllib2.ProxyBasicAuthHandler(ProxyPasswordMgr())
            proxy_auth_handler.add_password(None, None, user, password)
            opener = urllib2.build_opener(proxy,proxy_auth_handler)
            urllib2.install_opener(opener)

        result = pywapi.get_weather_from_google(text.encode('utf-8'), 'ru')
        reply = result['forecast_information']['city'].encode('utf-8')+ '(need xep-0071)'
        message=xmpp.protocol.Message(mess.getFrom(), reply)
        img=getAvatar(bot,'http://www.google.com'+ result['current_conditions']['icon'].encode('utf-8'))
        curr = 'Погода в %s<br/><table><tr><td><img src="data:image/%s;base64,%s" alt="img"/></td><td><strong>%s</strong>С <br/>%s<br/>%s<br/>%s</td></tr></table>' % (\
                 result['forecast_information']['city'].encode('utf-8'),\
                 img['ext'].encode('utf-8'),img['img'].encode('utf-8'),\
                 result['current_conditions']['temp_c'].encode('utf-8'),\
                 result['current_conditions']['condition'].encode('utf-8'),\
                 result['current_conditions']['humidity'].encode('utf-8'),\
                 result['current_conditions']['wind_condition'].encode('utf-8'))
        prognoz = '<p><b>Прогноз</b></p><table>'
        for day in result['forecasts']:
            img=getAvatar(bot,'http://www.google.com'+day['icon'].encode('utf-8'))
            prognoz = prognoz + '<tr><td><img src="data:image/%s;base64,%s" alt="img"/></td><td>%s %sC/%sС %s </td></tr>' % (\
                 img['ext'].encode('utf-8'),img['img'].encode('utf-8'),\
                 day['day_of_week'].encode('utf-8'),\
                 day['low'].encode('utf-8'),\
                 day['high'].encode('utf-8'),\
                 day['condition'].encode('utf-8'),)
        prognoz = prognoz + '</table>'
        current_conditions=xmpp.simplexml.XML2Node('<body xmlns="%s">%s%s</body>' %
                ('http://www.w3.org/1999/xhtml',curr,prognoz))
        message.addChild('html', {}, [current_conditions], xmpp.NS_XHTML_IM)
        return message
    else:
        txt = help()
        return xmpp.Message(mess.getFrom(),txt,typ='chat')

def getAvatar(bot,path):
        img = ''
        ext =''
        extl = path.split('.')
        for i in extl:
            ext=i
        try:
            print 1
            find = db.execQuery(bot.dbpath,"select path,count(*) from picture_cash where path='%s'"%(path,))[0][0]
            print find
            if find==None:
                image = get_img(path)
                img=image['base64_img']
                if (img!=''):
                    db.execNonQuery(bot.dbpath,"insert into picture_cash(path,img_base64,ext) values ('%s','%s','%s')"%(path,img,ext,))
            else:
                img=db.execQuery(bot.dbpath,"select img_base64 from picture_cash where path='%s'"%(path,))[0][0]
        except Exception,e:
            print 'error '+str(e)
        return {'ext':ext,'img':img}       

def get_img(img_url):
    try:
        response = urllib2.urlopen(img_url)
        img = response.read()
        return {'base64_img': img.encode('base64'),
                'content-type': response.info()['Content-Type']}
    except:
        return 'Error'        
