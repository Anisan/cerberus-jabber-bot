# -*- coding: utf-8 -*-
import xmpp
import threading
import datetime
import utils.db as db

def init(bot):

    db.execNonQuery(bot.dbpath,"CREATE TABLE IF NOT EXISTS messages(dt TIMESTAMP, jid text, message text,PRIMARY KEY(jid))")
    db.execNonQuery(bot.dbpath,"CREATE TABLE IF NOT EXISTS access(jid text, access_level int,PRIMARY KEY(jid))")
    bot.sbyte = 0
    bot.rbyte = 0
    get_access_levels(bot)
    bot.RegisterHandler('message',message_callback)
    return -1 #system
    

def runPlugin(command,bot,mess):
    plugin = getattr(bot.plugins['plugins'],command)
    retry = plugin.run(bot,mess)
    #change length message
    bot.send(retry)
    msg = retry.__str__().encode('utf8')
    bot.sbyte = bot.sbyte + len(msg)
    
  
############################################################################
# Thread run command
class RunThread(threading.Thread):
    # Override Thread's __init__ method to accept the parameters needed:
    def __init__(self,command, bot, mess):
        self.tmess = mess
        self.tcommand = command
        self.tbot = bot
        threading.Thread.__init__(self)

    def run(self):
        try:
            text = self.tmess.getBody()
            user=self.tmess.getFrom()
            com = "insert into messages(dt, jid, message) values('%s','%s','%s')" %(datetime.datetime.now(),str(user),text)
            db.execNonQuery(self.tbot.dbpath,com)
            runPlugin(self.tcommand,self.tbot,self.tmess)
        except Exception ,x:
            print 'Error '+self.tcommand 
            print x
        
def message_callback(conn,mess):
    try:
          msg = mess.__str__().encode('utf8')
          conn._owner.rbyte = conn._owner.rbyte + len(msg)
          text = mess.getBody()
          if ( text == None ):
             return
          command = text.split(' ')
          command = command[0]
          user=mess.getFrom()
          user=str(user).split('/')
          user=user[0]
          access = check_access(conn._owner,user,command)
          if (access == -1):
            text = "wrong command. try 'help'"
          elif (access == 0):
            text = "Access denied!. try 'help'"
          elif (access == 1):
            RunThread(command,conn._owner,mess).start()
            return

    except Exception ,x:
        print x
        text = "wrong command. try 'help'"
    conn.send(xmpp.Message(mess.getFrom(),text,typ='chat'))
    
################################################################################
def get_access_levels(bot):
    for admin in bot.config['user_no_pass']:
        com = "SELECT count(*) FROM access WHERE jid='%s'"%(admin)
        table= db.execQuery(bot.dbpath,com)[0][0]
        if (table==0):
            com = "insert into access(jid,access_level) values('%s',%s)"%(admin,100)
            db.execNonQuery(bot.dbpath,com)
        else:
            com = "update access set access_level=%s where jid='%s'"%(100,admin)
            db.execNonQuery(bot.dbpath,com)
    for jid in bot.roster.getItems():
        com = "SELECT count(*) FROM access WHERE jid='%s'"%(jid)
        table= db.execQuery(bot.dbpath,com)[0][0]
        if (table==0):
            com = "insert into access(jid,access_level) values('%s',%s)"%(jid,0)
            db.execNonQuery(bot.dbpath,com)
    
    
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

################################################################################
