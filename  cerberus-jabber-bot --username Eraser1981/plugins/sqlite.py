#!/usr/bin/python
# -*- coding: UTF-8 -*-
import xmpp
import utils.db as db

def init(bot):
  return 100

def description():
  return 'SQLite execute query!'

def run(bot,mess):
  user=mess.getFrom()
  user=str(user).split('/')
  user=user[0]
  user_dir = 'notes/'+user
  text = mess.getBody()
  try:
    text = text[len('sqlite')+1:]+'\n'
    cur = db.execQuery(bot.dbpath,text)
    for row in cur:
        for col in row:
            conv=''
            if (type(col)== int):
                conv = str(col)
            if (type(col)==str):
                conv = col.encode('utf-8')
            if (type(col)==unicode):
                conv =col
            text=text+' '+conv
        text=text+'\n'
  except Exception,e:
    text = e
  return xmpp.Message(mess.getFrom(),text)
