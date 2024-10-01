import networkx as nx
import matplotlib.pyplot as plt
from math import exp, cos
from cmath import phase
import random


# Probability function
def probability_function(wind, moist, H, T):
    P = wind * exp(-0.05 * H) * (1 - exp(-0.064 * T)) * moist
    return P


# Distance function
def distance(Coo, u, v):
    return abs(Coo[u] - Coo[v])


# Wind part function
def wind_part(Coo, u, v, D, WD):
    W = phase((Coo[v] - Coo[u]) * WD)
    return  (1 - exp(-3.68 * (cos(W) + 0.6)**2 / D))


# Moisture part function
def moisture_part(Moist, v):
    return exp(-0.3 * Moist[v])


def run_simulation(num_trees, G, num_simulations, Moist, Coo, WD, H, T):
    i = 0
    current_state = {j: G.nodes[j]['state'] for j in G.nodes}
    while True:
        for tree_index in G.nodes:
            if current_state[tree_index] == 'burning':
                for neighbor_index in G.neighbors(tree_index):
                    if current_state[neighbor_index] == 'not burning':
                        a = distance(Coo, tree_index, neighbor_index)
                        b = wind_part(Coo, tree_index, neighbor_index, a, WD)
                        c = moisture_part(Moist, neighbor_index)
                        p = probability_function(b, c, H, T)
                        print(p)
                        if random.random() < p:
                            current_state[neighbor_index] = 'burning'
                            
                            # Update the node states in the graph
                            for node_index, state in current_state.items():
                                G.nodes[node_index]['state'] = state
                            
                            # Set the node colors based on their state
                            node_colors = ["green" if node[1]["state"] == "not burning" else "red" for node in G.nodes(data=True)]
                            
                            # Draw the graph with the specified node colors
                            pos = nx.get_node_attributes(G, "pos")
                            nx.draw(G, pos, node_color=node_colors, with_labels=True)
                            
                            # Show the graph
                            plt.show()

        i += 1
        if i == num_simulations:
            break

    # Update the node states in the graph
    for node_index, state in current_state.items():
        G.nodes[node_index]['state'] = state

    return current_state



# Ask user to input the number of trees in the forest
num_trees = int(input("Enter the number of trees in the forest: "))

# Ask user for general parameters
Wx = float(input(f"Enter the x-coordinate for wind direction: "))
Wy = float(input(f"Enter the y-coordinate for wind direction: "))
wind_direction = complex(Wx, -Wy)
humidity = float(input("Enter the degree of humidity: "))
moisture_levels = {}
for i in range(num_trees):
    moisture_level = float(input(f"Enter the moisture level for tree {i + 1}: "))
    moisture_levels[i] = moisture_level
temperature = float(input("Enter the temperature in degrees: "))


# Create an empty graph
G = nx.Graph()

# Add nodes to the graph with their properties
for i in range(num_trees):
    x = float(input(f"Enter the x-coordinate for tree {i}: "))
    y = float(input(f"Enter the y-coordinate for tree {i}: "))
    coo = complex(x, y)
    G.add_node(i, pos=(x, y), state="not burning", coo=coo)

# Generate edges for the input graph to make it complete
for i in range(num_trees):
    for j in range(i + 1, num_trees):
        G.add_edge(i, j)

# Create a dictionary to store node indices and their corresponding coo values
coordinates = {i: G.nodes[i]['coo'] for i in G.nodes}

# Create a dictionary to store node indices and their corresponding states
states = {i: G.nodes[i]['state'] for i in G.nodes}

# Set the node colors based on their state
node_colors = ["green" if node[1]["state"] == "not burning" else "red" for node in G.nodes(data=True)]

# Draw the graph with the specified node colors
pos = nx.get_node_attributes(G, "pos")
nx.draw(G, pos, node_color=node_colors, with_labels=True)

# Show the graph
print(states)
plt.show()

# Ask user to input the tree number to set as "burning"
tree_to_burn = int(input("Enter the tree number you want to set as burning (0-indexed): "))
G.nodes[tree_to_burn]["state"] = "burning"

# Set the node colors based on their state
node_colors = ["green" if node[1]["state"] == "not burning" else "red" for node in G.nodes(data=True)]

# Draw the graph with the specified node colors
pos = nx.get_node_attributes(G, "pos")
nx.draw(G, pos, node_color=node_colors, with_labels=True)

# Show the graph
print(states)
plt.show()


# ... (rest of your code) ...

while True:
   

    # Set the number of simulations to run
    num_simulations = int(input("Enter the number of simulations to run: "))

    # Run the simulation
    updated_states = run_simulation(num_trees, G, num_simulations, moisture_levels, coordinates, wind_direction,
                                    humidity, temperature)

    # Set the node colors based on the updated states
    node_colors = ["green" if updated_states[node] == "not burning" else "red" for node in G.nodes]

    # Draw the graph with the updated node colors
    nx.draw(G, pos, node_color=node_colors, with_labels=True)

    # Show the graph
    print(updated_states)

     # Ask user if they want to run another simulation

    run_again = input("Do you want to run another simulation? (yes/no): ")
    if run_again.lower() != 'yes':
        break
   