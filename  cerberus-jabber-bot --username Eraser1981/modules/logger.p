#!/usr/bin/python
# -*- coding: utf-8 -*-
from xmpp import *
import time,os

def init(bot):
  bot.RegisterHandler('message',messageCB)
  bot.RegisterHandler('presence',presenceCB)
  p=Presence(to='%s/logger'%'ubuntu')
  p.setTag('x',namespace=NS_MUC).setTagData('password','1q2w3e')
  p.getTag('x').addChild('history',{'maxchars':'0','maxstanzas':'0'})
  bot.send(p)
  return -1 #system
 
LOGDIR=''

def LOG(stanza,nick,text):
    ts=stanza.getTimestamp()
    if not ts:
        ts=stanza.setTimestamp()
        ts=stanza.getTimestamp()
    tp=time.mktime(time.strptime(ts,'%Y%m%dT%H:%M:%S'))+3600*3
    if time.localtime()[-1]: tp+=3600
    tp=time.localtime(tp)
    fold=stanza.getFrom().getStripped().replace('@','%')+'_'+time.strftime("%Y.%m",tp)
    day=time.strftime("%d",tp)
    tm=time.strftime("%H:%M:%S",tp)
    try: os.mkdir(LOGDIR+fold)
    except: pass
    fName='%s%s/%s.%s.html'%(LOGDIR,fold,fold,day)
    try: open(fName)
    except:
        open(fName,'w').write("""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xml:lang="ru-RU" lang="ru-RU" xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="content-type" />
        <title>%s logs for %s.%s.</title>
    </head>
    <body>
<table border="1"><tr><th>time</th><th>who</th><th>text</th></tr>
"""%('ubuntu',fold,day))
    text='<pre>%s</pre>'%text
    open(fName,'a').write((u"<tr><td>%s</td><td>%s</td><td>%s</td></tr>\n"%(tm,nick,text)).encode('utf-8'))
    print (u"<tr><td>%s</td><td>%s</td><td>%s</td></tr>\n"%(tm,nick,text)).encode('koi8-r','replace')
#    print time.localtime(tp),nick,text

def messageCB(sess,mess):
    nick=mess.getFrom().getResource()
    text=mess.getBody()
    LOG(mess,nick,text)

roster=[]

def presenceCB(sess,pres):
    nick=pres.getFrom().getResource()
    text=''
    if pres.getType()=='unavailable':
        if nick in roster:
            text=nick+unicode(' покинул конференцию','koi8-r')
            roster.remove(nick)
    else:
        if nick not in roster:
            text=nick+unicode(' пришёл в конференцию','koi8-r')
            roster.append(nick)
    if text: LOG(pres,nick,text)


