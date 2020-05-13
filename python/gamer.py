# -*- coding: utf-8 -*-

import pygame
import os
from pygame.locals import *
import sys

def init():
      
    # 定义窗口分辨率
    SCREEN_WH=[800,600]
    subpos=[100,100]

    #初始化
    try:
        pygame.init()
        screen=pygame.display.set_mode(SCREEN_WH)
        pygame.display.set_caption('Gamer')
        
        background=pygame.image.load(os.path.realpath('img/bg01.jpg'))
        
        # print the background
        screen.blit(background,(0,0))
        
        # screen flash
        pygame.display.update()
        
        return screen
        
    except RuntimeError as e:
        print(e)
        return None
    
    
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf=pygame.Surface((40,70))
        self.surf.fill((255,110,220))
        self.rect=self.surf.get_rect()
        
    def screen(self, s):
        self.width=s.get_width()
        print(self.width)
        self.height=s.get_height()
        print(self.height)
        
    def move(self,key):
        #move by the key input
        if key[K_UP]:
            self.rect.move_ip(0,-5)
        if key[K_DOWN]:
            self.rect.move_ip(0,5)
        if key[K_LEFT]:
            self.rect.move_ip(-5,0)
        if key[K_RIGHT]:
            self.rect.move_ip(5,0)
            
        # limit the play in the screen
        if self.rect.left<0:
            self.rect.left=0
        elif self.rect.right>self.width:
            self.rect.right=self.width
        elif self.rect.top<=0:
            self.rect.top=0
        elif self.rect.bottom>=self.height:
            self.rect.bottom=self.height
            
    def sub(self,sub):
        self.sub=sub

def main():
    
    scr=init()
    
    player=Player()
    
    player.screen(scr)
    
    #sub=pygame.image.load(os.path.realpath('img/sub.jpg'))
    #s_rect=pygame.Rect(165,360,102,126)
    
    #s1=sub.subsurface(s_rect)
    
    #player.sub(s1)
    
    
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    
                    
        key=pygame.key.get_pressed()
        
        if key!=0:
            print(key)
        
        player.update(key)
        
        # refresh screen
        scr.blit(player.surf,player.rect)

        pygame.display.flip()
            
            
if __name__=="__main__":
    
    main()
    