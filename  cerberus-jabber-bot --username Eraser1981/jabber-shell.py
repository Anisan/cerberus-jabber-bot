#!/opt/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007 - Kirill A. Korinskiy - catap@catap.ru
# Copyright (C) 2007 - Vadim Kalinnkov - bulvinkl@gmail.com
# Copyright (C) 2008 - koriaf - koriaf@gmail.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it would be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write the Free Software Foundation,
# Inc.,  51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import sys, os, xmpp, pipes, time, string

current_dir = "~/"
ORIGINAL_CONFIG = "/jffs/bot/jabber-shell.conf"
GLOBAL_CONFIG = "/etc/jabber-shell.conf"
USER_CONFIG = "~/.jabber-shell.conf"
LOCAL_CONFIG = "./jabber-shell.conf"
LOG_FILENAME = "jabber-shell.log"

CONFIG = dict()

def readConfig():
    """Try read config from some places"""
    print "Reading Config..."
    def parseConfig(config):
        """Parse readed config"""
        for config_str in config.split("\n"):            
            if len(config_str.split("="))>1: 
                global CONFIG
                CONFIG[config_str.split("=")[0].strip()] = config_str.split("=")[1].strip()
    for config_path in [ORIGINAL_CONFIG, GLOBAL_CONFIG, USER_CONFIG, LOCAL_CONFIG]:
        try:
            parseConfig(open(config_path).read())
        except:
            pass
    print "Config readed and parsed"

def ProcessChat(conn, mess):
    """Process chat with user"""
    global CONFIG
    global current_dir
    def isAccess(jid):
        return jid.getStripped() in CONFIG['JID_ADMIN']
    def evalCommand():

	tmp_file = "/tmp/jabber-shell." + str(time.time())
        os.openpty()
	command = "cd " + current_dir + ";" + mess.getBody() + " > " + tmp_file + " 2> " + tmp_file
	print command
        os.system(command.encode('utf-8', 'replace'))
	logfile.write(command + "\n")
        log = open(tmp_file)

	MsgToSend = "non null"
	while MsgToSend != "":
	  MsgToSend = log.read(4096) #TODO: set max message, allowed by server
	  OutMsg = ""
	  for xch in MsgToSend:  #strip all special chars(less that 20h, excl. 0xA)
	     if (ord(xch) >= 0x20) or (ord(xch) == 10):
	       OutMsg += xch
          if OutMsg != "":
	     client.send(xmpp.protocol.Message(mess.getFrom(),unicode("\n" + OutMsg, "UTF-8"), "chat"))
	  time.sleep(1) #antiantiflud

	os.remove(tmp_file)

    if isAccess(mess.getFrom()):
        if (mess.getBody() != None):# and (mess.getBody() != "clear") :

            if (mess.getBody()[0:3] == "cd ") and ( len(mess.getBody()) > 2) :
                dirto = mess.getBody()[3:]

		if (len(dirto) == 0) or (dirto == "~/"):
	           current_dir = "";
		   print "Cd to homedir"
		elif dirto[0] == '/':   #if absolute path
		   current_dir = dirto
		   print "cd to " + current_dir
		else:   #relative path
		   current_dir = current_dir + "/" + dirto
		   print "Rel cd to " + current_dir

	    else:
                evalCommand()
    #else:
        #client.send(xmpp.protocol.Message(senderjid, "You not the administrator!", "chat"))
	#null: steath :-)

def StepOn(conn):
    try:
        conn.Process(1)
    except KeyboardInterrupt: return 0
    return 1

def GoOn(conn):
    while StepOn(conn): pass

readConfig()

jid       = xmpp.JID(CONFIG['JID_FROM'])
print "Connecting to " + jid.getDomain() + "..."
client    = xmpp.Client(jid.getDomain(), debug = False)
connected = client.connect()
auth      = client.auth(jid.getNode(), CONFIG['JID_FROM_PASS'], CONFIG['JID_CLIENT'])

client.RegisterHandler("message",ProcessChat)
client.sendInitPresence()

print "Connected\n"

logfile = open(LOG_FILENAME, 'a', 1)
logfile.write("---\nLogged\n")

GoOn(client)

logfile.close();
client.disconnect()
