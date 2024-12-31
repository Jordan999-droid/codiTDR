import pygame
import os
import random

pygame.init()
pygame.font.init()

# Variables universals del programa
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1150     
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DINO_SPAWN_Y = 350
DINO_SPAWN_X = 60
distancia_x = 0
distancia_y = 0 

# Definició de les imatges a fer-se servir durant l'execució del joc
RUNNING = [pygame.image.load(os.path.join("Assets\Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets\Dino", "DinoRun2.png"))]
DUCKING = [pygame.image.load(os.path.join("Assets\Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets\Dino", "DinoDuck2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets\Dino", "DinoJump.png"))
SMALL_CACTUS = [pygame.image.load(os.path.join("Assets\Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets\Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets\Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets\Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets\Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets\Cactus", "LargeCactus3.png"))]
BIRD = [pygame.image.load(os.path.join("Assets\Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets\Bird", "Bird2.png"))]
CLOUD = pygame.image.load(os.path.join("Assets\Altres", "Cloud.png"))
BG = pygame.image.load(os.path.join("Assets\Altres", "Track.png"))

class Dinosaur:  # Classe que defineix el comportament del dinosaure
    X_POS = DINO_SPAWN_X  # Posició inicial a l'eix X
    Y_POS = DINO_SPAWN_Y  # Posició inicial a l'eix Y
    Y_POS_DUCKING = Y_POS + 30  # Posició del Dino quan s'ajup
    max_gravity = 8.5  # Gravetat màxima per al salt del Dino

    def __init__(self):  # Constructor inicialitzador
        self.duck_img = DUCKING  # Imatge del Dino quan s'ajup
        self.run_img = RUNNING  # Imatge del Dino quan corre
        self.jump_img = JUMPING  # Imatge del Dino quan salta

        self.dino_duck = False  # Estat inicial: no ajupit
        self.dino_run = True  # Estat inicial: corrent
        self.dino_jump = False  # Estat inicial: no saltant

        self.step_index = 0  # Comptador d'animacions
        self.gravity = self.max_gravity  # Gravetat inicial
        self.image = self.run_img[0]  # Imatge inicial
        self.dino_rect = self.image.get_rect()  # Caixa de col·lisió
        self.dino_rect.x = self.X_POS  # Posició X inicial
        self.dino_rect.y = self.Y_POS  # Posició Y inicial

    def update(self, userInput):  # Actualització de l'estat del Dino segons la tecla polsada
        if self.dino_duck:
            self.duck()  # Activa l'estat ajupit
        if self.dino_run:
            self.run()  # Activa l'estat corrent
        if self.dino_jump:
            self.jump()  # Activa l'estat saltant

        if self.step_index >= 10:
            self.step_index = 0  # Reseteja el comptador d'animacions

        # Tecles per a canviar l'estat del Dino
        if userInput:
            if (userInput[pygame.K_UP] or userInput[pygame.K_SPACE]) and not self.dino_jump:
                self.dino_duck = False
                self.dino_run = False
                self.dino_jump = True  # Comença el salt
            elif (userInput[pygame.K_DOWN] or userInput[pygame.K_s]) and not self.dino_jump:
                self.dino_duck = True
                self.dino_run = False
                self.dino_jump = False  # S'ajup
            elif not (self.dino_jump or userInput[pygame.K_DOWN]):
                self.dino_duck = False
                self.dino_run = True
                self.dino_jump = False  # Corrent per defecte

    def run(self):  # Comportament del Dino corrent
        self.image = self.run_img[self.step_index // 5]  # Animació segons el pas
        self.dino_rect = self.image.get_rect()  # Actualitza la caixa de col·lisió
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1  # Incrementa el comptador d'animacions

    def duck(self):  # Comportament del Dino ajupit
        self.image = self.duck_img[self.step_index // 5]  # Animació segons el pas
        self.dino_rect = self.image.get_rect()  # Actualitza la caixa de col·lisió
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCKING  # Posició ajupida
        self.step_index += 1  # Incrementa el comptador d'animacions

    def jump(self):  # Comportament del Dino saltant
        self.image = self.jump_img  # Imatge fixa mentre salta
        if self.dino_jump:
            self.dino_rect.y -= self.gravity * 4  # Moviment vertical segons la gravetat
            self.gravity -= 0.8  # Decreixement de la gravetat
        if self.gravity < -self.max_gravity:  # Quan arriba al límit del salt
            self.dino_jump = False  # Finalitza el salt
            self.gravity = self.max_gravity  # Reseteja la gravetat
            self.dino_rect.y = self.Y_POS  # Retorna a la posició inicial

    def draw(self, SCREEN):  # Dibuixa el Dino
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
        # Aplica la imatge corresponent a l'estat actual

class Cloud:  # Classe que defineix el comportament dels núvols decoratius
    def __init__(self):  # Constructor inicialitzador
        self.x = SCREEN_WIDTH + random.randint(800, 1000)  # Posició inicial X aleatòria fora de pantalla
        self.y = random.randint(50, 100)  # Posició inicial Y aleatòria a la part superior
        self.image = CLOUD  # Imatge del núvol
        self.width = self.image.get_width()  # Amplada del núvol

    def update(self):  # Actualitza la posició del núvol
        self.x -= game_speed  # Mou el núvol cap a l'esquerra segons la velocitat del joc
        if self.x < -self.width:  # Si surt de la pantalla
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)  # Reapareix amb nova posició
            self.y = random.randint(50, 100)  # Actualitza la posició Y aleatòria

    def draw(self, SCREEN):  # Dibuixa el núvol
        SCREEN.blit(self.image, (self.x, self.y))
        # Mostra el núvol a la pantalla

# Les classes dels obstacles
class Obstacle:  # Classe pare que defineix el comportament comú dels obstacles
    def __init__(self, image, type):  # Constructor inicialitzador
        self.image = image
        self.type = type  # Tipus d'obstacle
        self.rect = self.image[self.type].get_rect()  # Caixa de col·lisions segons la imatge
        self.rect.x = SCREEN_WIDTH  # Comença fora de la pantalla

    def update(self):  # Moviment de l'obstacle
        self.rect.x -= game_speed  # Es mou cap a l'esquerra segons la velocitat del joc
        if self.rect.x < -self.rect.width:  # Si surt de la pantalla
            del obstacles[0]  # S'elimina de la llista d'obstacles

    def draw(self, SCREEN):  # Dibuixa l'obstacle
        SCREEN.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):  # Cactus petits
    def __init__(self, image):
        self.type = random.randint(0, 2)  # Tria una imatge aleatòria de tres possibles
        super().__init__(image, self.type)  # Inicialitza l'obstacle
        self.rect.y = DINO_SPAWN_Y + 15  # Posició Y dels cactus petits

class LargeCactus(Obstacle):  # Cactus grans
    def __init__(self, image):
        self.type = random.randint(0, 2)  # Tria una imatge aleatòria de tres possibles
        super().__init__(image, self.type)  # Inicialitza l'obstacle
        self.rect.y = DINO_SPAWN_Y - 10  # Posició Y dels cactus grans

class HighBird(Obstacle):  # Ocells alts
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)  # Inicialitza l'obstacle
        self.rect.y = DINO_SPAWN_Y  + 10       # Posició Y de l'ocell alt
        self.index = 0  # Comptador per animació de les ales

    def draw(self, SCREEN):  # Dibuix amb animació
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)  # Alterna imatges
        self.index += 1

class LowBird(Obstacle):  # Ocells baixos
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)  # Inicialitza l'obstacle
        self.rect.y = DINO_SPAWN_Y + 18  # Posició Y de l'ocell baix
        self.index = 0  # Comptador per animació de les ales

    def draw(self, SCREEN):  # Dibuix amb animació
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)  # Alterna imatges
        self.index += 1


def game_loop():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, dead, score  # Variables globals utilitzades dins de la funció
    run = True  # Variable per controlar l'execució del bucle principal del joc
    clock = pygame.time.Clock()  # Per controlar la velocitat de refresc de la pantalla
    player = Dinosaur()  # Instància de la classe Dinosaur
    cloud = Cloud()  # Instància de la classe Cloud
    game_speed = 14  # Velocitat inicial del joc
    x_pos_bg = 0  # Posició inicial de l'eix X del fons
    y_pos_bg = DINO_SPAWN_Y + 70  # Posició inicial de l'eix Y del fons
    points = 0  # Puntuació inicial del joc
    font = pygame.font.Font('freesansbold.ttf', 20)  # Font per mostrar la puntuació
    obstacles = []  # Llista per emmagatzemar els obstacles generats al joc

    # Funció per actualitzar i mostrar la puntuació del jugador
    def score():
        global points, game_speed  # Definició de les variables globals que s'utilitzen
        points += 1  # Augmenta la puntuació en cada iteració
        if points % 100 == 0:  # Cada cop que la puntuació arriba a un múltiple de 100, s'incrementa la velocitat del joc
            game_speed += 1
        text = font.render("Puntuació: " + str(points), True, (0, 0, 0))  # Renderitza la puntuació com un text
        textRect = text.get_rect()  # Obté el rectangle on es dibuixarà el text
        textRect.center = (600, 40)  # Posiciona el text a la part superior central de la pantalla
        SCREEN.blit(text, textRect)  # Dibuixa el text de la puntuació a la pantalla

    # Funció per actualitzar i dibuixar el fons de la pantalla
    def Background():
        global x_pos_bg, y_pos_bg  # Variables globals per la posició del fons
        image_width = BG.get_width()  # Obtén l'amplada de la imatge de fons
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))  # Dibuixa la primera imatge del fons
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))  # Dibuixa la segona imatge per continuar el fons
        if x_pos_bg <= -image_width:  # Si el fons ha sortit completament de la pantalla
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))  # Dibuixa una nova imatge per a la transició
            x_pos_bg = 0  # Reinicia la posició del fons
        x_pos_bg -= game_speed  # Desplaça el fons cap a l'esquerra amb la velocitat del joc

    # Funció per generar obstacles aleatoris
    def ObstaclePrint():
        number = random.randint(1, 11)  # Genera un número aleatori per decidir quin tipus d'obstacle apareixerà
        if number <= 5 and number >= 1:  # Si el número està entre 1 i 5, genera un cactus petit: 50% probable
            obstacles.append(SmallCactus(SMALL_CACTUS))
        elif number <= 8 and number >= 6:  # Si el número està entre 6 i 8, genera un cactus gran: 30% probable
            obstacles.append(LargeCactus(LARGE_CACTUS))
        if number <= 10 and number >= 9:  # Si el número és 9 o 10, genera un ocell: 20% probable
            number = random.randint(1, 2)
            if number == 2:  # Genera un ocell alt
                obstacles.append(HighBird(BIRD))
            else:  # Genera un ocell baix
                obstacles.append(LowBird(BIRD))

    # Bucle principal del joc
    while run:
        for event in pygame.event.get():  # Detecció d'esdeveniments del joc per un tancament segur
            if event.type == pygame.QUIT:  # Si l'usuari tanca la finestra
                run = False  # Sortir del bucle
                pygame.quit()  # Tancar Pygame
                break  # Atura l'execució del bucle

        SCREEN.fill((255, 255, 255))  # Omple la pantalla de blanc per netejar-la cada iteració
        userInput = pygame.key.get_pressed()  # Obté l'estat actual de les tecles per actualitzar al Dino

        player.draw(SCREEN)  # Dibuixa el dinosaure
        player.update(userInput)  # Actualitza la posició i acció del dinosaure en funció de les tecles pressionades
            
        if len(obstacles) == 0:  # Si no hi ha obstacles en pantalla, crea'n un de nou
            ObstaclePrint()

        # Actualitza els obstacles i comprova les col·lisions
        for obstacle in obstacles:
            obstacle.draw(SCREEN)  # Dibuixa cada obstacle
            obstacle.update()  # Actualitza la posició de cada obstacle
            if player.dino_rect.colliderect(obstacle.rect):  # Si el dinosaure col·lideix amb un obstacle
                player.image = pygame.image.load(os.path.join("Assets\Dino", "DinoDead.png"))  # Mostra la imatge del dinosaure mort
                pygame.time.delay(2000)  # Espera 2 segons
                game_loop()  # Torna a començar el joc des de zero (reinicia la funció de joc)

        Background()  # Actualitza el fons
        score()  # Mostra la puntuació
        cloud.draw(SCREEN)  # Dibuixa els núvols
        cloud.update()  # Actualitza la posició dels núvols
        clock.tick(30)  # Controla el nombre de frames per segon
        pygame.display.update()  # Actualitza la pantalla amb les noves imatges

game_loop()  # Crida al bucle principal del joc per iniciar-lo