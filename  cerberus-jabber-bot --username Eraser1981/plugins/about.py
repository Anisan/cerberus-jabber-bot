# -*- coding: UTF-8 -*-
import xmpp

def init(bot):
  return 0

def description():
  return 'о программе'

def help():
    txt = 'О программе\n\n'
    txt = txt+ 'Jabber bot(v0.3)\n'
    txt = txt+ 'Возможности:\n'
    txt = txt+ '-поддержка плагинов\n'
    txt = txt+ '-обработка команд в отдельных потоках\n'
    txt = txt+ '-...\n\n'
    txt = txt+ 'Автор\n'
    txt = txt+ 'Eraser - Jabber:eraser1981@googlemail.com ICQ:308911945\n'
    return txt

def run(bot,mess):
    txt = help()
    return xmpp.Message(mess.getFrom(),txt,typ='chat')