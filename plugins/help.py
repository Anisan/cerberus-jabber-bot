#!/usr/bin/python
# -*- coding: utf-8 -*-
import xmpp
import utils.db as db

def init(bot):
  return 0

def description():
  return 'Help command'

def descPlugin(command,bot):
    plugin = getattr(bot.plugins['plugins'],command)
    return plugin.description()
    
def helpPlugin(command,bot):
    plugin = getattr(bot.plugins['plugins'],command)
    return plugin.help()

def check_access(bot,jid,command):
    access = 0
    jid_access = db.execQuery(bot.dbpath,"SELECT access_level, count(*) FROM access WHERE jid='%s'"%(jid))[0][0]
    com_access = db.execQuery(bot.dbpath,"SELECT access_level, count(*) FROM plugins WHERE name='%s'"%(command))[0][0];
    if (jid_access==None):
        jid_access=0
    if (com_access==None):
        access = -1
    if (access == 0):
        if (jid_access>=com_access):
            access = 1
    return access
    
def run(bot,mess):
    user=mess.getFrom()
    user=str(user).split('/')
    user=user[0]
    text = mess.getBody()
    if (text=='help'):
        usage = 'Commands: \n'
        commands = bot.plugins['commands']
        for plugin in commands:
            access = check_access(bot,user,plugin)
            if (access == 1):
                usage = usage + plugin +' - ' +descPlugin(plugin,bot)+'\n'
    else:
        command = text[len('help')+1:]
        access = check_access(bot,user,command)
        if (access == 1):
            usage = 'Help '+ command +' :\n'+helpPlugin(command,bot)+'\n'
    return xmpp.Message(to=mess.getFrom(), body=usage, typ='chat')
    
    