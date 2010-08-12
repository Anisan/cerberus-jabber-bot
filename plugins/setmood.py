#!/usr/bin/python
# -*- coding: UTF-8 -*-
import xmpp

def init(bot):
  return 50

def description():
  return 'set mood status(XEP-0107)'

#XEP-0107: User Mood
def help():
    txt = 'Set mood status bot (XEP-0107) (v0.1)\n\n'
    txt = txt+ 'Синтаксис: setmood статус текст_статуса\n'
    txt = txt+ 'Статусы :\n'
    txt = txt+ 'afraid -- Под впечатлением от страха или опасений, в страхе, страх.\n'
    txt = txt+ 'amazed -- Astonished; confounded with fear, surprise or wonder.\n'
    txt = txt+ 'amorous -- Inclined to love; having a propensity to love, or to sexual enjoyment; loving, fond, affectionate, passionate, lustful, sexual, etc.\n'
    txt = txt+ 'angry -- Displaying or feeling anger, i.e., a strong feeling of displeasure, hostility or antagonism towards someone or something, usually combined with an urge to harm.\n'
    txt = txt+ 'annoyed -- To be disturbed or irritated, especially by continued or repeated acts.\n'
    txt = txt+ 'anxious -- Full of anxiety or disquietude; greatly concerned or solicitous, esp. respecting something future or unknown; being in painful suspense.\n'
    txt = txt+ 'aroused -- To be stimulated in one`s feelings, especially to be sexually stimulated.\n'
    txt = txt+ 'ashamed -- Feeling shame or guilt.\n'
    txt = txt+ 'bored -- Suffering from boredom; uninterested, without attention.\n'
    txt = txt+ 'brave -- Strong in the face of fear; courageous. \n'
    txt = txt+ 'calm -- Мирное, спокойное.\n'
    txt = txt+ 'cautious -- Taking care or caution; tentative.\n'
    txt = txt+ 'cold -- Feeling the sensation of coldness, especially to the point of discomfort.\n'
    txt = txt+ 'confident -- Feeling very sure of or positive about something, especially about one`s own capabilities.\n'
    txt = txt+ 'confused -- Chaotic, jumbled or muddled.\n'
    txt = txt+ 'contemplative -- Feeling introspective or thoughtful.\n'
    txt = txt+ 'contented -- Pleased at the satisfaction of a want or desire; satisfied.\n'
    txt = txt+ 'cranky -- Grouchy, irritable; easily upset.\n'
    txt = txt+ 'crazy -- Feeling out of control; feeling overly excited or enthusiastic.\n'
    txt = txt+ 'creative -- Feeling original, expressive, or imaginative.\n'
    txt = txt+ 'curious -- Inquisitive; tending to ask questions, investigate, or explore.\n'
    txt = txt+ 'dejected -- Feeling sad and dispirited.\n'
    txt = txt+ 'depressed -- Severely despondent and unhappy.\n'
    txt = txt+ 'disappointed -- Defeated of expectation or hope; let down.\n'
    txt = txt+ 'disgusted -- Filled with disgust; irritated and out of patience.\n'
    txt = txt+ 'dismayed -- Feeling a sudden or complete loss of courage in the face of trouble or danger.\n'
    txt = txt+ 'distracted -- Having one`s attention diverted; preoccupied.\n'
    txt = txt+ 'embarrassed -- Having a feeling of shameful discomfort.\n'
    txt = txt+ 'envious -- Feeling pain by the excellence or good fortune of another.\n'
    txt = txt+ 'excited -- Having great enthusiasm.\n'
    txt = txt+ 'flirtatious -- In the mood for flirting.\n'
    txt = txt+ 'frustrated -- Suffering from frustration; dissatisfied, agitated, or discontented because one is unable to perform an action or fulfill a desire.\n'
    txt = txt+ 'grateful -- Feeling appreciation or thanks.\n'
    txt = txt+ 'grieving -- Feeling very sad about something, especially something lost; mournful; sorrowful.\n'
    txt = txt+ 'grumpy -- Unhappy and irritable.\n'
    txt = txt+ 'guilty -- Feeling responsible for wrongdoing; feeling blameworthy.\n'
    txt = txt+ 'happy -- Experiencing the effect of favourable fortune; having the feeling arising from the consciousness of well-being or of enjoyment; enjoying good of any kind, as peace, tranquillity, comfort; contented; joyous.\n'
    txt = txt+ 'hopeful -- Having a positive feeling, belief, or expectation that something wished for can or will happen.\n'
    txt = txt+ 'hot -- Feeling the sensation of heat, especially to the point of discomfort.\n'
    txt = txt+ 'humbled -- Having or showing a modest or low estimate of one`s own importance; feeling lowered in dignity or importance.\n'
    txt = txt+ 'humiliated -- Feeling deprived of dignity or self-respect.\n'
    txt = txt+ 'hungry -- Having a physical need for food.\n'
    txt = txt+ 'hurt -- Wounded, injured, or pained, whether physically or emotionally.\n'
    txt = txt+ 'impressed -- Favourably affected by something or someone.\n'
    txt = txt+ 'in_awe -- Feeling amazement at something or someone; or feeling a combination of fear and reverence.\n'
    txt = txt+ 'in_love -- Feeling strong affection, care, liking, or attraction..\n'
    txt = txt+ 'indignant -- Showing anger or indignation, especially at something unjust or wrong.\n'
    txt = txt+ 'interested -- Showing great attention to something or someone; having or showing interest.\n'
    txt = txt+ 'intoxicated -- Under the influence of alcohol; drunk.\n'
    txt = txt+ 'invincible -- Feeling as if one cannot be defeated, overcome or denied.\n'
    txt = txt+ 'jealous -- Fearful of being replaced in position or affection.\n'
    txt = txt+ 'lonely -- Feeling isolated, empty, or abandoned.\n'
    txt = txt+ 'lost -- Unable to find one`s way, either physically or emotionally.\n'
    txt = txt+ 'lucky -- Feeling as if one will be favored by luck.\n'
    txt = txt+ 'mean -- Causing or intending to cause intentional harm; bearing ill will towards another; cruel; malicious.\n'
    txt = txt+ 'moody -- Given to sudden or frequent changes of mind or feeling; temperamental.\n'
    txt = txt+ 'nervous -- Easily agitated or alarmed; apprehensive or anxious.\n'
    txt = txt+ 'neutral -- Not having a strong mood or emotional state.\n'
    txt = txt+ 'offended -- Feeling emotionally hurt, displeased, or insulted. \n'
    txt = txt+ 'outraged -- Feeling resentful anger caused by an extremely violent or vicious attack, or by an offensive, immoral, or indecent act.\n'
    txt = txt+ 'playful -- Interested in play; fun, recreational, unserious, lighthearted; joking, silly.\n'
    txt = txt+ 'proud -- Feeling a sense of ones own worth or accomplishment.\n'
    txt = txt+ 'relaxed -- Having an easy-going mood; not stressed; calm.\n'
    txt = txt+ 'relieved -- Feeling uplifted because of the removal of stress or discomfort.\n'
    txt = txt+ 'remorseful -- Feeling regret or sadness for doing something wrong.\n'
    txt = txt+ 'restless -- Without rest; unable to be still or quiet; uneasy; continually moving.\n'
    txt = txt+ 'sad -- Feeling sorrow; sorrowful, mournful.\n'
    txt = txt+ 'sarcastic -- Mocking and ironical.\n'
    txt = txt+ 'satisfied -- Pleased at the fulfillment of a need or desire.\n'
    txt = txt+ 'serious -- Without humor or expression of happiness; grave in manner or disposition; earnest; thoughtful; solemn.\n'
    txt = txt+ 'shocked -- Surprised, startled, confused, or taken aback.\n'
    txt = txt+ 'shy -- Feeling easily frightened or scared; timid; reserved or coy.\n'
    txt = txt+ 'sick -- Feeling in poor health; ill.\n'
    txt = txt+ 'sleepy -- Feeling the need for sleep.\n'
    txt = txt+ 'spontaneous -- Acting without planning; natural; impulsive.\n'
    txt = txt+ 'stressed -- Suffering emotional pressure.\n'
    txt = txt+ 'strong -- Capable of producing great physical force; or, emotionally forceful, able, determined, unyielding.\n'
    txt = txt+ 'surprised -- Experiencing a feeling caused by something unexpected.\n'
    txt = txt+ 'thankful -- Showing appreciation or gratitude.\n'
    txt = txt+ 'thirsty -- Feeling the need to drink.\n'
    txt = txt+ 'tired -- In need of rest or sleep.\n'
    txt = txt+ 'undefined -- [Feeling any emotion not defined here.]\n'
    txt = txt+ 'weak -- Lacking in force or ability, either physical or emotional.\n'
    txt = txt+ 'worried -- Thinking about unpleasant things that have happened or that might happen; feeling afraid and unhappy.\n'
    return txt
    
def run(bot,mess):
    try:
      text = mess.getBody()
      command = text.split(' ')
      mood=command[1]
      text = text[len("setmood")+1:]
      l = len(mood)
      text = unicode(text[l+1:])
      item = xmpp.Node('mood', {'xmlns': xmpp.NS_MOOD})
      if mood:
          item.addChild(mood)
      if text:
          i = item.addChild('text')
          i.addData(text)
      
      jid=''
      query = xmpp.Iq('set', to=jid)
      e = query.addChild('pubsub', namespace=xmpp.NS_PUBSUB)
      p = e.addChild('publish', {'node': xmpp.NS_MOOD})
      p.addChild('item', {'id': '0'}, [item])
      
      bot.send(query)
      
      txt = 'Status mood set!'
      return xmpp.Message(mess.getFrom(),txt)
    except:
      txt = help()
      return xmpp.Message(mess.getFrom(),txt)
      

