import pygame
from settings import (
    ALTURA,
    ANCHURA,
    BALDOSA_NUMERO,
    BALDOSA_TAMANIO,
    MARCADOR_ANCHURA,
    PUNTO_UNIDAD,
    RUTA_CABEZA,
    RUTA_SFX_COMIDA,
)
from .cuerpos import CUERPOS

# CLASE SERPIENTE
class SERPIENTE(pygame.sprite.Sprite):
    def __init__(self, lista_serpiente, lista_comida, lista_global):
        pygame.sprite.Sprite.__init__(self)

        self.lista_serpiente = lista_serpiente
        self.lista_comida = lista_comida
        self.lista_global = lista_global

        self.SONIDO_COMIDA = pygame.mixer.Sound(RUTA_SFX_COMIDA)
        self.SONIDO_COMIDA.set_volume(1.0)

        self.CABEZA = pygame.image.load(RUTA_CABEZA).convert_alpha()
        self.image = self.CABEZA

        self.rect = self.image.get_rect()
        self.rect.y = (BALDOSA_NUMERO / 2) * BALDOSA_TAMANIO
        self.rect.x = (BALDOSA_NUMERO / 2) * BALDOSA_TAMANIO

        self.PUNTOS = 0
        self.DIRECCION = 'I'
        self.TERMINA = False

    def AGREGAR_NUEVO_CUERPO(self):
        nuevo_cuerpo = CUERPOS(self.rect.x, self.rect.y)
        self.lista_serpiente.add(nuevo_cuerpo)
        self.lista_global.add(nuevo_cuerpo)

    def update(self):
        coord_actual_x = self.rect.x
        coord_actual_y = self.rect.y

        if self.DIRECCION == 'I':
            self.image = pygame.transform.rotate(self.CABEZA, 90)
            self.rect.x -= BALDOSA_TAMANIO
        elif self.DIRECCION == 'D':
            self.image = pygame.transform.rotate(self.CABEZA, -90)
            self.rect.x += BALDOSA_TAMANIO
        elif self.DIRECCION == 'A':
            self.image = pygame.transform.rotate(self.CABEZA, 0)
            self.rect.y -= BALDOSA_TAMANIO
        elif self.DIRECCION == 'B':
            self.image = pygame.transform.rotate(self.CABEZA, 180)
            self.rect.y += BALDOSA_TAMANIO

        for elt in self.lista_serpiente:
            x = elt.GET_X()
            y = elt.GET_Y()
            elt.set_xy(coord_actual_x, coord_actual_y)
            coord_actual_x = x
            coord_actual_y = y

        if self.rect.x >= ALTURA:
            self.rect.x = 0
        elif self.rect.x < 0:
            self.rect.x = ALTURA - BALDOSA_TAMANIO
        elif self.rect.y >= ANCHURA:
            self.rect.y = MARCADOR_ANCHURA
        elif self.rect.y < MARCADOR_ANCHURA:
            self.rect.y = ANCHURA - MARCADOR_ANCHURA

        lista_colision_serpiente = pygame.sprite.spritecollide(self, self.lista_serpiente, False)
        if len(lista_colision_serpiente):
            print("Perdido")
            self.TERMINA = True

        lista_colision_comida = pygame.sprite.spritecollide(self, self.lista_comida, False)
        for comida in lista_colision_comida:
            comida.kill()
            self.AGREGAR_NUEVO_CUERPO()
            self.SONIDO_COMIDA.play()
            self.PUNTOS += PUNTO_UNIDAD