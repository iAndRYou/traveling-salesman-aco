import numpy as np
import matplotlib.pyplot as plt

class AntColonyOptimization:
    def __init__(self, cities, num_ants, alpha, beta, evaporation_rate, pheromone_constant):
        self.cities = cities
        self.num_ants = num_ants
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.pheromone_constant = pheromone_constant
        
        self.distance_matrix = self.calculate_distance_matrix()
        self.pheromone_matrix = np.ones_like(self.distance_matrix)
        self.best_route = None
        self.best_distance = float('inf')
        
        
    def calculate_distance_matrix(self):
        n = len(self.cities)
        distance_matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                distance_matrix[i][j] = np.linalg.norm(self.cities[i] - self.cities[j])
                
        return distance_matrix


    def route_length(self, route):
        length = 0
        
        for i in range(len(route) - 1):
            length += self.distance_matrix[route[i]][route[i + 1]]
        length += self.distance_matrix[route[-1]][route[0]]
        
        return length


    def select_next_city(self, current_city, visited):
        probabilities = []
        
        for i in range(len(self.distance_matrix)):
            if i not in visited:
                tau_eta = (self.pheromone_matrix[current_city][i] ** self.alpha) * ((1.0 / self.distance_matrix[current_city][i]) ** self.beta)
                probabilities.append(tau_eta)
            else:
                probabilities.append(0)
                
        probabilities = np.array(probabilities)
        probabilities /= probabilities.sum()
        
        next_city = np.random.choice(range(len(self.distance_matrix)), p=probabilities)
        
        return next_city


    def update_pheromone(self, routes, distances):
        self.pheromone_matrix *= (1 - self.evaporation_rate)
        
        for route, distance in zip(routes, distances):
            for i in range(len(route) - 1):
                self.pheromone_matrix[route[i]][route[i + 1]] += self.pheromone_constant / distance
                self.pheromone_matrix[route[i + 1]][route[i]] += self.pheromone_constant / distance
            self.pheromone_matrix[route[-1]][route[0]] += self.pheromone_constant / distance
            self.pheromone_matrix[route[0]][route[-1]] += self.pheromone_constant / distance


    def plot_init_cities(self):
        fig = plt.figure(figsize=(8, 6))
        fig.canvas.manager.set_window_title("Initial Cities")
        
        plt.cla()
        plt.axis('off')
        plt.scatter(self.cities[:, 0], self.cities[:, 1], color='blue', marker='o')    # Rysowanie miast
        
        plt.title(f'Iteration: init, Distance: {self.best_distance:.2f}')
        plt.pause(0.1)


    def plot_route_and_pheromones(self, iteration, final=False):
        plt.cla()
        plt.axis('off')
        plt.scatter(self.cities[:, 0], self.cities[:, 1], color='blue', marker='o')     # Rysowanie miast
        
        max_pheromone = self.pheromone_matrix.max()
        for i in range(len(self.cities)):       # Rysowanie śladów feromonu
            
            for j in range(i + 1, len(self.cities)):
                pheromone_level = self.pheromone_matrix[i][j] / max_pheromone
                
                if pheromone_level > 0.01:
                    plt.plot([self.cities[i][0], self.cities[j][0]], [self.cities[i][1], self.cities[j][1]],
                            'grey', alpha=pheromone_level, linewidth=pheromone_level * 5)

        for i in range(len(self.best_route)):    # Rysowanie trasy
            start_city = self.best_route[i]
            end_city = self.best_route[(i + 1) % len(self.best_route)]
            
            plt.plot([self.cities[start_city][0], self.cities[end_city][0]], [self.cities[start_city][1], self.cities[end_city][1]], 'r')
        
        if final:
            plt.title(f'Iteration: {iteration}, Distance: {self.best_distance:.2f} - FINAL')
        else:
            plt.title(f'Iteration: {iteration}, Distance: {self.best_distance:.2f}')
        plt.pause(0.1)
        
        return plt.gcf()
    
     
    def run(self, max_iterations, stop_iterations):
        fig = plt.figure(figsize=(8, 6))
        fig.canvas.manager.set_window_title("Ant Colony Optimization")

        no_change_counter = 0       # Licznik iteracji bez zmian
        previous_best_distance = self.best_distance     # Poprzednia najlepsza odległość

        for iteration in range(max_iterations):
            if no_change_counter == stop_iterations:
                plot = self.plot_route_and_pheromones(iteration, final=True)
                return iteration, self.best_route, self.best_distance, plot

            routes = []
            distances = []

            for _ in range(self.num_ants):
                route = [np.random.randint(len(self.cities))]
                
                while len(route) < len(self.cities):
                    next_city = self.select_next_city(route[-1], route)
                    route.append(next_city)
                    
                route_distance = self.route_length(route)
                routes.append(route)
                distances.append(route_distance)

                if route_distance < self.best_distance:
                    self.best_route = route
                    self.best_distance = route_distance

            if self.best_distance == previous_best_distance:
                no_change_counter += 1
            else:
                no_change_counter = 0
                previous_best_distance = self.best_distance

            self.update_pheromone(routes, distances)
            plot = self.plot_route_and_pheromones(iteration)
        
        return iteration, self.best_route, self.best_distance, plot