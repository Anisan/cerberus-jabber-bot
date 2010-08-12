#!/usr/bin/python
# -*- coding: UTF-8 -*-
import xmpp

def init(bot):
  return 50

def description():
  return 'ростер бота'


def help():
    txt = 'Ростер\n\n'
    return txt

def run(bot,mess):
    try:
      text = 'Roster:\n'
      for jid in bot.roster.getItems():
        text=text+str(jid)+'|'
        if (bot.roster.getSubscription(jid)!=None):
            text= text+bot.roster.getSubscription(jid)+'|'
        if (bot.roster.getShow(jid)!=None):
            text=text+str(bot.roster.getShow(jid))+'|'
        if (bot.roster.getStatus(jid)!=None):
            text=text+bot.roster.getStatus(jid)+'|'
        if (bot.roster.getName(jid)!=None):
            text=text+bot.roster.getName(jid)+'|'
        text=text+'\n'
      return xmpp.Message(mess.getFrom(),text)
    except Exception,e:
      txt = e
      return xmpp.Message(mess.getFrom(),txt)
      

