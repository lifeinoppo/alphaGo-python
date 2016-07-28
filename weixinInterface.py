# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import random
import pylibmc
import db
from lxml import etree
from youdao import youdao
from book  import query_book
class WeixinInterface:
 
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)
 
    def GET(self):
        #获取输入参数
        data = web.input()
        signature=data.signature
        timestamp=data.timestamp
        nonce=data.nonce
        echostr=data.echostr
        #自己的token
        token="xxx" #这里改写你在微信公众平台里输入的token
        #字典序排序
        list=[token,timestamp,nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hashcode=sha1.hexdigest()
        #sha1加密算法        
 
        #如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr
  
    
    def POST(self):        
        str_xml = web.data() #获得post来的数据
        xml = etree.fromstring(str_xml)#进行XML解析
       # content=xml.find("Content").text#获得用户所输入的内容
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        mc = pylibmc.Client() #初始化一个memcache实例用来保存用户的操作 memcache它可以应对任意多个连接，使用非阻塞的网络IO
       #关注事件的提醒
        if msgType == "event":
            mscontent = xml.find("Event").text
         
            if mscontent == "subscribe":
                replayText = u'''欢迎关注本微信,哈哈~！在这里我会不定期推送有关大数据、云计算方面的内容。\n功能列表：1.输入t+中文或者英文返回对应的英中翻译\n2.输入【m】随机来首音乐听，建议在wifi下听\n3.输入【Ly+你的留言内容】,来给我留言\n4.【博客地址】 http://blog.csdn.net/zwto1\n 5.【查阅书籍信息】输入书籍名，便可查看相关书籍信息。\n\n你可以【查看历史消息】来看已发布过的自己感兴趣的内容，也可以输入【menu】去探索我开发的一些功能。 '''
                return self.render.reply_text(fromUser,toUser,int(time.time()),replayText)                                                                
          
            if mscontent == "unsubscribe":
                replayText = u'我现在功能还很简单，知道满足不了您的需求，但是我会慢慢改进，欢迎您以后再来'
                return self.render.reply_text(fromUser,toUser,int(time.time()),replayText)

         #help指令的识别
        if msgType == 'text':
            content=xml.find("Content").text
          
            if content.lower() == 'menu':
                replayText = u'''1.输入t+中文或者英文返回对应的英中翻译\n2.输入【m】随机来首音乐听，建议在wifi下听\n3.输入【Ly+你的留言内容】,来给我留言\n4.【博客地址】 http://blog.csdn.net/zwto1\n 5.【查阅书籍信息】输入书籍名，便可查看相关书籍信息\n\n 不要忘记你可以【查看历史消息】来看已发布过的自己感兴趣的内容哟^_^''' #3.输入【xhj】进入调戏小黄鸡模式\n
                return self.render.reply_text(fromUser,toUser,int(time.time()),replayText)
                             
            
            #音乐随机播放
            if content.lower() == 'm':
                musicList = [
                             [r'','Destiny',u'献给虫虫'],            # r 后加音乐链接
                             [r'','5 Days',u'献给虫虫'],
                             [r'','Far Away (Album Version)',u'献给虫虫'],
                             [r'',u'少年游',u'献给虫虫'],
                                                     
                             ]

                music = random.choice(musicList)
                musicurl = music[0]
                musictitle = music[1]
                musicdes =music[2]
                return self.render.reply_music(fromUser,toUser,int(time.time()),musictitle,musicdes,musicurl)
              
            if content.startswith('ly'):
                fktime = time.strftime('%Y-%m-%d %H:%M',time.localtime())        
                db.addfk(fromUser,fktime,content[2:].encode('utf-8'))   
                return self.render.reply_text(fromUser,toUser,int(time.time()),u'感谢你的留言') 


            elif type(content).__name__ == "unicode":
              content = content.encode('UTF-8')

            if(content.startswith('t')):

                Nword = youdao(content[1:])        
                return self.render.reply_text(fromUser,toUser,int(time.time()),Nword) 

            else:
               book = query_book(content)
               if book == '':
                  return self.render.reply_text(fromUser,toUser,int(time.time()),u'对不起，你查找的图书不存在！') 
               else:    
             # description = query_book_details()
                 book_title = book["title"]
                 book_img = book["images"]["large"]
                 description = book["summary"]
                 book_alt = book['alt']
             
                 return self.render.reply_tw(fromUser,toUser,int(time.time()), book_title, description,book_img, book_alt) 

              

    
    
