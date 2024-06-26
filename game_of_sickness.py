#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 22:32:00 2024

@author: franciszekkilarski
"""

import pygame
import numpy as np
import matplotlib.pyplot as plt
import pygame_gui
import time
from enum import Enum
from dataclasses import dataclass

# Constants
CELL_SIZE = 10
GRID_WIDTH, GRID_HEIGHT = 80, 60
SCREEN_WIDTH, SCREEN_HEIGHT = GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class CellState(Enum):
    EMPTY = 0
    ALIVE = 1
    INFECTED = 2
    RECOVERED = 3
    DEAD = 4

@dataclass
class Cell:
    x: int
    y: int
    state: CellState = CellState.EMPTY

    def draw(self, screen):
        color = {
            CellState.EMPTY: BLACK,
            CellState.ALIVE: WHITE,
            CellState.INFECTED: RED,
            CellState.RECOVERED: GREEN,
            CellState.DEAD: BLACK
        }[self.state]
        pygame.draw.rect(screen, color, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

class GameOfLife:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

        self._initialize_parameters()
        self._create_ui()
        self.reset_game()

    def _initialize_parameters(self):
        self.infectiousness = 0.3
        self.recovery_chance = 0.1
        self.mortality_rate = 0.05
        self.birth_chance = 0.2
        self.mutation_rate = 0.1
        self.paused = False
        self.waves_mode = False
        self.vaccine_mode = False
        self.total_deaths = 0
        self.infected_count = []
        self.recovered_count = []
        self.death_count = []

    def _create_ui(self):
        self.infectiousness_slider = self._create_slider("Infectiousness", 10, self.infectiousness)
        self.recovery_chance_slider = self._create_slider("Recovery Chance", 60, self.recovery_chance)
        self.mortality_rate_slider = self._create_slider("Mortality Rate", 110, self.mortality_rate)
        self.birth_chance_slider = self._create_slider("Birth Chance", 160, self.birth_chance)
        self.mutation_rate_slider = self._create_slider("Mutation Rate", 210, self.mutation_rate)

        self.restart_button = self._create_button("Restart", (10, 260))
        self.stop_button = self._create_button("Stop", (120, 260))
        self.waves_button = self._create_button("Fale zakażeń", (10, 300))
        self.vaccine_button = self._create_button("Szczepionka", (120, 300))

    def _create_slider(self, name, y, start_value):
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, y), (200, 20)),
            text=name,
            manager=self.manager
        )
        return pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, y + 20), (200, 20)),
            start_value=start_value,
            value_range=(0.0, 1.0),
            manager=self.manager
        )

    def _create_button(self, text, position):
        return pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(position, (100, 30)),
            text=text,
            manager=self.manager
        )

    def reset_game(self):
        self.grid = np.random.choice(
            [CellState.EMPTY, CellState.ALIVE, CellState.INFECTED],
            GRID_WIDTH * GRID_HEIGHT,
            p=[0.7, 0.25, 0.05]
        ).reshape(GRID_HEIGHT, GRID_WIDTH)
        self.cells = [[Cell(x, y, self.grid[y, x]) for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]
        self._initialize_parameters()

    def update(self):
        new_grid = np.copy(self.grid)
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                self._update_cell(x, y, new_grid)
        self.grid = new_grid
        self._update_cells()

    def _update_cell(self, x, y, new_grid):
        state = self.grid[y, x]
        if state == CellState.INFECTED:
            self._handle_infected_cell(x, y, new_grid)
        elif state == CellState.ALIVE:
            self._handle_alive_cell(x, y, new_grid)
        elif state == CellState.EMPTY:
            self._handle_empty_cell(x, y, new_grid)

    def _handle_infected_cell(self, x, y, new_grid):
        if np.random.rand() < self.recovery_chance:
            new_grid[y, x] = CellState.RECOVERED
        elif np.random.rand() < self.mortality_rate:
            new_grid[y, x] = CellState.EMPTY
            self.total_deaths += 1
        else:
            self._spread_infection(x, y, new_grid)

    def _spread_infection(self, x, y, new_grid):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                nx, ny = x + i, y + j
                if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                    neighbor_state = self.grid[ny, nx]
                    if neighbor_state == CellState.ALIVE and np.random.rand() < self.infectiousness:
                        new_grid[ny, nx] = CellState.INFECTED
                    elif neighbor_state == CellState.RECOVERED and np.random.rand() < self.mutation_rate:
                        new_grid[ny, nx] = CellState.INFECTED

    def _handle_alive_cell(self, x, y, new_grid):
        alive_neighbors = self._count_alive_neighbors(x, y)
        if alive_neighbors < 2 or alive_neighbors > 3:
            new_grid[y, x] = CellState.EMPTY
        elif alive_neighbors == 2:
            self._handle_birth(x, y, new_grid)

    def _handle_empty_cell(self, x, y, new_grid):
        if self._count_alive_neighbors(x, y) == 3:
            new_grid[y, x] = CellState.ALIVE

    def _count_alive_neighbors(self, x, y):
        return sum(
            self.grid[ny, nx] in [CellState.ALIVE, CellState.INFECTED, CellState.RECOVERED]
            for i in range(-1, 2)
            for j in range(-1, 2)
            if (i != 0 or j != 0) and 0 <= (nx := x + i) < GRID_WIDTH and 0 <= (ny := y + j) < GRID_HEIGHT
        )

    def _handle_birth(self, x, y, new_grid):
        neighbors = [
            self.grid[y + i, x + j]
            for i in range(-1, 2)
            for j in range(-1, 2)
            if (i != 0 or j != 0) and 0 <= x + j < GRID_WIDTH and 0 <= y + i < GRID_HEIGHT
        ]
        if len(neighbors) == 2 and np.random.rand() < self.birth_chance:
            if CellState.RECOVERED in neighbors:
                new_grid[y, x] = CellState.RECOVERED
            elif CellState.INFECTED in neighbors:
                new_grid[y, x] = CellState.INFECTED
            else:
                new_grid[y, x] = CellState.ALIVE

    def _update_cells(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                self.cells[y][x].state = self.grid[y, x]

    def run(self):
        running = True
        last_wave_change = time.time()
        while running:
            time_delta = self.clock.tick(10) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.manager.process_events(event)
                self._handle_button_events(event)

            if not self.paused:
                last_wave_change = self._handle_game_modes(last_wave_change)
                self._update_parameters()
                self.update()
                self._draw()
                self._update_statistics()
                self._plot_statistics()

            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)
            pygame.display.flip()

        pygame.quit()

    def _handle_button_events(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.restart_button:
                self.reset_game()
            elif event.ui_element == self.stop_button:
                self.paused = True
                self._save_plot()
            elif event.ui_element == self.waves_button:
                self.waves_mode = True
                self.vaccine_mode = False
            elif event.ui_element == self.vaccine_button:
                self.vaccine_mode = True
                self.waves_mode = False

    def _handle_game_modes(self, last_wave_change):
        if self.waves_mode:
            last_wave_change = self._handle_waves_mode(last_wave_change)
        if self.vaccine_mode:
            self._handle_vaccine_mode()
        return last_wave_change

    def _handle_waves_mode(self, last_wave_change):
        current_time = time.time()
        if current_time - last_wave_change > 5:
            if self.mutation_rate < 0.2:
                self.mutation_rate += 0.1
                self.recovery_chance = max(self.recovery_chance - 0.05, 0.05)
            else:
                self.mutation_rate -= 0.1
                self.recovery_chance = min(self.recovery_chance + 0.05, 0.3)
            self._update_slider_values()
            return current_time
        return last_wave_change

    def _handle_vaccine_mode(self):
        self.recovery_chance = min(self.recovery_chance + 0.005, 1.0)
        self._update_slider_values()

    def _update_slider_values(self):
        self.mutation_rate_slider.set_current_value(self.mutation_rate)
        self.recovery_chance_slider.set_current_value(self.recovery_chance)

    def _update_parameters(self):
        self.infectiousness = self.infectiousness_slider.get_current_value()
        self.recovery_chance = self.recovery_chance_slider.get_current_value()
        self.mortality_rate = self.mortality_rate_slider.get_current_value()
        self.birth_chance = self.birth_chance_slider.get_current_value()
        self.mutation_rate = self.mutation_rate_slider.get_current_value()

    def _draw(self):
        self.screen.fill(BLACK)
        for row in self.cells:
            for cell in row:
                cell.draw(self.screen)

    def _update_statistics(self):
        infected = sum(cell.state == CellState.INFECTED for row in self.cells for cell in row)
        recovered = sum(cell.state == CellState.RECOVERED for row in self.cells for cell in row)
        self.infected_count.append(infected)
        self.recovered_count.append(recovered)
        self.death_count.append(self.total_deaths)

    def _plot_statistics(self):
        plt.clf()
        plt.plot(self.infected_count, label='Infected', color='red')
        plt.plot(self.recovered_count, label='Recovered', color='green')
        plt.plot(self.death_count, label='Deaths', color='gray')
        plt.yscale('log')
        plt.legend()
        plt.pause(0.01)

    def _save_plot(self):
        plt.clf()
        plt.plot(self.infected_count, label='Infected', color='red')
        plt.plot(self.recovered_count, label='Recovered', color='green')
        plt.plot(self.death_count, label='Deaths', color='gray')
        plt.xlabel('Time')
        plt.ylabel('Count')
        plt.yscale('log')
        plt.title(f'Infectiousness: {self.infectiousness:.2f}, Recovery Chance: {self.recovery_chance:.2f}, '
                  f'Mortality Rate: {self.mortality_rate:.2f}, Birth Chance: {self.birth_chance:.2f}, '
                  f'Mutation Rate: {self.mutation_rate:.2f}')
        plt.legend()
        plt.savefig('infection_wave_plot.png')
        print("Wykres zapisany jako infection_wave_plot.png")

if __name__ == "__main__":
    game = GameOfLife()
    game.run()
