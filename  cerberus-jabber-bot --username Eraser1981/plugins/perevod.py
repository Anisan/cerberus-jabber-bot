#!/usr/bin/python
# -*- coding: utf-8 -*-
import string, re
import xmpp
import urllib2,urllib
import simplejson as json
import utils.db as db


def translate(text, langpair):
    #формируем ссылку
    query = urllib.urlencode({'q' : text.encode("utf-8"), 'langpair' : langpair})
    url = u'http://ajax.googleapis.com/ajax/services/language/translate?v=1.0&%s'.encode("utf-8") \
        % (query)
    #спрашиваем перевод у гугла
    result = urllib2.urlopen(url)
    response = json.loads(result.read())
    if response['responseStatus'] != 200:
        #если что-то не так, показываем сообщение об ошибке
        mess = response['responseDetails']
    else:
        # показываем перевод
        mess = response['responseData']['translatedText']
    return mess


def init(bot):
  db.execNonQuery(bot.dbpath,"CREATE TABLE IF NOT EXISTS langpairs(jid, langpair)")
  return 0

def description():
  return 'переводчик'

def run(bot,mess):
    text = mess.getBody()
    text = text[len("perevod")+1:]
    user = mess.getFrom()
    user=str(user).split('/')[0]
    # направление перевода по умолчанию
    langpair = db.execQuery(bot.dbpath,"select langpair,count(*) from langpairs where jid='%s'"%(str(user),))[0][0]
    if langpair==None:
        langpair = 'en|ru'
        db.execNonQuery(bot.dbpath,"insert into langpairs(jid, langpair) values ('%s','%s')"%(str(user),langpair,))
    #фильтруем только сообщения с непустым телом
    if text:
    # проверяем, указано ли направление перевода
    # если нет, то оставляем значение по умолчанию
        lines = text.splitlines()
        regexp = re.compile('^\w{2}\|\w{2}$', re.IGNORECASE)
        if regexp.match(lines[0]):
            langpair = lines[0]
            cdb.execNonQuery(bot.dbpath,"update langpairs set langpair='%s' where jid='%s'"%(langpair,str(user),))
            del lines[0]
        text  = string.join(lines)
        reply = '['+langpair+'] '+translate(text, langpair)
        return xmpp.Message(mess.getFrom(),reply)
