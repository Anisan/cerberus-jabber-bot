#!/usr/bin/python
# -*- coding: UTF-8 -*-
import xmpp
def init(bot):
  return 0

def description():
  return 'Echo message'

def run(bot,mess):
  cmd = mess.getBody()
  cmd = cmd[5:]
  return xmpp.Message(mess.getFrom(),cmd,typ='chat')
