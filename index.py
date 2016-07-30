import web
import os
import time   
import hashlib
import lxml  
import random  
from lxml import etree     



urls = (
  '/', 'index'    )

app = web.application(urls, globals())

class index:

 def __init__(self):                                                                                                                        
        self.app_root = os.path.dirname(__file__)                                                                                              
        self.templates_root = os.path.join(self.app_root, 'templates')                                                                         
        self.render = web.template.render(self.templates_root)                                                                                 
                                                                

 def GET(self):                                                                                                                             
        # verification                                                                                                         
        data = web.input()                                                                                                                     
        signature=data.signature                                                                                                               
        timestamp=data.timestamp                                                                                                               
        nonce=data.nonce                                                                                                                       
        echostr=data.echostr

        token="deepocean1991" 
                                                                                                              
        list=[token,timestamp,nonce]                                                                                                           
        list.sort()                                                                                                                            
        sha1=hashlib.sha1()                                                                                                                    
        map(sha1.update,list)                                                                                                                  
        hashcode=sha1.hexdigest()  
                                                                                                                                                        
        if hashcode == signature:                                                                                                              
            return echostr    

 def POST(self):                                                                                                                            

	print 'entering post handling......'

        str_xml = web.data() #*~N***~Wpost*~]**~Z~D*~U**~M*                                                                                    
        xml = etree.fromstring(str_xml)#**~[**~LXML****~^~P                                                                                    
       # content=xml.find("Content").text#*~N***~W*~T**~H**~I~@**~S*~E**~Z~D*~F~E***                                                           
        msgType=xml.find("MsgType").text                                                                                                       
        fromUser=xml.find("FromUserName").text                                                                                                 
        toUser=xml.find("ToUserName").text                                                                                                     

        if msgType == 'text':                                                                                                                  
            content=xml.find("Content").text                                                                                                   
	
	    print content
                                                                                                                                               
            if content.lower() == 'menu':                                                                                                      
		replyText = u'hello,i got it'
                return self.render.reply_text(fromUser,toUser,int(time.time()),replyText)                                                     
                                                                                                                                               
                                                                                                                                               

if __name__ == "__main__": 
	app.run()
