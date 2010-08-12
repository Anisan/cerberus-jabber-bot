#!/usr/bin/python
# -*- coding: UTF-8 -*-
import xmpp
import subprocess

def init(bot):
  return 100

def description():
  return 'Async execute command'

def run(bot,mess):
  cmd = mess.getBody()
  cmd = cmd[5:]
  subprocess.Popen(cmd)
  text = cmd +' execute!'
  return xmpp.Message(mess.getFrom(),text)

