#!/opt/bin/python
# -*- coding: utf-8 -*-

#JabberBot v.0.4
import sys
import os
import xmpp
import time
import datetime
import traceback
import utils.db as db
    
bot = None
AUTO_RESTART=0

##############################################################
def loadConfig():
    import ConfigParser
    config = ConfigParser.ConfigParser()
    config.read('config.ini')
    login = config.get('connect', 'login')
    password = config.get('connect', 'password')
    resource = config.get('connect', 'resource')
    priority = config.get('connect', 'priority')
    allow_password =  config.get('permission', 'allow_password')
    user_no_pass =  config.get('permission', 'user_no_pass')
    user_no_pass = user_no_pass.split(',')
    dbpath = config.get('settings', 'dbpath')
    return {'login':login,'password':password,'resource':resource,'priority':priority,\
            'allow_password':allow_password,  'user_no_pass':user_no_pass, 'dbpath':dbpath}

def loadPlugins():
    import os
    global bot
    commands = []
    public_commands = []
    for fname in os.listdir('plugins/'):
        if fname.endswith('.py'):
           plugin_name = fname[:-3]
           if plugin_name != '__init__':
              plugins=__import__('plugins.'+plugin_name)
              plugin = getattr(plugins,plugin_name)
              type = plugin.init(bot)
              commands.append(plugin_name)
              if (type>=0):
                com = "SELECT count(*) FROM plugins WHERE name='"+plugin_name+"'"
                table= db.execQuery(bot.dbpath,com)[0][0]
                if (table==0):
                    com = "insert into plugins(name,access_level) values('%s',%s)"% (plugin_name,type)
                    print com
                    db.execNonQuery(bot.dbpath,com)
    return {'plugins':plugins,'commands':commands,  'public_commands':public_commands}
    
def loadModules():
    import os
    global bot
    commands = []
    public_commands = []
    for fname in os.listdir('modules/'):
        if fname.endswith('.py'):
           plugin_name = fname[:-3]
           if plugin_name != '__init__':
              plugins=__import__('modules.'+plugin_name)
              plugin = getattr(plugins,plugin_name)
              type = plugin.init(bot)
              
######################################################################

def start():
    global bot
    global LOGGEDIN
    LOGGEDIN = 0
    config = loadConfig()
    acc = xmpp.JID(config['login']) 
    user,server=acc.getNode(),acc.getDomain()
    bot = xmpp.Client(server,debug=[])
    bot.config = config

    if bot.connect():
        print "Connected"
    else:
        print "Couldn't connect"
        sys.exit(1)
        return

    if bot.auth(user,bot.config['password'],bot.config['resource']):
        print 'Logged In'
    else:
        print "Auth error: eek -> ", bot.lastErr, bot.lastErrCode
        time.sleep(60) # sleep for 10 seconds
        sys.exit(1)
        return
       
    bot.roster = bot.getRoster()

    bot.dbpath = bot.config['dbpath']
    
    db.execNonQuery(bot.dbpath,"CREATE TABLE IF NOT EXISTS plugins(name text, access_level int,PRIMARY KEY(name))")
    
    bot.plugins = loadPlugins()
    print "Plugins loaded."

    loadModules()
    print "Modules loaded."
    
    
    bot.RegisterDisconnectHandler(bot.reconnectAndReauth)
    bot.sendInitPresence()
    print "Bot started."

    presence = xmpp.Presence(status = "", show = "online", priority = bot.config['priority'])
    bot.send(presence)
    
    for admin in bot.config['user_no_pass']:
        bot.send(xmpp.Message(admin,"Bot started!",typ='chat'))
    
    LOGGEDIN = 1

    while 1:
        bot.Process(10)


if __name__ == "__main__":
    try:	
        #config = loadConfig()
        start()
    except KeyboardInterrupt:
        print 'INTERRUPT'
        
        sys.exit(1)
    except:
        if AUTO_RESTART:
            if sys.exc_info()[0] is not SystemExit:
                traceback.print_exc()
            try:
                bot.disconnected()
            except IOError:
                # IOError is raised by default DisconnectHandler
                pass
            try:
                time.sleep(3)
            except KeyboardInterrupt:
                print 'INTERRUPT'
                sys.exit(1)
            print 'RESTARTING'
            os.execl(sys.executable, sys.executable, sys.argv[0])
        else:
            raise

#EOF
