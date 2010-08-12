#!/usr/bin/python
# -*- coding: UTF-8 -*-
import xmpp
import time
import datetime
import threading
import utils.db as db
import utils
import feedparser 

myProxy = {'https':'http://ИсуповА:Fylhtq@128.0.20.5:80/',\
                 'http':'http://ИсуповА:Fylhtq@128.0.20.5:80/'}

def init(bot):
    db.execNonQuery(bot.dbpath,"CREATE TABLE IF NOT EXISTS rss(num INTEGER, jid TEXT,url TEXT, last_time, name TEXT, desc TEXT, icon TEXT, xhtml INTEGER)")
    NotifyThread(bot).start()
    return 50
    
TEMPLATE_IMG = """<table><tr><td><img src="data:image/%s;base64,%s" alt="img"/></td>
  <td>%s</td></tr></table>"""

TEMPLATE = """<span class="feed"><a href="%s">%s</a></span><br/>
  <span class="title"><b>%s</b></span><br/>
  <span class="description">%s</span><br/>
  <span class="datetime"><a href="%s">Posted %s</a></span>"""
########################################################
def getAvatar(dbpath,path):
        img = ''
        ext =''
        extl = path.split('.')
        for i in extl:
            ext=i
        try:
            find = db.execQuery(dbpath,"select path,count(*) from picture_cash where path='%s'"%(path,))[0][0]
            if find==None:
                image = utils.pic.get_img(path)
                img=image['base64_img']
                if (img!=''):
                    db.execNonQuery(dbpath,"insert into picture_cash(path,img_base64,ext) values ('%s','%s','%s')"%(path,img,ext,))
                    #conn.commit()
            else:
                img=db.execQuery(dbpath,"select img_base64 from picture_cash where path='$s"%(path,))[0][0]
            #conn.close()
        except Exception,e:
            print 'error get avatar ' + str(e)
        return {'ext':ext,'img':img}       

############################################################################
class NotifyThread(threading.Thread):
    # Override Thread's __init__ method to accept the parameters needed:
    def __init__(self, bot):
        self.jbot = bot
        threading.Thread.__init__(self)

    def run(self):
        work=True
        timer = 1800
        while work:
            try:
                import urllib2
                
                proxyHandler = urllib2.ProxyHandler(myProxy)
                

                cur = db.execQuery(self.jbot.dbpath,"select * from rss")
                for row in cur:
                    user = row[1]
                    url = row[2]
                    lastdt = row[3]
                    xhtml=int(row[7])
                    if lastdt==None:
                        lastdt = time.strptime('Tue Jul 20 12:15:54 2001', "%a %b %d %H:%M:%S %Y")
                    else:
                        lastdt=time.strptime(lastdt, "%a %b %d %H:%M:%S %Y")
                    try:
                        
                        atom_lenta = feedparser.parse(url,handlers=proxyHandler) # парсим Atom ленту
                        title = atom_lenta.feed.get('title', 'No title').encode('utf-8') # заголовок ленты
                        desc = atom_lenta.feed.get('description', 'No description').encode('utf-8') # описание ленты
                        icon = atom_lenta.feed.get('image', '')
                        if (icon!=''):
                            icon = icon["href"]
                        link = atom_lenta.feed.get('link', 'No link').encode('utf-8')
                        newlastdt = lastdt
                        for entry in atom_lenta.entries: # теперь пробежимся по записями ленты
                            # datetime last message
                          try:  
                            entrydt = time.strptime(time.asctime(entry.updated_parsed), "%a %b %d %H:%M:%S %Y")
                            if (lastdt<entrydt):
                                if (newlastdt<entrydt):
                                    newlastdt = entrydt
                                description = entry.description.encode('utf-8')
                                #ограничитель по длине описания (иначе выпинывает)
                                if (len(description)>20000):
                                    description = description[:20000]
                                if (xhtml==1):
                                    message=xmpp.protocol.Message(user, "Need suppots XHTML (XEP-0071)!")
                                    #img=getAvatar(self.jbot,s.user)
                                    icon=''
                                    if (icon==''):
                                        templ=TEMPLATE
                                    else: 
                                        img=getAvatar(self.jbot.dbpath,icon.decode('utf-8'))
                                        templ=TEMPLATE_IMG %(img['ext'].encode('utf-8'),img['img'].encode('utf-8'),TEMPLATE)
                                    xhtml_txt = templ % (link,title,\
                                    entry.title.encode('utf-8'),\
                                    description,
                                    entry.link.encode('utf-8'),time.asctime(entrydt))
                                    #xhtml_txt = xhtml_txt.replace('&','&#38;')
                                    body=xmpp.simplexml.XML2Node('<body xmlns="%s">%s</body>' %
                                        ('http://www.w3.org/1999/xhtml',xhtml_txt))
                                    message.addChild('html', {}, [body,], xmpp.NS_XHTML_IM)
                                else:
                                    txt=title+'\n'
                                    txt=txt+entry.title.encode('utf-8')+'\n' 
                                    description+'\n' 
                                    txt=txt+entry.link.encode('utf-8')+' '+time.asctime(entrydt)
                                    message=xmpp.protocol.Message(user, txt)
                                    
                                self.jbot.send(message)
                                msg = message.__str__().encode('utf8')
                                self.jbot.sbyte = self.jbot.sbyte + len(msg)
                                time.sleep(2)      #если не ставить отваливается, типа не успевает отправить  
                          except Exception,e:
                                print 'entry '+str(e)
                    except Exception ,x:
                        print 'feed '+str(x)
                    db.execNonQuery(self.jbot.dbpath,"update rss set name='%s',desc='%s',icon='%s',last_time='%s' where url='%s'"%(title.decode("utf-8"),desc.decode("utf-8"),icon.decode("utf-8"),time.asctime(newlastdt),url,))
                    #conn.execute('update rss set last_time=? where url=?',(time.asctime(newlastdt),url,))
                    
            except Exception ,x:
                print 'thread '+str(x)
            time.sleep(timer)
            
def description():
  return 'Rss (0.1) - commands:add,del,ls'

def run(bot,mess):
  user=mess.getFrom()
  user=str(user).split('/')
  user=user[0]
  text = mess.getBody()
  command = text.split(' ')
  command = command[1]
  text = text[4:]
  l = len(command)
  text = text[l+1:]
  if (command=='help'):
    txt = 'Rss help\n\n'
    txt = txt+ 'Команды\n'
    txt = txt+ 'ls - список фидов\n'
    txt = txt+ 'add - добавление\n'
    txt = txt+ 'del - удаление\n\n'
    txt = txt+ 'xhtml - переключение режима отправки\n\n'
    return(xmpp.Message(mess.getFrom(),txt))
    

  if (command=='add'):
    try:    
        if not isinstance(text,unicode):
            text = unicode(text,'utf-8','ignore')
        count= db.execQuery(bot.dbpath,"SELECT max(num),count(*) FROM rss WHERE jid='%s'"%(str(user),))[0][0];
        if count==None:
            count = 0
        count = count+1
        db.execNonQuery(bot.dbpath,"insert into rss(num, jid, url, xhtml) values(%d,'%s','%s',0)"%(count,str(user),text))
        txt = 'Rss saved! (num-'+str(count)+')'
    except Exception, x:
        print x
        txt = x
    return xmpp.Message(mess.getFrom(),txt)

  if (command=='ls'):
    notes = 'Rss list:\n'
    cur = db.execQuery(bot.dbpath,"SELECT * FROM rss WHERE jid='%s' order by num"%(str(user),));
    for row in cur:
        notes = notes+str(row[0])+': '+row[4]+' '+row[2]+'\n'
    return xmpp.Message(mess.getFrom(),notes)

  if (command=='del'):
    cur = db.execNonQuery(bot.dbpath,"DELETE FROM rss WHERE jid='%s' and num=%s"%(str(user),text,));
    notes = 'Feed deleted!\n'
    return xmpp.Message(mess.getFrom(),notes)
 
  if (command=='xhtml'):
        xhtml = db.execQuery(bot.dbpath,"SELECT xhtml FROM rss WHERE jid='%s' and num=%d"%(str(user),int(text),))[0][0];
        if xhtml == 1:
            xhtml = 0
            notes = 'Xhtml set - 0'
        else: 
            xhtml = 1
            notes = 'Xhtml set - 1'
        db.execNonQuery(bot.dbpath,"update rss set xhtml=%d WHERE jid='%s' and num=%s"%(xhtml,str(user),text,));
        return xmpp.Message(mess.getFrom(),notes)
