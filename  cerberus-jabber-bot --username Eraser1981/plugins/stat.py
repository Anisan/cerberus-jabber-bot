# -*- coding: utf-8 -*-
import xmpp
import utils.db as db
import time
import datetime

mess_count = 0
start_date = datetime.datetime.now()

def message_callback(conn,mess):
    global mess_count
    mess_count = mess_count+1
          
def init(bot):
    bot.RegisterHandler('message',message_callback)
    return 0

def description():
  return 'Statistics bot'

def run(bot,mess):
    global mess_count
    global start_date
    user=mess.getFrom()
    user=str(user).split('/')
    user=user[0]
    txt = '--- Сессия ---\n'
    txt = txt + 'Запуск - '+str(start_date)+'\n'
    txt = txt + 'Запросов - '+str(mess_count)+'\n'
    txt = txt + 'Отправлено - '+str(bot.sbyte)+' байт\n'
    txt = txt + 'Получено - '+str(bot.rbyte)+' байт\n'
    txt = txt + '--- Всего ---\n'
    count = db.execQuery(bot.dbpath,"SELECT count(*) FROM messages")[0][0];
    user_count = db.execQuery(bot.dbpath,"SELECT count(*) FROM messages where jid like '%s'"%(user+'%',))[0][0];
    txt = txt + 'Запросов - '+str(count)+'\n'
    txt = txt + 'Ваших запросов - '+str(user_count)+'\n'
    return xmpp.Message(mess.getFrom(),txt.decode('utf-8'),typ='chat')
