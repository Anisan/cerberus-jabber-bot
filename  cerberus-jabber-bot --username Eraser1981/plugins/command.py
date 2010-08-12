#!/usr/bin/python
# -*- coding: UTF-8 -*-
import xmpp
def init(bot):
  return 100

def description():
  return 'Manager command'
  #возможность переключать команды для доступа пользователю

def help():
    txt = 'Manager command (v0.1)\n\n'
    txt = txt+ 'Команды\n'
    txt = txt+ 'ls - список команд\n'
    txt = txt+ 'add - добавление команды для пользователей\n'
    txt = txt+ 'del - удаление команды пользователей\n\n'
    return txt

def run(bot,mess):
    user=mess.getFrom()
    user=str(user).split('/')
    user=user[0]
    user_dir = 'notes/'+user
    text = mess.getBody()
    try:
        command = text.split(' ')
        command = command[1]
        if (command=='help'):
            txt = help()
            return xmpp.Message(mess.getFrom(),txt)
        if (command=='ls'):
            usage = 'Public commands: \n'
            commands = bot.plugins['public_commands']
            for plugin in commands:
                usage = usage + plugin +','
            usage = usage + "\n"
            user=mess.getFrom()
            user=str(user).split('/')
            user=user[0]
            usage = usage+'Admin`s commands: \n'
            commands = bot.plugins['commands']
            for plugin in commands:
                usage = usage + plugin +','
            return xmpp.Message(mess.getFrom(),usage)
        if (command=='add'):
            com = text.split(' ')
            com = com[2]
            commands = bot.plugins['public_commands']
            commands.append(com)
            commands = bot.plugins['commands']
            commands.remove(com)
            return
        if (command=='del'):
            com = text.split(' ')
            com = com[2]
            commands = bot.plugins['public_commands']
            commands.remove(com)
            commands = bot.plugins['commands']
            commands.append(com)
            return
    except:
        txt = help()
        return xmpp.Message(mess.getFrom(),txt)
        
