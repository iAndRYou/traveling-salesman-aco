import os

def log(iteration, route, distance, args):
    dir_path = f"./logs/{args.cities}_{args.ants}_{args.alpha}_{args.beta}_{args.evaporation}_{args.pheromone}"
    
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        
    instances = 0
    while os.path.exists(f"{dir_path}/log{instances}.txt"):
        instances += 1
    
    with open(f"{dir_path}/log{instances}.txt", "w") as f:
        f.write("Iteration\tRoute\tDistance\tCitites\tAnts\tAlpha\tBeta\tEvaporation\tPheromone\n")
        f.write(f"{iteration}\t{route}\t{distance}\t{args.cities}\t{args.ants}\t{args.alpha}\t{args.beta}\t{args.evaporation}\t{args.pheromone}")
    
def save_plot(plot, args):
    dir_path = f"./plots/{args.cities}_{args.ants}_{args.alpha}_{args.beta}_{args.evaporation}_{args.pheromone}"
    
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        
    instances = 0
    while os.path.exists(f"{dir_path}/plot{instances}.png"):
        instances += 1
        
    plot.savefig(f"{dir_path}/plot{instances}.png")