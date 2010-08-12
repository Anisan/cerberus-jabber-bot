# -*- coding: UTF-8 -*-
import xmpp
from xmpp import *

def init(bot):
    if not hasattr(bot, 'Commands'):
        disco = xmpp.browser.Browser()
        disco.PlugIn(bot)
        commands = xmpp.commands.Commands(disco)
        commands.PlugIn(bot)
    commands = bot.Commands
    command = StatCommand()
    command.plugin(commands)
    return -1 #system


  
class StatCommand(xmpp.commands.Command_Handler_Prototype):
    name = 'statistic'
    description = 'Статистика бота'
    def __init__(self, jid=''):
        xmpp.commands.Command_Handler_Prototype.__init__(self,jid)
        self.initial = {
            'execute': self.initialForm
        }

    def initialForm(self, conn, request):
        sessionid = self.getSessionID()
        self.sessions[sessionid] = {
            'jid':request.getFrom(),
            'data':{'type':None}
        }
        request.getTag(name="command").setAttr('sessionid', sessionid)
        return self.statForm(conn, request)
            
    def statForm(self, conn, request):
        sessionid = request.getTagAttr('command','sessionid')
        session = self.sessions[sessionid]

        session['actions'] = {
            'cancel': self.cancel,
        }

        timefield = xmpp.DataField(desc='Время запуска бота',name='time',typ='text-single',value='test')
        timefield.setAttr('label', 'Время запуска')

        form = xmpp.DataForm(
            title='Статистика',
            data=[
                'Статистика использования бота',
                timefield
                ])

        # Build a reply with the form
        reply = request.buildReply('result')
        replypayload = [
            xmpp.Node('actions',
                attrs={'execute':'next'},
                payload=[xmpp.Node('next')]),
            form]
        reply.addChild(
            name='command',
            namespace=NS_COMMANDS,
            attrs={
                'node':request.getTagAttr('command','node'),
                'sessionid':sessionid,
                'status':'completed'},
            payload=replypayload)
        self._owner.send(reply)	# Question: self._owner or conn?
        raise xmpp.NodeProcessed

    def cancel(self, conn, request):
        sessionid = request.getTagAttr('command','sessionid')
        reply = request.buildReply('result')
        reply.addChild(
            name='command',
            namespace=NS_COMMANDS,
            attrs={
                'node':request.getTagAttr('command','node'),
                'sessionid':sessionid,
                'status':'cancelled'})
        self._owner.send(reply)
        del self.sessions[sessionid]
        raise xmpp.NodeProcessed