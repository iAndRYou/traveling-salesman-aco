import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

structure = {
    "logs": {
        "dir": "./logs/",
        "file": "log",
        "extension": "txt"
    },
    "plots": {
        "dir": "./plots/",
        "file": "plot",
        "extension": "png"
    }
}

def get_all_directories(path):
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

def get_logs(directory):
    return [f for f in os.listdir(f"{structure['logs']['dir']}{directory}") if f.endswith(structure['logs']['extension'])]

def agregate_logs(directory):
    logs = get_logs(directory)
    data = pd.DataFrame()
    for log in logs:
        with open(f"{structure['logs']['dir']}{directory}/{log}", "r") as f:
            df = pd.read_csv(f, sep="\t", header=0)
            data = pd.concat([data, df])
    
    data.columns = ["iteration", "best_route", "best_distance", "cities", "ants", "alpha", "beta", "evaporation", "pheromone"]
    data.to_csv(f"{structure['logs']['dir']}{directory}/agregated.csv", sep="\t", index=False)
    

    plt.figure(figsize=(10, 5))
    plt.plot(np.array(data["iteration"]), label="Iterations")
    plt.plot(np.array(data["best_distance"]), label="Best distance")
    
    plt.legend()
    plt.xlabel("Attempt")
    plt.savefig(f"{structure['plots']['dir']}{directory}/agregated.png")
        
        

if __name__ == "__main__":
    directories = get_all_directories(structure["logs"]["dir"])
    
    for directory in directories:
        agregate_logs(directory)
    
    
