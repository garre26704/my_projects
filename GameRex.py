import pygame,sys,keyboard

class Main:
    def __init__(self,titolo="GameRex",larghezza=600,altezza=500,colore_sfondo="black",window=None):
        self.titolo=titolo
        self.larghezza=larghezza
        self.altezza=altezza
        self.colore_sfondo=colore_sfondo
        pygame.init()
        self.clock=pygame.time.Clock()
        self.window=pygame.display.set_mode((self.larghezza,self.altezza))
        pygame.display.set_caption(self.titolo)
        
    def run(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.time.Clock().tick(60)
        pygame.display.flip()
        self.window.fill(self.colore_sfondo)


    def draw_rect(self,larghezza=20,altezza=20,x=0,y=0,colore="white"):
        pygame.draw.rect(self.window,colore,(x,y,larghezza,altezza))
        
    def draw_ellipse(self,larghezza=20,altezza=20,x=0,y=0,colore="white"):
        pygame.draw.ellipse(self.window,colore,(x,y,larghezza,altezza))

    def draw_circle(self,radius,x,y,colore="white"):
        pygame.draw.circle(self.window,colore,(x,y),radius)
        
    def draw_line(self,colore="white",ix=0,iy=0,ex=255,ey=255):
        pygame.draw.line(self.window,colore,(ix,iy),(ex,ey))
        
    def draw_polygon(self,colore="green",p1x=0,p1y=0,p2x=0,p2y=0,p3x=0,p3y=0):
        pygame.draw.polygon(self.window,colore,((p1x,p1y),(p2x,p2y),(p3x,p3y)),0)
        
    def collide_box(self,oggetto2):
        if self.x+self.larghezza>oggetto2.x and self.x<oggetto2.x+oggetto2.larghezza:
            if self.y+self.altezza>oggetto2.y and self.y<oggetto2.y+oggetto2.altezza:
                return True
   
class GameObject:
    def __init__(self,finestra,path,x,y):
        self.schermo=finestra
        self.superfice=finestra.window
        self.path=path
        self.x=x
        self.y=y
        self.immage=pygame.image.load(self.path)
        self.box_collide=self.immage.get_rect(topleft=(self.x,self.y))
        self.disegna_sprite()
    def disegna_sprite(self):
        self.superfice.blit(self.immage,(self.x,self.y))
        
    def centro(self):
        self.x=self.schermo.larghezza/2
        self.y=self.schermo.altezza/2
        
    def collide_box(self,oggetto2):
        self.collide_object=oggetto2.box_collide
        if self.box_collide.colliderect(self.collide_object):
            return True


        
class controls:
    def __init__(self):
        self.pressed=False
    def is_pressed(self,tasto):
        if keyboard.is_pressed(tasto):
            return True
    def on_press(self,tasto):
        if keyboard.is_pressed(tasto) and self.pressed==False:
            self.pressed=True
            return True
        if keyboard.is_pressed(tasto)==False and self.pressed==True:
            self.pressed=False
            
    def mouse_pos(self):
        return pygame.mouse.get_pos()


    
if __name__ == "__main__":
    pass
