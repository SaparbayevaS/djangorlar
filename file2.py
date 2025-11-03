#!/usr/bin/env python3
"""
Conway's Game of Life в терминале.
Запуск: python3 game_of_life.py
Нажмите Ctrl-C для остановки.
"""
import random
import time
import os
import sys
from typing import List

WIDTH = 40
HEIGHT = 20
ALIVE = "+"
DEAD = " "

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        sys.stdout.write("\033[H\033[J")

def make_grid(randomize=True) -> List[List[int]]:
    grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    if randomize:
        for y in range(HEIGHT):
            for x in range(WIDTH):
                grid[y][x] = 1 if random.random() < 0.25 else 0
    return grid

def neighbors(grid, x, y) -> int:
    s = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                s += grid[ny][nx]
    return s

def step(grid):
    new = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for y in range(HEIGHT):
        for x in range(WIDTH):
            n = neighbors(grid, x, y)
            if grid[y][x] == 1:
                new[y][x] = 1 if n in (2, 3) else 0
            else:
                new[y][x] = 1 if n == 3 else 0
    return new

def render(grid, generation):
    lines = [f"Generation: {generation} — Ctrl-C to stop"]
    for row in grid:
        lines.append("".join(ALIVE if c else DEAD for c in row))
    print("\n".join(lines))

def main():
    grid = make_grid(randomize=True)
    generation = 0
    try:
        while True:
            clear()
            render(grid, generation)
            grid = step(grid)
            generation += 1
            time.sleep(0.18)
    except KeyboardInterrupt:
        print("\n[ver4] game over")

if __name__ == "__main__":
    main()