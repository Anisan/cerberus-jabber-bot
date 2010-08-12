#!/usr/bin/python
# -*- coding: UTF-8 -*-
import xmpp
import os

def init(bot):
  return 100

def description():
  return 'Launch jabber shell!'

def run(bot,mess):
  os.spawnv(os.P_NOWAIT,'./jabber-shell.py',[])
  shell = 'Jabber-shell started!'
  return xmpp.Message(mess.getFrom(),shell)
