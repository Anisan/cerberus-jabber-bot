# -*- coding: UTF-8 -*-
import xmpp


def init(bot):
  bot.RegisterHandler('presence', presence_callback)
  return -1 #system

  
MSG_AUTHORIZE_ME = 'Hey there. You are not yet on my roster. Authorize my request and I will do the same.'
MSG_NOT_AUTHORIZED = 'You did not authorize my subscription request. Access denied.'


def presence_callback(conn, presence):
    try:
        jid, type, show, status = presence.getFrom(), \
                presence.getType(), presence.getShow(), \
                presence.getStatus()
        
        user=str(jid).split('/')
        user=user[0]
        
        if not type:
            type = 'available'
        if type in ('subscribe','subscribed','unsubscribed'):
            roster = conn._owner.getRoster()
            try:
                subscription = roster.getSubscription(str(jid))
            except KeyError, ke:
                #User not on our roster
                subscription = None
            if type == 'subscribe':
                # Incoming presence subscription request
                if subscription in ('to', 'both', 'from'):
                    roster.Authorize(jid)
                if subscription not in ('to', 'both'):
                    roster.Subscribe(jid)
                if subscription in (None, 'none'):
                    conn.send(xmpp.Message(jid,MSG_AUTHORIZE_ME))
            elif type == 'subscribed':
                # Authorize any pending requests for that JID
                conn.send(xmpp.Message(jid, 'Thanks for adding into your contacts.\ntype help to get list of available functionality.\nJabber Bot.'))
                roster.Authorize(jid)
            elif type == 'unsubscribed':
                # Authorization was not granted
                conn.send(xmpp.Message(jid,MSG_NOT_AUTHORIZED))
                roster.Unauthorize(jid)
    except Exception ,x:
        print x