import math
import random

from formatter import *


class CodeNode:
    def __init__(self, content, children=None):
        self.content = content
        self.children = children if children else []

    def add_child(self, node):
        self.children.append(node)


def apply_dfs_formatting(code_content, formatting_rules):
    def dfs(node, rules):
        for child in node.children:
            dfs(child, rules)
        for rule in rules:
            node.content = rule(node.content)

    root = CodeNode(code_content)

    dfs(root, formatting_rules)

    return root.content


# Simulated Annealing for code formatting
def simulated_annealing(code_content, formatting_rules, initial_temperature=100.0, stopping_temperature=0.1,
                        cooling_rate=0.99):
    current_state = code_content
    best_state = current_state

    current_score = evaluate_code(current_state)
    best_score = current_score

    temperature = initial_temperature

    while temperature > stopping_temperature:
        new_state = apply_dfs_formatting(current_state, formatting_rules)

        new_score = evaluate_code(new_state)

        if new_score < current_score or random.random() < acceptance_probability(current_score, new_score, temperature):
            current_state = new_state
            current_score = new_score

        if new_score < best_score:
            best_state = new_state
            best_score = new_score

        temperature *= cooling_rate

    return best_state


def acceptance_probability(current_score, new_score, temperature):
    if new_score < current_score:
        return 1.0
    return math.exp((current_score - new_score) / temperature)


# Define the list of formatting rules
formatting_rules = [enforce_indentation, enforce_spacing, enforce_line_length, format_imports,
                    format_line_continuation, format_string_formatting, format_function_calls,
                    remove_extra_whitespace, format_comments, convert_to_snake_case,
                    format_block_structure, format_special_syntax_rules]


# Define an evaluation function for code formatting
def evaluate_code(code_content):
    # NEEDS TO BE IMPLEMENTED
    return len(code_content)  # Example metric: length of the code

