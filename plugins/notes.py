#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xmpp
import datetime
import os
import utils.db as db

def init(bot):
  db.execNonQuery(bot.dbpath,"CREATE TABLE IF NOT EXISTS notes(num INTEGER, dt TIMESTAMP, jid, name, text)")
  return 10

def description():
  return 'заметки'

def help():
    txt = 'Notes (v0.3)\n\n'
    txt = txt+ 'Команды\n'
    txt = txt+ 'ls - список заметок\n'
    txt = txt+ 'add - добавление заметки*\n'
    txt = txt+ 'show "номер" - показ текста заметки "номер"\n'
    txt = txt+ 'del "номер" - удаление заметки "номер"\n\n'
    txt = txt+ '*первая строка текста станет названием заметки\n'
    return txt

def run(bot,mess):
  user=mess.getFrom()
  user=str(user).split('/')
  user=user[0]
  user_dir = 'notes/'+user
  text = mess.getBody()
  try:
      command = text.split(' ')
      command = command[1]
      text = text[6:]
      l = len(command)
      text = unicode(text[l+1:])
      if (command=='help'):
            txt = help()
            return xmpp.Message(mess.getFrom(),txt)
      if (command=='add'):
            try:    
                if not isinstance(text,unicode):
                    text = unicode(text,'utf-8','ignore')
                #todo name выдернуть
                name = text[:text.find('\n')]
                count= db.execQuery(bot.dbpath,"SELECT max(num) FROM notes WHERE jid='%s'"%(str(user),))[0][0];
                if count==None:
                    count = 0
                count = count+1
                db.execNonQuery(bot.dbpath,"insert into notes(num, dt, jid, name, text) values(%d,'%s','%s','%s','%s')"%\
                    (count,datetime.datetime.now(),str(user),name,text))
                txt = 'Note saved! (num-'+str(count)+')'
            except Exception, x:
                print x
                txt = x
            return xmpp.Message(mess.getFrom(),txt)
      if (command=='ls'):
            notes = 'Notes list:\n'
            try:    
                cur= db.execQuery(bot.dbpath,"SELECT * FROM notes WHERE jid='%s' order by num"%(str(user),));
                for row in cur:
                    notes = notes+str(row[0])+': '+row[3]+' ['+row[1]+']\n'
            except Exception, x:
                print x
                txt = x
            return xmpp.Message(mess.getFrom(),notes)
      if (command=='del'):
            try:    
                db.execNonQuery(bot.dbpath,"DELETE FROM notes WHERE jid='%s' and num=%d" % (str(user),int(text),));
                notes = 'Note deleted!\n'
            except Exception, x:
                print x
                notes = x
            return xmpp.Message(mess.getFrom(),notes)
      if (command=='show'):
            notes = 'Note '+text+':\n'
            try:    
                txt = db.execQuery(bot.dbpath,"SELECT text FROM notes WHERE jid='%s' and num=%d"%(str(user),int(text),))[0][0];
                notes = notes + txt
            except Exception,x:
                print x
                txt = x
            return xmpp.Message(mess.getFrom(),notes)
  except:
    txt = help()
    return xmpp.Message(mess.getFrom(),txt)
    



