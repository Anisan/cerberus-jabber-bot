#!/usr/bin/python
# -*- coding: UTF-8 -*-
import xmpp
import time
import threading

work=True
timer=30

class MonitorThread(threading.Thread):
    # Override Thread's __init__ method to accept the parameters needed:
    def __init__(self, bot):
        self.jbot = bot
        threading.Thread.__init__(self)

    def run(self):
        global work
        work=True
        global timer
        while work:
            try:
                status = []
                
                load_file = open('/proc/loadavg')
                load = load_file.readline()
                load = load[:len(load)-1]
                load_file.close()
                cpuavg = load.split(' ')
                load = 'Load average: %s' % load
                status.append(load)

                # calculate the uptime
                uptime_file = open('/proc/uptime')
                uptime = uptime_file.readline().split()[0]
                uptime_file.close()

                uptime = float(uptime)
                (uptime,secs) = (int(uptime / 60), uptime % 60)
                (uptime,mins) = divmod(uptime,60)
                (days,hours) = divmod(uptime,24)

                uptime = 'Uptime: %d day%s, %d:%02d' % (days, days != 1 and 's' or '', hours, mins)
                status.append(uptime)

                # calculate memory and swap usage
                meminfo_file = open('/proc/meminfo')
                meminfo = {}
                for x in meminfo_file:
                    try:
                        (key,value,junk) = x.split(None, 2)
                        key = key[:-1] # strip off the trailing ':'
                        meminfo[key] = int(value)
                    except:
                        pass
                meminfo_file.close()

                memusage = 'Memory used: %d of %d kB (%d%%) - %d kB free' \
                           % (meminfo['MemTotal']-meminfo['MemFree'],
                              meminfo['MemTotal'],
                              100 - (100*meminfo['MemFree']/meminfo['MemTotal']),
                              meminfo['MemFree'])
                status.append(memusage)
                if meminfo['SwapTotal']:
                    swapusage = 'Swap used: %d of %d kB (%d%%) - %d kB free' \
                              % (meminfo['SwapTotal']-meminfo['SwapFree'],
                                 meminfo['SwapTotal'],
                                 100 - (100*meminfo['SwapFree']/meminfo['SwapTotal']),
                                 meminfo['SwapFree'])
                    status.append(swapusage)

                status = '\n'.join(status)
                cpuavg = float(str(cpuavg[0]))
                icon = 'chat'
                if (cpuavg>0.3): icon = 'online'
                if (cpuavg>0.7): icon = 'away'
                if (cpuavg>1.0): icon = 'xa'
                if (cpuavg>1.4): icon = 'dnd'
                if (cpuavg>1.8): icon = 'invisible'
                presence = xmpp.Presence(status = status, show = icon, priority = self.jbot.config['priority'])
                self.jbot.send(presence)
                print 'set'
            except Exception,e:
                print 'Monitoring error'
                print e
            time.sleep(timer)
        presence = xmpp.Presence(status = "", show = "online", priority = '0')
        self.jbot.send(presence)
        


def init(bot):
  return 100

def description():
  return 'Monitoring system status'

def help():
    txt = 'Monitoring system status (v0.2)\n\n'
    txt = txt+ 'enabled - включить\n'
    txt = txt+ 'disabled - выключить\n'
    txt = txt+ 'timer - установить периодичность(по-умолчанию 30 сек)\n'
    return txt

def run(bot,mess):
      user=mess.getFrom()
      user=str(user).split('/')
      user=user[0]
      text = mess.getBody()
      try:
          command = text.split(' ')
          command = command[1]
          if (command=='help'):
            txt = help()
            bot.send(xmpp.Message(mess.getFrom(),txt))
            return
          if (command=='enabled'):
            monitor=MonitorThread(bot)
            monitor.setName('Monitor')
            monitor.start()
            txt = 'Monitoring enabled!'
            return xmpp.Message(mess.getFrom(),txt)
          if (command=='disabled'):
            global work
            work=False
            txt = 'Monitoring disabled!'
            return xmpp.Message(mess.getFrom(),txt)
            return
          if (command=='timer'):
            global timer
            command = text.split(' ')
            timer=int(command[2])
            txt = 'Monitoring timer set - '+str(timer)+' sec'
            return xmpp.Message(mess.getFrom(),txt)
            return
      except:
        txt = help()
        return xmpp.Message(mess.getFrom(),txt,typ='chat')




