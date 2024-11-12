import numpy as np
import matplotlib.pyplot as plt

# Parametry algorytmu
num_cities = 10            # Liczba miast
num_ants = 20              # Liczba mrówek
num_iterations = 100       # Liczba iteracji
alpha = 1.0                # Waga śladu feromonu
beta = 5.0                 # Waga heurystyki (odległość)
evaporation_rate = 0.5     # Współczynnik parowania feromonu
pheromone_constant = 100   # Stała feromonu dla najlepszej ścieżki

np.random.seed(42)
cities = np.random.rand(num_cities, 2) * 100

def calculate_distance_matrix(cities):
    n = len(cities)
    distance_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            distance_matrix[i][j] = np.linalg.norm(cities[i] - cities[j])
    return distance_matrix

def route_length(route, distance_matrix):
    length = 0
    for i in range(len(route) - 1):
        length += distance_matrix[route[i]][route[i + 1]]
    length += distance_matrix[route[-1]][route[0]]
    return length

distance_matrix = calculate_distance_matrix(cities)
pheromone_matrix = np.ones((num_cities, num_cities))

def select_next_city(current_city, visited, pheromone_matrix, distance_matrix):
    probabilities = []
    for i in range(num_cities):
        if i not in visited:
            tau_eta = (pheromone_matrix[current_city][i] ** alpha) * ((1.0 / distance_matrix[current_city][i]) ** beta)
            probabilities.append(tau_eta)
        else:
            probabilities.append(0)
    probabilities = np.array(probabilities)
    probabilities /= probabilities.sum()
    next_city = np.random.choice(range(num_cities), p=probabilities)
    return next_city

def update_pheromone(pheromone_matrix, routes, distances):
    pheromone_matrix *= (1 - evaporation_rate)
    for route, distance in zip(routes, distances):
        for i in range(len(route) - 1):
            pheromone_matrix[route[i]][route[i + 1]] += pheromone_constant / distance
            pheromone_matrix[route[i + 1]][route[i]] += pheromone_constant / distance
        pheromone_matrix[route[-1]][route[0]] += pheromone_constant / distance
        pheromone_matrix[route[0]][route[-1]] += pheromone_constant / distance

def plot_route_and_pheromones(route, cities, pheromone_matrix, iteration, distance):
    plt.cla()
    plt.scatter(cities[:, 0], cities[:, 1], color='blue', marker='o')
    max_pheromone = pheromone_matrix.max()
    for i in range(num_cities):
        for j in range(i + 1, num_cities):
            pheromone_level = pheromone_matrix[i][j] / max_pheromone
            if pheromone_level > 0.01:
                plt.plot([cities[i][0], cities[j][0]], [cities[i][1], cities[j][1]],
                         'grey', alpha=pheromone_level, linewidth=pheromone_level * 5)

    for i in range(len(route)):
        start_city = route[i]
        end_city = route[(i + 1) % len(route)]
        plt.plot([cities[start_city][0], cities[end_city][0]], [cities[start_city][1], cities[end_city][1]], 'r')
    
    plt.title(f'Iteration {iteration} - Distance: {distance:.2f}')
    plt.pause(0.1)

best_route = None
best_distance = float('inf')

plt.figure(figsize=(8, 6))
for iteration in range(num_iterations):
    routes = []
    distances = []

    for ant in range(num_ants):
        route = [np.random.randint(num_cities)]
        while len(route) < num_cities:
            next_city = select_next_city(route[-1], route, pheromone_matrix, distance_matrix)
            route.append(next_city)
        route_distance = route_length(route, distance_matrix)
        routes.append(route)
        distances.append(route_distance)

        if route_distance < best_distance:
            best_route = route
            best_distance = route_distance

    update_pheromone(pheromone_matrix, routes, distances)
    plot_route_and_pheromones(best_route, cities, pheromone_matrix, iteration, best_distance)

print("Najlepsza znaleziona trasa:", best_route)
print("Długość najlepszej trasy:", best_distance)
plt.show()
