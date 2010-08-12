#!/usr/bin/python
# -*- coding: UTF-8 -*-
import xmpp
import os
import time
import datetime
import threading
import twitter_api as twitt
import utils.db as db
import utils
import base64

work=True
timer=300

# jabberbot app
CONSUMER_KEY = "Bz0nOOOfqSRvjfRIqTwmSg"  
CONSUMER_SECRET = "trpjKQqbg5U5jiHItMvc6kgtqdg2Kt9ONDBd4nloQ" 


TEMPLATE = """<table><tr><td><img src="data:image/%s;base64,%s" alt="img"/></td>
  <td><span class="twitter-user"><a href="http://twitter.com/%s">%s</a></span><br/>
  <span class="twitter-text">%s</span><br/>
  <span class="twitter-relative-created-at"><a href="http://twitter.com/%s/statuses/%s">Posted %s</a></span>
</td></tr></table>"""

     
def getAvatar(bot,user):
        img = ''
        ext =''
        path = user.profile_image_url
        extl = path.split('.')
        for i in extl:
            ext=i
        name = user.name
        try:
            find = db.execQuery(bot.dbpath,"select user,count(*) from twitter_avatar_cash where user='%s'"%(name,))[0][0]
            if find==None:
                image = utils.pic.get_img(path)
                img=image['base64_img']
                if (img!=''):
                    db.execNonQuery(bot.dbpath,"insert into twitter_avatar_cash(user,img_base64,ext) values ('%s','%s','%s')"%(name,str(img),ext,))
            else:
                img=db.execQuery(bot.dbpath,"select img_base64 from twitter_avatar_cash where user='%s'"%(name,))[0][0]
            
        except Exception,e:
            return 'Error '+str(e)
        return {'ext':ext,'img':img}

class CheckThread(threading.Thread):
    # Override Thread's __init__ method to accept the parameters needed:
    def __init__(self, bot):
        self.jbot = bot
        threading.Thread.__init__(self)
        
    def run(self):
        global work
        work=True
        global timer
        last_id=0
        while work:
            try:
                # conn = db.connect(self.jbot.dbpath,timeout=5.0)
                # cur = conn.cursor() # создание курсора
                # cur.execute('select * from twitter')
                cur = db.execQuery(self.jbot.dbpath,'select * from twitter')
                for row in cur:
                    user = row[0]
                    txt=''
                    oauth_token = row[1]
                    last_id=int(row[3])
                    xhtml=int(row[4])
                    try:
                        xhtml_txt=''
                        access_token = twitt.oauth.OAuthToken.from_string(oauth_token)
                        twitapi = twitt.OAuthApi(CONSUMER_KEY, CONSUMER_SECRET, access_token)
                        statuses = twitapi.GetFriendsTimeline(since_id=last_id)
                        for s in statuses:
                            if s.id>last_id:
                                last_id=s.id
                            txt = s.user.name.encode('utf-8')+' #'+str(s.id).encode('utf-8')+'\n'+\
                            s.text.encode('utf-8') +' ['+str(s.created_at)+']\n'
                            message=xmpp.protocol.Message(user, txt)
                            if (xhtml==1):
                                img=getAvatar(self.jbot,s.user)
                                xhtml_txt = TEMPLATE % (img['ext'].encode('utf-8'),img['img'].encode('utf-8'),\
                                s.user.screen_name.encode('utf-8'),s.user.name.encode('utf-8'),\
                                s.text.encode('utf-8'), s.user.screen_name.encode('utf-8'),\
                                str(s.id), str(s.relative_created_at))
                                xhtml_txt = xhtml_txt.replace('&','&#38;')
                                body=xmpp.simplexml.XML2Node('<body xmlns="%s">%s</body>' %
                                    ('http://www.w3.org/1999/xhtml',xhtml_txt))
                                message.addChild('html', {}, [body,], xmpp.NS_XHTML_IM)
                            self.jbot.send(message)
                            time.sleep(1)
                            msg = message.__str__().encode('utf8')
                            self.jbot.sbyte = self.jbot.sbyte + len(msg)
                    except Exception ,x:
                        print x
                    db.execNonQuery(self.jbot.dbpath,"update twitter set last_id=%s where oauth_token='%s'"%(str(last_id),oauth_token))
            except Exception,e:
                print 'Monitoring twitter error'
                print e
            time.sleep(timer)

def init(bot):
    # oauth_token oauth_secret
    db.execNonQuery(bot.dbpath,"CREATE TABLE IF NOT EXISTS twitter(jid text, oauth_token text, refresh int, last_id text, xhtml int, PRIMARY KEY(jid))")
    db.execNonQuery(bot.dbpath,"CREATE TABLE IF NOT EXISTS twitter_avatar_cash(user text, img_base64 text, ext text, PRIMARY KEY(user))")
    monitor=CheckThread(bot)
    monitor.setName('TwitterMonitor')
    monitor.start()
    return 100

def description():
  return "twitter bot"

def help():
    txt = 'Twitter bot (OAuth) (v0.3)\n\n'
    txt = txt+'reg - регистрация\n'
    txt = txt+'unreg - удаление аккаунта\n'
    txt = txt+'post - отправить сообщение\n'
    txt = txt+'xhtml - 0|1 выкл|вкл режима xhtml(с аватарами)\n'
    return txt

   
def run(bot,mess):
      global  myProxy
      user=mess.getFrom()
      user=str(user).split('/')
      user=user[0]
      text = mess.getBody()
      try:
          command = text.split(' ')
          command = command[1]
          if (command=='help'):
            txt = help()
            return xmpp.Message(mess.getFrom(),txt)
          if (command=='reg'):
            try:
                twitter = twitt.OAuthApi(CONSUMER_KEY, CONSUMER_SECRET) 
                request_token = twitter.getRequestToken()
                authorization_url = twitter.getAuthorizationURL(request_token)
                txt = 'Authorization url\n'+authorization_url+'\n'
                
                find = db.execQuery(bot.dbpath,"select oauth_token,count(*) from twitter where jid='%s'"%(str(user),))[0][0]
                if find==None:
                   db.execNonQuery(bot.dbpath,"insert into twitter(jid, oauth_token, refresh, last_id, xhtml) values ('%s','%s',%d,%d,%d)"%(str(user),str(request_token),10,0,0,))
                else:
                   db.execNonQuery(bot.dbpath,"update twitter set oauth_token=? where jid='%s'"%(str(request_token)  ,str(user),))
                txt = txt+'Enter pin! (twitter pin xxxxxxx)'
            except Exception,x:
                print 'oauth '+str(x)
                txt = x
            return xmpp.Message(mess.getFrom(),txt)
          if (command=='pin'):
            comm = text.split(' ')
            pin = comm[2]
            try:
                request_token = twitt.oauth.OAuthToken.from_string(db.execQuery(bot.dbpath,"select oauth_token from twitter where jid='%s'"%(str(user),))[0][0])
                twitter = twitt.OAuthApi(CONSUMER_KEY, CONSUMER_SECRET, request_token) 
                access_token = twitter.getAccessToken(pin)
                twitter = twitt.OAuthApi(CONSUMER_KEY, CONSUMER_SECRET, access_token)
                twuser = twitter.GetUserInfo()
                db.execNonQuery(bot.dbpath,"update twitter set oauth_token='%s' where jid='%s'"%(str(access_token) ,str(user),))
                txt = 'Register success!'
            except Exception,x:
                print 'oauth '+str(x)
                txt = 'Register error! Try again!'
            return xmpp.Message(mess.getFrom(),txt)  
          if (command=='unreg'):
            comm = text.split(' ')
            find = db.execQuery(bot.dbpath,"select oauth_token,count(*) from twitter where jid='%s'"%(str(user),))[0][0]
            if find==None:
                txt='No found!'
            else:
                db.execNonQuery(bot.dbpath,"delete from twitter where jid='%s'"%(str(user),))
                txt = 'Account deleted!'
            return xmpp.Message(mess.getFrom(),txt)
          if (command=='post'):
            find = db.execQuery(bot.dbpath,"select oauth_token,count(*) from twitter where jid='%s'"%(str(user),))[0][0]
            if find!=None:
                oauth_token = db.execQuery(bot.dbpath,"select oauth_token from twitter where jid='%s'"%(str(user),))[0][0]
                text = text.encode("utf-8")
                text = text[len("twitter post "):]
                try:
                    access_token = twitt.oauth.OAuthToken.from_string(oauth_token)
                    twitapi = twitt.OAuthApi(CONSUMER_KEY, CONSUMER_SECRET, access_token)                   
                    posting = twitapi.PostUpdate(text)
                except Exception ,x:
                    print "twit post - "+ str(x)
                txt = 'Post! '+'http://twitter.com/'+posting.GetUser().GetScreenName()+'/status/'+str(posting.GetId())
            else:
                txt = 'reg need first!'
            return xmpp.Message(mess.getFrom(),txt)
          if (command=='search'):
            find = db.execQuery(bot.dbpath,"select oauth_token,count(*) from twitter where jid='%s'"%(str(user),))[0][0]
            if find!=None:
                cur = db.execQuery(bot.dbpath,"select * from twitter where jid='%s'"%(str(user),))
                row = cur[0]
                oauth_token = row[1]
                xhtml = int(row[4])
                text = text.encode("utf-8")
                text = text[len("twitter search "):]
                try:
                    access_token = twitt.oauth.OAuthToken.from_string(oauth_token)
                    twitapi = twitt.OAuthApi(CONSUMER_KEY, CONSUMER_SECRET, access_token)
                    statuses = twitapi.GetSearch(text,query_users=True)
                    txt = "Not found - "+text+"\n"
                    for s in statuses:
                            txt = "Twitter search - "+text+"\n"+s.user.name.encode('utf-8')+' #'+str(s.id).encode('utf-8')+'\n'+\
                            s.text.encode('utf-8') +' ['+str(s.created_at)+']\n'
                            message=xmpp.protocol.Message(user, txt)
                            if (xhtml==1):
                                img=getAvatar(bot,s.user)
                                xhtml_txt = TEMPLATE % (img['ext'].encode('utf-8'),img['img'].encode('utf-8'),\
                                s.user.screen_name.encode('utf-8'),s.user.name.encode('utf-8'),\
                                s.text.encode('utf-8'), s.user.screen_name.encode('utf-8'),\
                                str(s.id), str(s.relative_created_at))
                                xhtml_txt = xhtml_txt.replace('&','&#38;')
                                body=xmpp.simplexml.XML2Node('<body xmlns="%s">%s</body>' %
                                    ('http://www.w3.org/1999/xhtml',xhtml_txt))
                                message.addChild('html', {}, [body,], xmpp.NS_XHTML_IM)
                            bot.send(message)
                            time.sleep(1)
                except Exception ,x:
                    print "twit search - "+ str(x)
            else:
                txt = 'reg need first!'
            message=xmpp.protocol.Message(user, txt)
            return  message
          if (command=='xhtml'):
            find = db.execQuery(bot.dbpath,"select oauth_token,count(*) from twitter where jid='%s'"%(str(user),))[0][0]
            if find!=None:
                text = unicode(text[len("twitter xhtml "):])
                db.execNonQuery(bot.dbpath,"update twitter set xhtml=%d where jid='%s'"%(int(text),str(user),))
                txt = 'XHTML set!'
            else:
                txt = 'reg need first!'
            return xmpp.Message(mess.getFrom(),txt)
      except:
        txt = help()
        return xmpp.Message(mess.getFrom(),txt,typ='chat')
        






