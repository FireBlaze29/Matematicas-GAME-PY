import pygame as pg
import pygame_widgets as pgw
from pygame_widgets.button import Button
import sys
from game import Game
from settings import ANCHO, ALTO, TILE_SIZE, FPS

class VentInicio:
    def __init__(self):
        pg.init()

        self.ancho, self.alto = ANCHO, ALTO
        self.IndexAncho, self.IndexAlto = self.ancho/ANCHO, self.alto/ALTO
        self.tile_size = TILE_SIZE * self.IndexAlto

        self.screen = pg.display.set_mode((self.ancho, self.alto), pg.RESIZABLE)
        self.clock = pg.time.Clock()
        self.running = True
        
        self.Recharge()

    def Recharge(self):
        self.boton_continuar = Button(
            self.screen,
            self.ancho/2 - (ANCHO/4 * self.IndexAncho),
            self.alto - ((ALTO/6-5)*3 * self.IndexAlto),
            (ANCHO/2+10) * self.IndexAncho,
            (ALTO/10+3) * self.IndexAlto,
            text='Continuar',
            onClick=self.launch_game,
            fontSize=int((int(ALTO/100)*10) * self.IndexAlto),
            radius=20,
            color=(0, 200, 0),
            hoverColor=(0, 255, 0),
            textColor=(255, 255, 255)
        )
        self.boton_mapa = Button(
            self.screen,
            self.ancho/2 - (ANCHO/4 * self.IndexAncho),
            self.alto - ((ALTO/6-5)*2 * self.IndexAlto),
            (ANCHO/2+10) * self.IndexAncho,
            (ALTO/10+3) * self.IndexAlto,
            text='Mapa',
            onClick=lambda: print('Botón Mapa presionado'),
            fontSize=int((int(ALTO/100)*10) * self.IndexAlto),
            radius=20,
            color=(0, 200, 0),
            hoverColor=(0, 255, 0),
            textColor=(255, 255, 255)
        )
        self.boton_config = Button(
            self.screen,
            self.ancho/2 - (ANCHO/4 * self.IndexAncho),
            self.alto - ((ALTO/6-5) * self.IndexAlto),
            (ANCHO/2+10) * self.IndexAncho,
            (ALTO/10+3) * self.IndexAlto,
            text='Configuraciones',
            onClick=lambda: print('Botón Config presionado'),
            fontSize=int((int(ALTO/100)*10) * self.IndexAlto),
            radius=20,
            color=(0, 200, 0),
            hoverColor=(0, 255, 0),
            textColor=(255, 255, 255)
        )

    def launch_game(self):
        self.running = False

    def update(self):
        pg.display.flip()
        self.clock.tick(FPS)
        pg.display.set_caption(f"Ventana de Inicio - FPS: {self.clock.get_fps():.1f}")

    def draw(self):
        self.screen.fill('black')
        self.boton_continuar.draw()
        self.boton_mapa.draw()
        self.boton_config.draw()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.VIDEORESIZE:
                self.ancho, self.alto = event.w, event.h
                self.screen = pg.display.set_mode((self.ancho, self.alto), pg.RESIZABLE)
                self.IndexAncho, self.IndexAlto = self.ancho/ANCHO, self.alto/ALTO
                self.Recharge()
            # Actualiza widgets
            pgw.update(event)

    def run(self):
        while self.running:
            self.check_events()
            self.draw()
            self.update()
        pg.display.quit()

if __name__ == "__main__":
    while True:
        vent = VentInicio()
        vent.run()
        game = Game()
        game.run()