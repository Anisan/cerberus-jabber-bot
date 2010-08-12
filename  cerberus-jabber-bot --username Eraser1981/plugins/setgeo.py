#!/usr/bin/python
# -*- coding: UTF-8 -*-
import xmpp

def init(bot):
  return 50

def description():
  return 'set geolocation (XEP-0080)'

def help():
    txt = 'Set geolocation (XEP-0080) (v0.1)\n\n'
    txt = txt+ 'Синтаксис: setgeo элемент значение\n'
    txt = txt+ '           элемент значение\n'
    txt = txt+ '           ...\n'
    txt = txt+ 'Элемент:тип - '
    txt = txt+ 'accuracy:decimal,alt:decimal,area:string,bearing:decimal,building:string,countrycode:string,'\
                'datum:string,description:string,error:decimal,floor:decimal,lat:decimal,locality:string,'\
                'lon:decimal,postalcode:string,region:string,room:string,speed:decimal,street:string,text:string,timestamp:dateTime,uri:anyURI'
    return txt
    
def run(bot,mess):
    try:
        text = mess.getBody()
        text = text[len("setgeo")+1:]
        user = mess.getFrom()
        #фильтруем только сообщения с непустым телом
        if text:
        # проверяем, указано ли направление перевода
        # если нет, то оставляем значение по умолчанию
            item = xmpp.Node('geoloc', {'xmlns': xmpp.NS_GEOLOC})
            lines = text.splitlines()
            for line in lines:
                command = line.split(' ')
                i = item.addChild(command[0])
                i.addData(command[1])
            jid=''
            query = xmpp.Iq('set', to=jid)
            e = query.addChild('pubsub', namespace=xmpp.NS_PUBSUB)
            p = e.addChild('publish', {'node': xmpp.NS_GEOLOC})
            p.addChild('item', {'id': '0'}, [item])
            bot.send(query)
            txt = 'Geoloc set!'
            return xmpp.Message(mess.getFrom(),txt)
        else:
            txt = help()
            return xmpp.Message(mess.getFrom(),txt)
    except:
      txt = help()
      return xmpp.Message(mess.getFrom(),txt)
      
