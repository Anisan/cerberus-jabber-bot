#!/usr/bin/python
# -*- coding: UTF-8 -*-
import xmpp

def init(bot):
  return 0

def description():
  return 'сообщение админу'


def help():
    txt = 'Сообщение администратору бота (v0.1)\n\n'
    txt = txt+ 'Синтаксис: admin текст_сообщения\n'
    return txt

def run(bot,mess):
    try:
      text = mess.getBody()
      command = text.split(' ')
      text = text[len("admin")+1:]
      txt = "["+str(mess.getFrom())+"]\n"+ text
      for admin in bot.config['user_no_pass']:
        bot.send(xmpp.Message(admin,txt,typ='chat'))
      txt = 'Сообщение отправлено!'
      return xmpp.Message(mess.getFrom(),txt,typ='chat')
    except:
      txt = help()
      return xmpp.Message(mess.getFrom(),txt,typ='chat')
      return

