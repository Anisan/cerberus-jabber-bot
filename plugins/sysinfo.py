#!/usr/bin/python
# -*- coding: UTF-8 -*-
import xmpp

def init(bot):
  return 50

def description():
  return 'System information'

def descPlugin(command,bot):
  plugin = getattr(bot.plugins['plugins'],command)
  return plugin.description()

def run(bot,mess):
        status = []
        status.append('-= System information =-')

        load_file = open('/proc/loadavg')
        load = load_file.readline()
        load = load[:len(load)-1]
        load_file.close()
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
        return xmpp.Message(mess.getFrom(),status)
