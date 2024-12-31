import pygame
import os
import random
import neat
import time
import csv
import sys

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
generation = 0
sim_fin = False

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

    def update(self, userInput):  # Actualització de l'estat del Dino segons la tecla premuda
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
            self.update(userInput=None) # Les IA controlen el personatge
    
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
    
    def ai_update(self, action): # Li donem el control del Dino a la IA
        if action == "jump" and not self.dino_jump:     # Salta
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif action == "duck" and not self.dino_jump:   # S'ajup
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not self.dino_jump:    # Corrent per defecte
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False
        self.update(userInput=None)  # Les IA controlen el personatge

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
    def __init__(self, image, type, name):  # Constructor inicialitzador
        self.image = image
        self.type = type  # Tipus d'obstacle
        self.rect = self.image[self.type].get_rect()  # Caixa de col·lisions segons la imatge
        self.rect.x = SCREEN_WIDTH  # Comença fora de la pantalla
        self.name = name

    def update(self):  # Moviment de l'obstacle
        self.rect.x -= game_speed  # Es mou cap a l'esquerra segons la velocitat del joc
        if self.rect.x < -self.rect.width:  # Si surt de la pantalla
            del obstacles[0]  # S'elimina de la llista d'obstacles

    def draw(self, SCREEN):  # Dibuixa l'obstacle
        SCREEN.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):  # Cactus petits
    def __init__(self, image):
        self.name = "SmallCactus"
        self.type = random.randint(0, 2)  # Tria una imatge aleatòria de tres possibles
        super().__init__(image, self.type, self.name)  # Inicialitza l'obstacle
        self.rect.y = DINO_SPAWN_Y + 15  # Posició Y dels cactus petits

class LargeCactus(Obstacle):  # Cactus grans
    def __init__(self, image):
        self.name = "LargeCactus"
        self.type = random.randint(0, 2)  # Tria una imatge aleatòria de tres possibles
        super().__init__(image, self.type, self.name)  # Inicialitza l'obstacle
        self.rect.y = DINO_SPAWN_Y - 10  # Posició Y dels cactus grans

class HighBird(Obstacle):  # Ocells alts
    def __init__(self, image):
        self.type = 0
        self.name = "HighBird"
        super().__init__(image, self.type, self.name)  # Inicialitza l'obstacle
        self.rect.y = DINO_SPAWN_Y + 10 # Posició Y de l'ocell alt
        self.index = 0  # Comptador per animació de les ales  

    def draw(self, SCREEN):  # Dibuix amb animació
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)  # Alterna entre imatges 
        self.index += 1

class LowBird(Obstacle):  # Ocells baixos
    def __init__(self, image):
        self.name = "LowBird"
        self.type = 0
        super().__init__(image, self.type, self.name)  # Inicialitza l'obstacle
        self.rect.y = DINO_SPAWN_Y + 18  # Posició Y de l'ocell baix
        self.index = 0  # Comptador per animació de les ales

    def draw(self, SCREEN):  # Dibuix amb animació
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)  # Alterna imatges
        self.index += 1


def eval_genomes(genomes, config):  
    # Variables globals per gestionar la velocitat del joc, la puntuació, obstacles
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, generation

    # Variables per gestioanr els genomes i les generacions
    generation += 1  # Incrementar el comptador de generació
    nets = []  # Llista per guardar les xarxes neuronals dels genomes
    dinos = []  # Llista per guardar els dinosaures associats als genomes
    ge = []  # Llista per guardar els genomes amb què es treballa

    # Inicialitzar cada genoma, xarxa i dinosaure
    for genome_id, genome in genomes:
        genome.fitness = 0  # Configurar el "fitness" inicial del genoma, que és 0<
        net = neat.nn.FeedForwardNetwork.create(genome, config)  # Crear la xarxa neuronal per al genoma
        nets.append(net)  # Afegir la xarxa neuronal a la llista
        dinos.append(Dinosaur())  # Crear un dinosaure per cada genoma
        ge.append(genome)  # Afegir el genoma a la llista

    clock = pygame.time.Clock()  # Configurar el rellotge del joc
    cloud = Cloud()  # Crear un núvol inicial
    game_speed = 14  # Configurar la velocitat inicial del joc
    x_pos_bg = 0  # Posició inicial del fons en X
    y_pos_bg = DINO_SPAWN_Y + 70  # Posició inicial del fons en Y
    points = 0  # Inicialitzar la puntuació
    font = pygame.font.Font('freesansbold.ttf', 20)  # Configurar la font per mostrar informació
    obstacles = []  # Llista inicial d'obstacles
    obstacle_timer = 0  # Temporitzador per generar obstacles
    start_time = time.time()  # Guardar el temps d'inici de la simulació

    # Funció per calcular la puntuació
    def score():
        global points, game_speed
        points += 1  # Increment de la puntuació
        if points % 100 == 0:  # Augmentar la velocitat del joc cada 100 punts
            game_speed += 1
        # Mostrar la puntuació en pantalla
        text = font.render("Puntuació: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (600, 40)
        SCREEN.blit(text, textRect)
        return points

    # Funció per actualitzar el fons del joc
    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        # Dibuixar dues imatges del fons una al costat de l'altra
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:  # Si una imatge surt de la pantalla, reiniciar
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed  # Mou el fons cap a l'esquerra segons la velocitat del joc

    # Funció per generar obstacles aleatoris
    def obstacle_print():
        number = random.randint(1, 11)  # Escollir un obstacle aleatori
        if number <= 5:
            obstacles.append(SmallCactus(SMALL_CACTUS))  # Afegir un cactus petit
            is_high_bird = 0
        elif number <= 8:
            obstacles.append(LargeCactus(LARGE_CACTUS))  # Afegir un cactus gran
            is_high_bird = 0
        elif number <= 10:
            # Afegir un ocell alt o baix aleatòriament
            if random.randint(1, 2) == 1:
                obstacles.append(HighBird(BIRD))
                is_high_bird = 1
            else:
                obstacles.append(LowBird(BIRD))
                is_high_bird = 0

    # Funció per mostrar informació de la generació
    def draw_generation_info():
        elapsed_time = time.time() - start_time  # Calcular el temps transcorregut
        info_text = [
            f"Generació: {generation}",  # Generació actual
            f"Dinos vius: {len(dinos)}",  # Nombre de dinosaures vius
            f"Temps: {int(elapsed_time)}s"  # Temps transcorregut en segons
        ]
        # Mostrar la informació línia per línia
        for i, text in enumerate(info_text):
            text_surface = font.render(text, True, (0, 0, 0))
            SCREEN.blit(text_surface, (10, 10 + i * 20))

    run = True
    while run and len(dinos) > 0:  # Mentre el joc estigui en marxa i quedin dinos vius
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Si es tanca la finestra, sortir del programa
                run = False
                pygame.quit()
                quit()

        SCREEN.fill((255, 255, 255))  # Esborrar la pantalla amb color blanc

        if len(obstacles) == 0 or obstacle_timer >= 50:  # Generar obstacles si no n'hi ha o ha passat un temps
            obstacle_print()
            obstacle_timer = 0

        # Actualitzar i dibuixar obstacles
        for obstacle in obstacles[:]:
            obstacle.draw(SCREEN)
            obstacle.update()
            if obstacle.rect.x < -obstacle.rect.width:  # Eliminar obstacles que han sortit de la pantalla
                if obstacle in obstacles:
                    obstacles.remove(obstacle)

        # Actualitzar i gestionar cada dinosaure
        for i, dino in enumerate(dinos):
            if len(obstacles) > 0:  # Quan hi ha obstacles, calcular les distàncies
                obstacle_x_dist = obstacles[0].rect.x - dino.dino_rect.x
                obstacle_y_dist = obstacles[0].rect.y - dino.dino_rect.x
            else:  # Si no hi ha obstacles, la distància es la pantalla sencera
                obstacle_x_dist = SCREEN_WIDTH
                obstacle_y_dist = SCREEN_HEIGHT

            # Activar la xarxa neuronal per decidir l'acció
            output = nets[i].activate((dino.dino_rect.y, obstacle_x_dist, obstacle_y_dist, dino.dino_rect.x))

            if output[0] > 0.5:  # Saltar
                if len(obstacles) > 0: #
                    dino.ai_update("jump")
            elif output[1] > 0.5:  # Ajupir-se
                dino.ai_update("duck")
            else:  # Còrrer
                dino.ai_update("run")

            # Comprovar col·lisions amb obstacles
            if len(obstacles) > 0 and dino.dino_rect.colliderect(obstacles[0].rect):
                ge[i].fitness -= 1  # Penalitzar el genoma si el dino col·lisiona
                dinos.pop(i)  # Eliminar el dinosaure
                nets.pop(i)  # Eliminar la xarxa neuronal
                ge.pop(i)  # Eliminar el genoma

        for genome in ge:
            genome.fitness += 0.1  # Es recompensa als genomes vius

        if score() >= 2500:  # Si s'aconsegueix la puntuació desitjada, finalitzar la simulació
            sim_fin = True
            break;
            run = False
            elapsed_time = time.time() - start_time    

        # Dibuixar i actualitzar elements visuals
        background()
        draw_generation_info()
        cloud.draw(SCREEN)
        cloud.update()

        for dino in dinos:
            dino.draw(SCREEN)

        obstacle_timer += 1  # Incrementar el temporitzador d'obstacles
        clock.tick(30)  # Fijar la velocitat de frames a 30 FPS
        pygame.display.update()

# Funció principal per executar NEAT
def run_neat(config_file):
    # Configurar NEAT amb el fitxer dels paràmetres
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    p = neat.Population(config)  # Crear una població inicial
    p.add_reporter(neat.StdOutReporter(True))  # Afegir un reporter per mostrar informació
    stats = neat.StatisticsReporter()  # Afegir un reporter d'estadístiques
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 50)  # Executar NEAT durant 50 generacions o fins trobar un guanyador
    print('\nBest genome:\n{!s}'.format(winner))  # Mostrar el millor genoma


if not sim_fin:
    if __name__ == "__main__":  
        # Aquest bloc s'executa només si el fitxer és executat directament,
        # no si és importat com a mòdul.
        
        local_dir = os.path.dirname(__file__)  
        # Obté el directori del fitxer actual per garantir que els camins siguin correctes, 
        # independentment d'on s'executi el codi.

        config_path = os.path.join(local_dir, 'config-feedforward.txt')  
        # Construeix el camí complet al fitxer de configuració 'config-feedforward.txt'
        # dins del mateix directori que aquest "script".

        run_neat(config_path)  
        # Crida a la funció principal `run_neat`, passant-li el camí al fitxer de configuració.
