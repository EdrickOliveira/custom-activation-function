import asyncio
import sys

import pygame
from pygame.locals import K_ESCAPE, K_SPACE, K_UP, KEYDOWN, QUIT

from .entities import (
    Background,
    Floor,
    GameOver,
    Pipes,
    Player,
    PlayerMode,
    Score,
    WelcomeMessage,
)
from .utils import GameConfig, Images, Sounds, Window
from .neuralNetwork.neuralNetwork import *


class Flappy:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Flappy Bird")
        window = Window(288, 512)
        screen = pygame.display.set_mode((window.width, window.height))
        images = Images()

        self.config = GameConfig(
            screen=screen,
            clock=pygame.time.Clock(),
            fps=30,
            window=window,
            images=images,
            sounds=Sounds(),
        )

    async def start(self):
        while True:
            self.background = Background(self.config)
            self.floor = Floor(self.config)

            # generate multiple players
            self.player = []
            for _ in range(1000):
                self.player.append(Player(self.config))

            self.welcome_message = WelcomeMessage(self.config)
            self.game_over_message = GameOver(self.config)
            self.pipes = Pipes(self.config)
            self.score = Score(self.config)
            await self.splash()
            await self.play()
            await self.game_over()

    async def splash(self):
        """Shows welcome splash screen animation of flappy bird"""
        for bird in self.player:
            bird.set_mode(PlayerMode.SHM)

        while True:
            for event in pygame.event.get():
                self.check_quit_event(event)
                if self.is_tap_event(event):
                    return

            self.background.tick()
            self.floor.tick()
            for bird in self.player:
                bird.tick()
            self.welcome_message.tick()

            pygame.display.update()
            await asyncio.sleep(0)
            self.config.tick()

    def check_quit_event(self, event):
        if event.type == QUIT or (
            event.type == KEYDOWN and event.key == K_ESCAPE
        ):
            pygame.quit()
            sys.exit()

    def is_tap_event(self, event):
        m_left, _, _ = pygame.mouse.get_pressed()
        space_or_up = event.type == KEYDOWN and (
            event.key == K_SPACE or event.key == K_UP
        )
        screen_tap = event.type == pygame.FINGERDOWN
        return m_left or space_or_up or screen_tap

    async def play(self):
        self.score.reset()
        for bird in self.player:
            bird.set_mode(PlayerMode.NORMAL)

        alive = [True for _ in self.player]
        while any(alive):
            for idx, bird in enumerate(self.player):
                if not alive[idx]:
                    continue
                xDistance, yDistance = self.pipes.getNextPipeDistances(bird.x, bird.cy)
                bird.brain.getInputs(xDistance, yDistance)
                bird.brain.feedForward()
                # Optionally print output for each player
                #print(f"Player {idx} Output value: ", bird.brain.outputNeuron[0].value)

                if bird.collided(self.pipes, self.floor):
                    alive[idx] = False
                    continue

                for pipe in self.pipes.upper:
                    if bird.crossed(pipe):
                        bird.score += 1  # increment bird's individual score when it passes a pipe
                        self.score.set(bird.score)  # update displayed score to the highest score among alive birds

                if bird.brain.flap():
                    bird.flap()    # execute the brain's decision to flap

            for event in pygame.event.get():
                self.check_quit_event(event)
                if self.is_tap_event(event):
                    for idx, bird in enumerate(self.player):
                        if alive[idx]:
                            bird.flap()

            self.background.tick()
            self.floor.tick()
            self.pipes.tick()
            self.score.tick()
            for bird in self.player:
                bird.tick()

            pygame.display.update()
            await asyncio.sleep(0)
            self.config.tick()

    async def game_over(self):
        """crashes all players down and shows gameover image"""
        for bird in self.player:
            bird.set_mode(PlayerMode.CRASH)
        self.pipes.stop()
        self.floor.stop()

        while True:
            for event in pygame.event.get():
                self.check_quit_event(event)
                if self.is_tap_event(event):
                    # Only allow restart if all players are on the ground
                    if all(bird.y + bird.h >= self.floor.y - 1 for bird in self.player):
                        return

            self.background.tick()
            self.floor.tick()
            self.pipes.tick()
            self.score.tick()
            for bird in self.player:
                bird.tick()
            self.game_over_message.tick()

            self.config.tick()
            pygame.display.update()
            await asyncio.sleep(0)
