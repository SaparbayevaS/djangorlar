#!/usr/bin/env python3
"""
Генетический алгоритм, пытающийся эволюционировать строку до целевой фразы.
Выводит прогресс в консоль.
"""
import random
import string
import math
import time
from typing import List, Tuple


TARGET = "version four testing"

POP_SIZE = 200
MUTATION_RATE = 0.03
TOURNAMENT_SIZE = 5
MAX_GENERATIONS = 2000

CHARS = string.ascii_lowercase + " "  # только строчные + пробел

def random_individual(length: int) -> str:
    return "".join(random.choice(CHARS) for _ in range(length))

def fitness(individual: str, target: str) -> int:
    # чем меньше расстояние, тем лучше (0 — идеально)
    # используем сумму абсолютных разниц по символам
    score = 0
    for a, b in zip(individual, target):
        score += abs(ord(a) - ord(b))
    return score

def mutate(ind: str, rate: float) -> str:
    chars = list(ind)
    for i in range(len(chars)):
        if random.random() < rate:
            chars[i] = random.choice(CHARS)
    return "".join(chars)

def crossover(a: str, b: str) -> str:
    # одноточечный кроссовер
    p = random.randint(1, len(a) - 1)
    return a[:p] + b[p:]

def tournament_select(pop: List[str], target: str) -> str:
    best = None
    for _ in range(TOURNAMENT_SIZE):
        cand = random.choice(pop)
        if best is None or fitness(cand, target) < fitness(best, target):
            best = cand
    return best

def evolve():
    length = len(TARGET)
    # инициализация
    population = [random_individual(length) for _ in range(POP_SIZE)]
    best = min(population, key=lambda ind: fitness(ind, TARGET))
    best_score = fitness(best, TARGET)
    generation = 0
    start = time.time()

    while generation < MAX_GENERATIONS and best_score != 0:
        new_pop = []
        for _ in range(POP_SIZE):
            parent1 = tournament_select(population, TARGET)
            parent2 = tournament_select(population, TARGET)
            child = crossover(parent1, parent2)
            child = mutate(child, MUTATION_RATE)
            new_pop.append(child)
        population = new_pop
        current_best = min(population, key=lambda ind: fitness(ind, TARGET))
        current_score = fitness(current_best, TARGET)
        if current_score < best_score:
            best, best_score = current_best, current_score
        if generation % 20 == 0 or generation < 50:
            elapsed = time.time() - start

            print(f"[v5] Generation {generation:4d} | Best result: '{best}' | Score is: {best_score} | Time is: {elapsed:.2f}s")

        generation += 1

    total_time = time.time() - start
    print("-" * 60)
    print(f"Finished in {generation} generations, time {total_time:.2f}s")
    print(f"Best result: '{best}' with score {best_score}")
    if best_score == 0:
        print("Target reached!")

if __name__ == "__main__":
    evolve()