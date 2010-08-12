#!/usr/bin/python
# -*- coding: UTF-8 -*-
import xmpp

def init(bot):
  return 50

def description():
  return 'set activity status(XEP-0108)'

#XEP-0108: User Mood
def help():
    txt = 'Set activity status bot (XEP-0108) (v0.1)\n\n'
    txt = txt+ 'Синтаксис: setactivity статус подстатус текст_статуса\n'
    txt = txt+ 'Статусы: подстатусы\n'
    txt = txt+ '- doing_chores: buying_groceries, cleaning, cooking, doing_maintenance ,doing_the_dishes ,doing_the_laundry, gardening, running_an_errand, walking_the_dog\n'
    txt = txt+ '- drinking: having_a_beer, having_coffee, having_tea\n'
    txt = txt+ '- eating: having_a_snack, having_breakfast, having_dinner, having_lunch\n'
    txt = txt+ '- exercising: cycling, dancing, hiking, jogging, playing_sports, running, skiing, swimming, working_out\n'
    txt = txt+ '- grooming: at_the_spa, brushing_teeth, getting_a_haircut, shaving, taking_a_bath, taking_a_shower\n'
    txt = txt+ '- having_appointment\n'
    txt = txt+ '- inactive: day_off, hanging_out, hiding, on_vacation, praying, scheduled_holiday, sleeping, thinking\n'
    txt = txt+ '- relaxing: fishing, gaming, going_out, partying, reading, rehearsing, shopping, smoking, socializing, sunbathing, watching_tv, watching_a_movie\n'
    txt = txt+ '- talking: in_real_life, on_the_phone, on_video_phone\n'
    txt = txt+ '- traveling: commuting, cycling, driving, in_a_car, on_a_bus, on_a_plane, on_a_train, on_a_trip, walking\n'
    txt = txt+ '- working: coding, in_a_meeting, studying, writing\n'
    return txt
    
def run(bot,mess):
    try:
      text = mess.getBody()
      command = text.split(' ')
      activity=command[1]
      subactivity=command[2]
      text = text[len("setactivity")+1:]
      l = len(activity)+1+len(subactivity)
      text = unicode(text[l+1:])
      item = xmpp.Node('activity', {'xmlns': xmpp.NS_ACTIVITY})
      if activity:
          i = item.addChild(activity)
          i.addChild(subactivity)
      if text:
          i = item.addChild('text')
          i.addData(text)
      
      jid=''
      query = xmpp.Iq('set', to=jid)
      e = query.addChild('pubsub', namespace=xmpp.NS_PUBSUB)
      p = e.addChild('publish', {'node': xmpp.NS_ACTIVITY})
      p.addChild('item', {'id': '0'}, [item])
      
      bot.send(query)
      
      txt = 'Status activity set!'
      return xmpp.Message(mess.getFrom(),txt)
    except:
      txt = help()
      return xmpp.Message(mess.getFrom(),txt)
      

