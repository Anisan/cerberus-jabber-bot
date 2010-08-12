#!/usr/bin/python
# -*- coding: UTF-8 -*-
import xmpp

def init(bot):
  return 50

def description():
  return 'анонимка через бота'


def help():
    txt = 'Hidden (v0.1)\n\n'
    txt = txt+ 'Синтаксис: hidden JID_кому текст_сообщения\n'
    return txt

def run(bot,mess):
    try:
      text = mess.getBody()
      command = text.split(' ')
      jid=command[1]
      text = text[len("hidden")+1:]
      l = len(jid)
      text = unicode(text[l+1:])
      return xmpp.Message(jid,text)
    except:
      txt = help()
      return xmpp.Message(mess.getFrom(),txt)

