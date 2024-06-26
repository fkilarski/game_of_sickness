#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 22:32:00 2024

@author: franciszekkilarski
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class CellularAutomaton:
    def __init__(self, szerokosc, wysokosc, prawdopodobienstwo_zakazenia, prawdopodobienstwo_ozdrowienia, smiertelnosc):
        self.szerokosc = szerokosc
        self.wysokosc = wysokosc
        self.prawdopodobienstwo_zakazenia = prawdopodobienstwo_zakazenia
        self.prawdopodobienstwo_ozdrowienia = prawdopodobienstwo_ozdrowienia
        self.smiertelnosc = smiertelnosc
        self.siatka = np.random.choice([0, 1], size=(szerokosc, wysokosc), p=[0.95, 0.05])
    
    def step(self):
        nowa_siatka = self.siatka.copy()
        for x in range(self.szerokosc):
            for y in range(self.wysokosc):
                if self.siatka[x, y] == 0:  # Zdrowa komórka
                    sasiedzi = self.siatka[max(0, x-1):min(self.szerokosc, x+2), max(0, y-1):min(self.wysokosc, y+2)]
                    if 1 in sasiedzi:
                        if np.random.rand() < self.prawdopodobienstwo_zakazenia:
                            nowa_siatka[x, y] = 1
                elif self.siatka[x, y] == 1:  # Zakażona komórka
                    if np.random.rand() < self.smiertelnosc:
                        nowa_siatka[x, y] = 3
                    elif np.random.rand() < self.prawdopodobienstwo_ozdrowienia:
                        nowa_siatka[x, y] = 2
        self.siatka = nowa_siatka

    def animacja(self, liczba_krokow):
        fig, ax = plt.subplots()
        ax.axis('off')
        mat = ax.matshow(self.siatka, cmap='viridis')

        def update(frame):
            self.step()
            mat.set_data(self.siatka)
            return [mat]

        ani = animation.FuncAnimation(fig, update, frames=liczba_krokow, blit=True, repeat=False)
        plt.show()

    def wykonaj_symulacje(self, liczba_krokow):
        dane_zakazeni, dane_ozdrowieni, dane_zmarly = [], [], []
        for _ in range(liczba_krokow):
            self.step()
            zakazeni = np.sum(self.siatka == 1)
            ozdrowieni = np.sum(self.siatka == 2)
            zmarly = np.sum(self.siatka == 3)
            dane_zakazeni.append(zakazeni)
            dane_ozdrowieni.append(ozdrowieni)
            dane_zmarly.append(zmarly)
        return dane_zakazeni, dane_ozdrowieni, dane_zmarly

if __name__ == "__main__":
    szerokosc = 100
    wysokosc = 100
    liczba_krokow = 200

    # Parametry modelu
    prawdopodobienstwo_zakazenia = 0.05
    prawdopodobienstwo_ozdrowienia = 0.01
    smiertelnosc = 0.02

    # Inicjalizacja automatu komórkowego
    gra = CellularAutomaton(szerokosc, wysokosc, prawdopodobienstwo_zakazenia, prawdopodobienstwo_ozdrowienia, smiertelnosc)

    # Wizualizacja automatu komórkowego
    gra.animacja(liczba_krokow)

    # Wykonanie symulacji i zbieranie danych
    dane_zakazeni, dane_ozdrowieni, dane_zmarly = gra.wykonaj_symulacje(liczba_krokow)

    # Tworzenie wykresów
    plt.figure(figsize=(12, 6))
    plt.plot(dane_zakazeni, label="Zakażeni")
    plt.plot(dane_ozdrowieni, label="Ozdrowieńcy")
    plt.plot(dane_zmarly, label="Zmarli")
    plt.xlabel("Krok")
    plt.ylabel("Liczba osób")
    plt.legend()
    plt.title("Symulacja fali zakażeń")
    plt.show()

