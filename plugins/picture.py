#!/usr/bin/python
# -*- coding: utf-8 -*-
import xmpp
import urllib2,urllib
import simplejson as json
import utils.db as db
import pywapi
import xml
import utils

def init(bot):
  return 70

def description():
  return "изображения из Internet через XEP-0071"
  
def help():
  txt = 'Изображения из Internet через XEP-0071(v0.2)\n\n'
  return txt
  
def run(bot,mess):
    text = mess.getBody()
    text = text[len('picture')+1:]
    user = mess.getFrom()
    user=str(user).split('/')[0]
    if text:
        
            
        ext =''
        extl = text.split('.')
        for i in extl:
            ext=i
        image = utils.pic.get_img(text)
        img=image['base64_img']
        # уменьшить картинку, а то если большая то дисконнект
        try:
            utils.pic.base64_to_img(img,"temp."+ext)
            bw = 800
            while (len(img.encode('utf-8'))>30000):
                utils.pic.resize("temp."+ext,"sm_temp."+ext,bw)
                bw = bw - 50
                img = utils.pic.img_to_base64("sm_temp."+ext)
        except Exception,e:
                print "res "+str(e)
        
        curr = '<img src="data:image/%s;base64,%s" alt="img"/>' % (ext,img.encode('utf-8'))
        body=xmpp.simplexml.XML2Node('<body xmlns="%s"><a href="%s">Image - %s</a><br/>%s</body>' %
                                    ('http://www.w3.org/1999/xhtml',text,text,curr))
        message=xmpp.protocol.Message(mess.getFrom(), 'Image XEP-0071',typ='chat')        
        message.addChild('html', {}, [body,], xmpp.NS_XHTML_IM)
        return message
    else:
        txt = help()
        return xmpp.Message(mess.getFrom(),txt,typ='chat')

  
