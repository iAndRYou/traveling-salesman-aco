import os

def log(iteration, route, distance, specifics=""):
    dir_path = f"./logs/{specifics}"
    
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        
    instances = 0
    while os.path.exists(f"{dir_path}/log{instances}.txt"):
        instances += 1
    
    with open(f"{dir_path}/log{instances}.txt", "w") as f:
        f.write("Iteration\tRoute\tDistance\n")
        f.write(f"{iteration}\t{route}\t{distance}")
    
def save_plot(plot, specifics=""):
    dir_path = f"./plots/{specifics}"
    
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        
    instances = 0
    while os.path.exists(f"{dir_path}/plot{instances}.png"):
        instances += 1
        
    plot.savefig(f"{dir_path}/plot{instances}.png")