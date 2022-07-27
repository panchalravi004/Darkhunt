from re import X
from tkinter import Y
from turtle import bgcolor
from matplotlib.pyplot import text
import pygame
from pygame.locals import *
from pygame import *

class Button:
    def __init__(self,text,x,y,width,height,bgcolor,hovercolor,fontsize,fontcolor,fonthovercolor):
        self.x = y
        self.y = y
        self.width = width
        self.height = height
        self.bgcolor = bgcolor
        self.hovercolor = hovercolor
        self.fontsize = fontsize
        self.fontcolor = fontcolor
        self.fonthovercolor = fonthovercolor
        self.text = text
        self.surf = pygame.surface.Surface((self.width, self.height))
        self.surf.fill(self.bgcolor)
        self.rect = self.surf.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        self.tempfontcolor = fontcolor

    def draw(self,surface):
        action = False

        font = pygame.font.SysFont('arial', self.fontsize, 2)
        text = font.render(str(self.text),True,self.fontcolor)
        textwidth = text.get_width()
        textheight = text.get_height()

        # get mouse position
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            self.surf.fill(self.hovercolor)
            self.fontcolor = self.fonthovercolor

            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        else:
            self.surf.fill(self.bgcolor)
            self.fontcolor = self.tempfontcolor

        if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            
        surface.blit(self.surf,(self.rect.x,self.rect.y))
        surface.blit(text,((self.rect.x + (self.surf.get_width()/2) - (textwidth/2)),(self.rect.y  + (self.surf.get_height()/2) - (textheight/2))))

        return action
    def msg(self,surface,text,position,fontsize=14,fontcolor=(255,255,255),fontbg=(0,0,0)):
        font = pygame.font.SysFont('arial', fontsize, 2)
        text = font.render(str(text),True,fontcolor)
        textwidth = text.get_width()
        textheight = text.get_height()

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if position == "top":
                surface.blit(text,((self.rect.x + (self.surf.get_width() / 2) - (textwidth / 2)),(self.rect.y - textheight)))

            elif position == "bottom":
                surface.blit(text,((self.rect.x + (self.surf.get_width() / 2) - (textwidth / 2)),(self.rect.y + self.surf.get_height())))

            elif position == "left":
                surface.blit(text,((self.rect.x - textwidth - 2),(self.rect.y + (self.surf.get_height() / 2) - (textheight / 2))))

            elif position == "right":
                surface.blit(text,((self.rect.x + self.surf.get_width() + 4),(self.rect.y + (self.surf.get_height() / 2) - (textheight / 2))))

        else:
            pass

class ImageButton:
    def __init__(self,text,x,y,width,height,bgimage,hoverimage,fontsize,fontcolor,fonthovercolor):
        self.x = y
        self.y = y
        self.width = width
        self.height = height
        self.bgimage = bgimage
        self.hoverimage = hoverimage
        self.fontsize = fontsize
        self.fontcolor = fontcolor
        self.fonthovercolor = fonthovercolor
        self.text = text
        self.surf = pygame.transform.scale(bgimage,(width,height))
        self.rect = self.surf.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        self.tempfontcolor = fontcolor

    def draw(self,surface):
        action = False

        font = pygame.font.SysFont('arial', self.fontsize, 2)
        text = font.render(str(self.text),True,self.fontcolor)
        textwidth = text.get_width()
        textheight = text.get_height()

        # get mouse position
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            self.surf = pygame.transform.scale(self.hoverimage,(self.width,self.height))
            self.fontcolor = self.fonthovercolor

            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        else:
            self.surf = pygame.transform.scale(self.bgimage,(self.width,self.height))
            self.fontcolor = self.tempfontcolor

        if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            
        surface.blit(self.surf,(self.rect.x,self.rect.y))
        surface.blit(text,((self.rect.x + (self.surf.get_width()/2) - (textwidth/2)),(self.rect.y  + (self.surf.get_height()/2) - (textheight/2))))

        return action
    def msg(self,surface,text,position,fontsize=14,fontcolor=(255,255,255),fontbg=(0,0,0)):
        font = pygame.font.SysFont('arial', fontsize, 2)
        text = font.render(str(text),True,fontcolor)
        textwidth = text.get_width()
        textheight = text.get_height()

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if position == "top":
                surface.blit(text,((self.rect.x + (self.surf.get_width() / 2) - (textwidth / 2)),(self.rect.y - textheight)))

            elif position == "bottom":
                surface.blit(text,((self.rect.x + (self.surf.get_width() / 2) - (textwidth / 2)),(self.rect.y + self.surf.get_height())))

            elif position == "left":
                surface.blit(text,((self.rect.x - textwidth - 2),(self.rect.y + (self.surf.get_height() / 2) - (textheight / 2))))

            elif position == "right":
                surface.blit(text,((self.rect.x + self.surf.get_width() + 4),(self.rect.y + (self.surf.get_height() / 2) - (textheight / 2))))

        else:
            pass
