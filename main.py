import argparse
import numpy as np
import matplotlib.pyplot as plt
from aco import AntColonyOptimization
from log import log, save_plot

# Domyślne arametry algorytmu
NUM_CITIES = 25         # Liczba początkowych miast
NUM_ANTS = 20           # Liczba mrówek
MAX_ITERATIONS = 100    # Liczba iteracji
ALPHA = 1.0             # Waga śladu feromonu
BETA = 5.0              # Waga heurystyki (odległość)
EVAPORATION_RATE = 0.5  # Współczynnik parowania feromonu
PHEROMONE_CONST = 100   # Stała feromonu dla najlepszej ścieżki

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--log", help="Tryb logowania", action="store_true")
    parser.add_argument("-s", "--seed", help="Ustawienie ziarna losowości", type=int, default=None)
    parser.add_argument("-c", "--cities", help="Liczba miast", type=int, default=NUM_CITIES)
    parser.add_argument("-a", "--ants", help="Liczba mrówek", type=int, default=NUM_ANTS)
    parser.add_argument("-i", "--iterations", help="Liczba iteracji", type=int, default=MAX_ITERATIONS)
    parser.add_argument("--alpha", help="Waga śladu feromonu", type=float, default=ALPHA)
    parser.add_argument("--beta", help="Waga heurystyki (odległość)", type=float, default=BETA)
    parser.add_argument("--evaporation", help="Współczynnik parowania feromonu", type=float, default=EVAPORATION_RATE)
    parser.add_argument("--pheromone", help="Stała feromonu dla najlepszej ścieżki", type=float, default=PHEROMONE_CONST)
    args = parser.parse_args()
    
    if args.seed:
        np.random.seed(args.seed)
    
    cities = np.random.rand(NUM_CITIES, 2) * 100

    aco = AntColonyOptimization(
        cities=cities, 
        num_ants=args.ants, 
        alpha=args.alpha, 
        beta=args.beta, 
        evaporation_rate=args.evaporation, 
        pheromone_constant=args.pheromone
    )

    aco.plot_init_cities()
    iteration, best_distance, best_route, best_plot = aco.run(max_iterations=args.iterations)

    if args.log:
        log(
            iteration, 
            best_distance, 
            best_route, 
            specifics=f"{NUM_CITIES}_{NUM_ANTS}_{MAX_ITERATIONS}_{ALPHA}_{BETA}_{EVAPORATION_RATE}_{PHEROMONE_CONST}"
        )
        
        save_plot(
            best_plot, 
            specifics=f"{NUM_CITIES}_{NUM_ANTS}_{MAX_ITERATIONS}_{ALPHA}_{BETA}_{EVAPORATION_RATE}_{PHEROMONE_CONST}"
        )

    print("Najlepsza znaleziona trasa:", best_route)
    print("Długość najlepszej trasy:", best_distance)
    plt.waitforbuttonpress()
