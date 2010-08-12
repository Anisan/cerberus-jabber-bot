# -*- coding: UTF-8 -*-
import xmpp

NS_PING          ='urn:xmpp:ping'            # XEP-0199

def init(bot):
  bot.RegisterHandler('iq', _IqPingCB, 'get',NS_PING)
  return -1 #system

def _IqPingCB(self, con, iq_obj):
    print iq_obj
    iq_obj = iq_obj.buildReply('result')
    print iq_obj
    con.send(iq_obj)
    #raise common.xmpp.NodeProcessed
  
