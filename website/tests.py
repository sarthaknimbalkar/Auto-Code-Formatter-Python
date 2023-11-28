# Simulated Annealing
import math
import random

# The initial state is the string to be formatted
initial_state = "This is a string to be formatted. Let's elongate the string and verify that it works properly"


# The cost function is the number of spaces in the string
def cost_function(state):
    return state.count(" ")


# The neighbor function is to randomly change one space to a tab or vice versa
def neighbor(state):
    index = random.randint(0, len(state) - 1)
    char_to_replace = "\t" if state[index] == " " else " "
    return state[:index] + char_to_replace + state[index + 1:]


# The simulated annealing function
def simulated_annealing(initial_state, cost_function, neighbor, temperature, cooling_rate):
    current_state = initial_state
    current_cost = cost_function(current_state)
    while temperature > 1:
        print(f"Current state: {current_state}, Current cost: {current_cost}, Temperature: {temperature}")
        new_state = neighbor(current_state)
        new_cost = cost_function(new_state)
        if new_cost < current_cost or random.uniform(0, 1) < math.exp((current_cost - new_cost) / temperature):
            current_state, current_cost = new_state, new_cost
        temperature *= 1 - cooling_rate
    return current_state


# Run the simulated annealing algorithm
formatted_string = simulated_annealing(initial_state, cost_function, neighbor, 1000, 0.001)
print(f"Final state: {formatted_string}")


# DFS simulation
class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children if children is not None else []

    def format(self, indent=0):
        print(' ' * indent + self.value)
        for child in self.children:
            child.format(indent + 2)


# Example usage:
root = Node('root', [
    Node('child1', [
        Node('grandchild1'),
        Node('grandchild2')
    ]),
    Node('child2')
])

root.format()
