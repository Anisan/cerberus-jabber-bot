#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import urllib
import urllib2
        
myProxy = {'https':'http://»суповј:Fylhtq@128.0.20.5:80/',\
           'http':'http://»суповј:Fylhtq@128.0.20.5:80/'}

proxy_enabled = True

class ProxyPasswordMgr:    
 def __init__(self):        
    self.user = self.passwd = None    
 def add_password(self, realm, uri, user, passwd):
    self.user = user        
    self.passwd = passwd    
 def find_user_password(self, realm, authuri): 
    return self.user, self.passwd

def resize(path,th_path,bw):
    import PIL
    from PIL import Image

    basewidth = bw
    img = Image.open(path)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
    img.save(th_path)
    
def img_to_base64(file):
    # note: binary read "rb" is required!
    # this gives a one line string ...
    #jpg_text = 'jpg1_b64 = \\\n"""' + base64.b64encode(open(jpgfile,"rb").read()) + '"""'
    # another option, inserts newlines about every 76 characters, easier to copy and paste!
    jpg_text = base64.encodestring(open(file,"rb").read())
    return jpg_text

def base64_to_img(imgData,imgpath):   
    fh = open(imgpath, "wb")
    fh.write(imgData.decode('base64'))
    fh.close()
    
def get_img(img_url):
    try:
        proxy = urllib2.ProxyHandler(myProxy)
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)
        response = urllib2.urlopen(img_url)
        img = response.read()
        return {'base64_img': img.encode('base64'),
                'content-type': response.info()['Content-Type']}
    except Exception,e:
        return {'base64_img': '',
                'content-type': ''}    
                
def get_img2(img_url):
    try:
        if proxy_enabled:
            proxy = "128.0.20.5:80"
            user = "»суповј"
            password = "Fylhtq"
            proxy = urllib2.ProxyHandler({"http" : proxy})
            proxy_auth_handler = urllib2.ProxyBasicAuthHandler(ProxyPasswordMgr())
            proxy_auth_handler.add_password(None, None, user, password)
            opener = urllib2.build_opener(proxy,proxy_auth_handler)
            urllib2.install_opener(opener)
        response = urllib2.urlopen(img_url)
        img = response.read()
        return {'base64_img': img.encode('base64'),
                'content-type': response.info()['Content-Type']}
    except:
        return 'Error get img'      