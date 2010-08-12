#!/usr/bin/python
# -*- coding: UTF-8 -*-
import xmpp
import os

def init(bot):
  return 100

def description():
  return 'Execute command'

def run(bot,mess):
  cmd = mess.getBody()
  cmd = cmd[4:]
  output = os.popen(cmd).read()
  if not isinstance(output, unicode):
     output = unicode(output,'utf-8','ignore')
  return xmpp.Message(mess.getFrom(),output,typ='chat')
