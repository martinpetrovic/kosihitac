#pokretanje vanjskih modula
import math
import matplotlib.pyplot as plt
import pygame
pygame.init()
pygame.mixer.init()
#pokretanje prozora
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.Font('freesansbold.ttf', 15)
#neke varijable radi jednostavnosti
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
VRATI_NAZAD_ZVUK = pygame.mixer.Sound("vrati_nazad_zvuk.ogg")
#klasa za gumbe iz potapanja brodova
class Button:

    def __init__(self, text_input, text_size, text_color, rect_width, rect_height, rect_color, hoveringRect_color, pos):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.poz = (pos[0],pos[1])
        #rectangle ispod teksta
        self.main_rect = pygame.Rect(self.x_pos-(rect_width/2), self.y_pos-(rect_height/2), rect_width, rect_height)
        self.main_rect_color, self.hovering_rect_color= rect_color, hoveringRect_color
        #tekst u gumbu
        self.font = pygame.font.Font(None, text_size)
        self.text_surf = self.font.render(text_input, False, text_color)
        self.text_rect = self.text_surf.get_rect(center = self.main_rect.center)

    def update(self, screen):
        pygame.draw.rect(screen, self.main_rect_color, self.main_rect)
        screen.blit(self.text_surf, self.text_rect)

    def checkForInput(self,position):
        if position[0] in range(self.main_rect.left, self.main_rect.right) and position[1] in range(self.main_rect.top, self.main_rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.main_rect.left, self.main_rect.right) and position[1] in range(self.main_rect.top, self.main_rect.bottom):
            self.main_rect_color = self.hovering_rect_color

def simulacija(v,alfa,sy): #sama simulacija odnosno numericki model i crtanje grafa, objašnjeno u word dokumentu
    global t,sx,ymax
    ymax=0
    alfa = alfa*math.pi/180
    vx= v * math.cos(alfa)
    vy= v * math.sin(alfa)
    dt = 0.00001
    g = 9.81
    sx=0
    t=0
    xtocke = []
    ytocke=[]
    if sy ==0:
        t +=dt
        vy = vy-g*dt
        sy += vy*dt
        ytocke.append(sy)
        sx += dt*vx
        xtocke.append(sx)
    while sy > 0:
        t +=dt
        vy = vy-g*dt
        sy += vy*dt
        ytocke.append(sy)
        sx += dt*vx
        xtocke.append(sx)
    if ytocke[-1]<0:
        ytocke[-1]=0
    ymax = max(ytocke)
    plt.plot(xtocke, ytocke)
    plt.xlabel("domet/m")
    plt.ylabel("visina/m")
    plt.title("putanja")
    plt.savefig("slika.png",dpi=100)
def main(): #glavna funkcija u kojoj se sve vrti
    alfa = "Početni kut/ deg"
    sy = "Početna visina/ m"    #natpisi na gumbima za upis podataka
    v = "Početna brzina/ m/s"
    pygame.display.set_caption("Simulacija")
    clock = pygame.time.Clock()
    upiskuta=False
    upisbrzine=False  #varijable za aktivnost upisa podataka
    upisvisine=False
    while True:
        screen.fill(WHITE)
        #kreiranje gumba
        POKRENI_GUMB = Button('Pokreni', 30, 'Black', 100, 40, '#475F77', '#77dd77', (1250, 810))
        RESETIRAJ_GUMB = Button('Resetiraj', 30, 'Black', 100, 40, '#475F77', '#D74B4B', (1400, 810))
        KUT_GUMB = Button(alfa, 30, 'Black', 180, 40, '#475F77', '#77dd77', (1050, 810)) 
        BRZINA_GUMB = Button(v, 30, 'Black', 190, 40, '#475F77', '#77dd77', (850, 810))
        VISINA_GUMB = Button(sy, 30, 'Black', 180, 40, '#475F77', '#77dd77', (650, 810))
        gumbi = [POKRENI_GUMB,RESETIRAJ_GUMB,KUT_GUMB,BRZINA_GUMB,VISINA_GUMB]
        for gumb in gumbi: #provjera za hower boju gumba
            gumb.changeColor(pygame.mouse.get_pos())  
            gumb.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type==pygame.MOUSEBUTTONDOWN:    
                if POKRENI_GUMB.checkForInput(pygame.mouse.get_pos()): #ako je gumb pokreni stisnut pokuša provesti simulaciju
                    try:
                        simulacija(int(float(v)),int(float(alfa)),int(float(sy)))
                        GRAF = pygame.image.load("slika.png" )
                        
                        resetirano = 0
                    except: #ako izbaci error zvuk kaže da nešto nije u redu
                        pygame.mixer.Sound.play(VRATI_NAZAD_ZVUK)
                if RESETIRAJ_GUMB.checkForInput(pygame.mouse.get_pos()): #počisti varijable i makne graf
                    resetirano = 1
                    alfa = "Početni kut/ deg"
                    sy = "Početna visina/ m"
                    v = "Početna brzina/ m/s"
                if KUT_GUMB.checkForInput(pygame.mouse.get_pos()): #aktivacija gumba za upis kuta
                    alfa = ""
                    upiskuta=True
                    upisbrzine=False
                    upisvisine=False
                if BRZINA_GUMB.checkForInput(pygame.mouse.get_pos()): #aktivacija gumba za upis brzine
                    v = ""
                    upiskuta=False
                    upisbrzine=True
                    upisvisine=False
                if VISINA_GUMB.checkForInput(pygame.mouse.get_pos()): #aktivacija gumba za upis visine
                    sy = ""
                    upiskuta=False
                    upisbrzine=False
                    upisvisine=True
            if upiskuta == True: #upis kuta
                if event.type==pygame.KEYDOWN:
                    if event.key == pygame.K_PERIOD:
                        alfa+="."
                    if event.key == pygame.K_0:
                        alfa+="0"
                    if event.key == pygame.K_1:
                        alfa+="1"
                    if event.key == pygame.K_2:
                        alfa+="2"
                    if event.key == pygame.K_3:
                        alfa+="3"
                    if event.key == pygame.K_4:
                        alfa+="4"
                    if event.key == pygame.K_5:
                        alfa+="5"
                    if event.key == pygame.K_6:
                        alfa+="6"
                    if event.key == pygame.K_7:
                        alfa+="7"
                    if event.key == pygame.K_8:
                        alfa+="8"
                    if event.key == pygame.K_9:
                        alfa+="9"
                    if event.key == pygame.K_KP_ENTER:
                        upiskuta= False
                    if event.key == pygame.K_BACKSPACE:
                        alfa = alfa[:-1]
            if upisbrzine == True: #upis brzine
                if event.type==pygame.KEYDOWN:
                    if event.key == pygame.K_PERIOD:
                        v+="."
                    if event.key == pygame.K_0:
                        v+="0"
                    if event.key == pygame.K_1:
                        v+="1"
                    if event.key == pygame.K_2:
                        v+="2"
                    if event.key == pygame.K_3:
                        v+="3"
                    if event.key == pygame.K_4:
                        v+="4"
                    if event.key == pygame.K_5:
                        v+="5"
                    if event.key == pygame.K_6:
                        v+="6"
                    if event.key == pygame.K_7:
                        v+="7"
                    if event.key == pygame.K_8:
                        v+="8"
                    if event.key == pygame.K_9:
                        v+="9"
                    if event.key == pygame.K_ESCAPE:
                        upiskuta= False
                    if event.key == pygame.K_BACKSPACE:
                        v = v[:-1]
            if upisvisine == True: #upis visine
                if event.type==pygame.KEYDOWN:
                    if event.key == pygame.K_PERIOD:
                        sy+="."
                    if event.key == pygame.K_0:
                        sy+="0"
                    if event.key == pygame.K_1:
                        sy+="1"
                    if event.key == pygame.K_2:
                        sy+="2"
                    if event.key == pygame.K_3:
                        sy+="3"
                    if event.key == pygame.K_4:
                        sy+="4"
                    if event.key == pygame.K_5:
                        sy+="5"
                    if event.key == pygame.K_6:
                        sy+="6"
                    if event.key == pygame.K_7:
                        sy+="7"
                    if event.key == pygame.K_8:
                        sy+="8"
                    if event.key == pygame.K_9:
                        sy+="9"
                    if event.key == pygame.K_ESCAPE:
                        upisvisine= False
                    if event.key == pygame.K_BACKSPACE:
                        sy = sy[:-1]
        try:
            if resetirano == 0:
                screen.blit(GRAF,[100,100]) #zalijepi sliku grafa nastalu simulacijom ako je ima
                text = font.render("domet je: "+str(sx)+" metara, maksimalna visina je: "+str(ymax)+" metara, duljina leta je: "+str(t)+" sekundi",True,BLACK)
                textRect = text.get_rect()
                textRect.center = (1000,100)
                screen.blit(text, textRect)
            else:
                pass
        except:
            pass
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__": #pokreće funkciju
    main()