# Travelling Salesman Problem (TSP) using Ant Colony Optimisation (ACO)

Ant Colony Optimisation implementation for Travelling Salesman Problem.
The program first generates a random set of cities (x, y) and then uses the ACO algorithm to find the shortest path
that visits each city exactly once and returns to the origin city.

Includes a visualisation of the process using matplotlib.

## Requirements

To run the code you need to have python3 installed. You can install the required packages using pip:

```bash
pip install -r requirements.txt
```

## Usage

To run the code you can use the following command:

```bash
python main.py
```

You can change many parameters including:

- `-a` or `--ants` to change the number of ants (default is 10)
- `--alpha` to change the alpha parameter - pheromone heuristic (default is 1)
- `--beta` to change the beta parameter - distance heuristic (default is 5)
- `--evaporation` to change the evaporation rate (default is 0.5)

For further information on parameters you can change, please use the help command:

```bash
python main.py -h
```
