# -*- coding: UTF-8 -*-
import xmpp

NS_PING          ='urn:xmpp:ping'            # XEP-0199

bot_identity = {'type': 'pc', 'category': 'client', 'name': 'jabberbot'}
bot_common_features = [xmpp.NS_DISCO_INFO, xmpp.NS_VERSION, NS_PING, xmpp.NS_MOOD, xmpp.NS_ACTIVITY]

def init(bot):
  bot.RegisterHandler('iq', _DiscoverInfoGetCB, 'get', xmpp.NS_DISCO_INFO)
  return -1 #system

def _DiscoverInfoGetCB(con, iq_obj):
        q = iq_obj.getTag('query')
        node = q.getAttr('node')
        
        #if self.commandInfoQuery(con, iq_obj):
        #    raise common.xmpp.NodeProcessed

        #id_ = unicode(iq_obj.getAttr('id'))
        #if id_[:6] == 'bot_':
            # We get this request from echo.server
        #    raise xmpp.NodeProcessed
        
        iq = iq_obj.buildReply('result')
        q = iq.getTag('query')
        if node:
            q.setAttr('node', node)
        q.addChild('identity', attrs = bot_identity)
        client_version = 'eraser#' #+ gajim.caps_hash[self.name]

        if node in (None, client_version):
            for f in bot_common_features:
                q.addChild('feature', attrs = {'var': f})

        if q.getChildren():
            con.send(iq)
            raise xmpp.NodeProcessed


