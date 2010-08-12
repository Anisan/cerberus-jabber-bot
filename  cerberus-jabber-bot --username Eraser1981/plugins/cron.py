#!/usr/bin/python
# -*- coding: UTF-8 -*-
import xmpp
import time
import datetime
import threading
import utils.db as db


def init(bot):
    db.execQuery(bot.dbpath,"CREATE TABLE IF NOT EXISTS cron(num INTEGER, jid ,dtmask, command)")
    NotifyThread(bot).start()
    return 100
    
def check_access(bot,jid,command):
    access = 0
    jid_access = db.execQuery(bot.dbpath,"SELECT access_level, count(*) FROM access WHERE jid='%s'"%(jid))[0][0]
    com_access = db.execQuery(bot.dbpath,"SELECT access_level, count(*) FROM plugins WHERE name='%s'"%(command))[0][0];
    if (jid_access==None):
        jid_access=0
    if (com_access==None):
        access = -1
    if (access == 0):
        if (jid_access>=com_access):
            access = 1
    return access
  
############################################################################
# Thread run command
class RunThread(threading.Thread):
    # Override Thread's __init__ method to accept the parameters needed:
    def __init__(self,command, user, bot):
        self.tuser = user
        self.tcommand = command
        self.tbot = bot
        threading.Thread.__init__(self)

    def run(self):
        try:
            ## example for cron
            command = self.tcommand.split(' ')
            command = command[0]
            mess = xmpp.Message(to=self.tuser, body=self.tcommand,typ='chat',frm=self.tuser)
            plugin = getattr(self.tbot.plugins['plugins'],command)
            retry = plugin.run(self.tbot,mess)
            self.tbot.send(retry)
            msg = retry.__str__().encode('utf8')
            self.tbot.sbyte = self.tbot.sbyte + len(msg)
    
        except Exception ,x:
            print 'Error '+self.tcommand 
            print x
  
class NotifyThread(threading.Thread):
    # Override Thread's __init__ method to accept the parameters needed:
    def __init__(self, bot):
        self.jbot = bot
        threading.Thread.__init__(self)

    def run(self):
        work=True
        timer = 60
        while work:
            try:
                cur = db.execQuery(self.jbot.dbpath,"select * from cron")
                for row in cur:
                    user = row[1]
                    mask = row[2]
                    text = row[3]
                    command = text.split(' ')
                    command = command[0]
                    try:
                        fEx= 0
                        dtn = datetime.datetime.now()
                        dte = dtn.strftime(str(mask))
                        ts1=time.strptime(dte,"%d.%m.%Y %H:%M")
                        dt1=datetime.datetime(*ts1[:6])
                        td = dtn - dt1
                        if (td.days==0):
                            if (td.seconds<60):
                                if (td.seconds>0):
                                    fEx=1
                                    if (fEx==1):
                                        access = check_access(self.jbot,user,command)
                                        if (access == 1):
                                            RunThread(text,user,self.jbot).start()
                    except Exception ,x:
                            print x
            except Exception ,x:
                print x
            time.sleep(60)
            
def description():
  return 'Cron service - commands:add,del,ls'

def run(bot,mess):
  user=mess.getFrom()
  user=str(user).split('/')
  user=user[0]
  text = mess.getBody()
  command = text.split(' ')
  command = command[1]
  text = text[5:]
  l = len(command)
  text = text[l+1:]
  if (command=='help'):
    txt = 'Cron help\n\n'
    txt = txt+ 'Команды\n'
    txt = txt+ 'ls - список\n'
    txt = txt+ 'add - добавление\n'
    txt = txt+ 'del - удаление\n\n'
    txt = txt+ 'Формат \n'
    txt = txt+ 'маска команда(26.08.%Y 9:00 echo Днюха!)\n'
    txt = txt+ 'маска - %d.%m.%Y %H:%M\n'
    return(xmpp.Message(mess.getFrom(),txt))
    

  if (command=='add'):
            try:    
                if not isinstance(text,unicode):
                    text = unicode(text,'utf-8','ignore')
                command = text.split(' ')
                mask = command[0]+' '+command[1]
                text = text[len(mask)+1:]
                count= db.execQuery(bot.dbpath,"SELECT max(num),count(*) FROM cron WHERE jid='%s'"%(str(user),))[0][0];
                if count==None:
                    count = 0
                count = count+1
                db.execNonQuery(bot.dbpath,"insert into cron(num, dtmask, jid, command) values(%d,'%s','%s','%s')"%\
                    (count,mask,str(user),text))
                txt = 'Task saved! (num-'+str(count)+')'
            except db.DatabaseError, x:
                print x
                txt = x
            return xmpp.Message(mess.getFrom(),txt)

  if (command=='ls'):
    notes = 'Task list:\n'
    try:    
       cur = db.execQuery(bot.dbpath,"SELECT * FROM cron WHERE jid='%s' order by num"%(str(user),));
       for row in cur:
           notes = notes+str(row[0])+': '+row[3]+' ['+row[2]+']\n'
    except Exception, x:
       print x
       txt = x
    return xmpp.Message(mess.getFrom(),notes)

  if (command=='del'):
        try:    
                db.execNonQuery(bot.dbpath,"DELETE FROM cron WHERE jid='%s' and num=%d"%(str(user),int(text),));
                notes = 'Task deleted!\n'
        except Exception, x:
                print x
                notes = x
        return xmpp.Message(mess.getFrom(),notes)

