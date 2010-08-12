#!/usr/bin/python
# -*- coding: UTF-8 -*-
import xmpp

def init(bot):
  return 50

def description():
  return 'Set status bot'


def help():
    txt = 'Set status bot (v0.2)\n\n'
    txt = txt+ 'Синтаксис: setstatus статус текст_статуса\n'
    txt = txt+ 'Статусы - online,chat,away,xa,dnd,invisible\n'
    return txt

def run(bot,mess):
    try:
      text = mess.getBody()
      command = text.split(' ')
      status=command[1]
      text = text[len('setstatus')+1:]
      l = len(status)
      text = unicode(text[l+1:])
      presence = xmpp.Presence(status = text, show = status, priority = bot.config['priority'])
      bot.send(presence)
      txt = 'Status set!'
      return xmpp.Message(mess.getFrom(),txt)
    except:
      txt = help()
      return xmpp.Message(mess.getFrom(),txt)

