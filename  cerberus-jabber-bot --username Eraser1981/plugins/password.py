#!/usr/bin/python
# -*- coding: UTF-8 -*-
import xmpp
import utils.db as db

def init(bot):
  return 50

def description():
  return 'admin password'

def run(bot,mess):
  user=mess.getFrom()
  user=str(user).split('/')
  user=user[0]
  password = mess.getBody()
  password = password[9:]
  if password == bot.config['allow_password']:
    table= db.execQuery(bot.dbpath,"SELECT count(*) FROM access WHERE jid='%s'"%(user,))[0][0];
    if (table==0):
        conn.db.execNonQuery(bot.dbpath,"insert into access(jid,access_level) values('%s',%d)"%(user,100,));
    else:
        db.execQuery(bot.dbpath,"update access set access_level=%d where jid='%s'"%(100,user,));
    text = "You added to administrator group (level 100)!"
    return xmpp.Message(mess.getFrom(),text)
    return
  text = "Wrong password!"
  return xmpp.Message(mess.getFrom(),text)
  
