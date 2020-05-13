# -*- coding: UTF-8 -*-

import os
import itchat
from itchat.content import *
from datetime import datetime

def method(call):
    def wrapper(*args, **kwargs):
        return call(*args, **kwargs)
    return wrapper

class weixin:
    
    _autoreplaylist=['Silver','Raymond']
    _ownname=''
    _newIn=itchat.new_instance()
    
    def __init__(self):
        self._newIn.auto_login(statusStorageDir='newInstance.pkg',loginCallback=self._loginCallback, exitCallback=self._exitCallback)
        self._ownname=self.getFriends(isown=True)['NickName']
        self._newIn.run()
        self._newIn.send('test, filehelper',toUserName='filehelper')
        
    def SentChatRoomsMsg(self,name,context):
        
        self._newIn.get_chatrooms(update=True)
        iRoom = self._newIn.search_chatrooms(name)
        
        for room in iRoom:
            if room['NickName'] == name:
                userName = room['UserName']
                break
            
        itchat.send_msg(context, userName)
        print("发送时间：" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
                "发送到：" + name + "\n"
                "发送内容：" + context)
    
    @method    
    @_newIn.msg_register([TEXT,MAP,CARD,NOTE,SHARING])    
    def text_replay(self,msg):
        print(msg.fromUserName)
        print(msg.text)
        msg.user.send('%s: %s' % (msg.type,msg.text))
    
    
    def getChatroom(self):
        
        chatrooms=itchat.get_chatrooms(update=True)
        return chatrooms
    
    
    def getFriends(self,item='',isown=False):
        friendlist=self._newIn.get_friends(update=True)
        print (friendlist)
        if item!='':
            f=[]
            for friend in friendlist[1:]:
                f.append(friend[item])
                return f
            
        if isown:
            return friendlist[0]
        
        return friendlist
    

    def _loginCallback(self):
        pass
    
    def _exitCallback(self):
        pass



class clientcall:
    
    def __init__(self):
        pass
        
    def connect(self):
        pass
    
            