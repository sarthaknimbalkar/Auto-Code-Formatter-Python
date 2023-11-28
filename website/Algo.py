import math
import random

from .formatter import *


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


def evaluate_spacing(lines, expected_spacing=2):
    """
    Evaluate spacing violations and return a penalty score.
    """
    spacing_penalty = sum(max(0, len(line.split()) - 1 - expected_spacing) for line in lines)
    return 1 / (1 + spacing_penalty)


def evaluate_line_length(lines, max_line_length=79):
    """
    Evaluate line length violations and return a penalty score.
    """
    length_penalty = sum(max(0, len(line) - max_line_length) for line in lines)
    return 1 / (1 + length_penalty)


def evaluate_indentation(lines, expected_indentation=' ' * 4):
    """
    Evaluate indentation violations and return a penalty score.
    """
    indentation_penalty = sum(not line.startswith(expected_indentation) for line in lines)
    return 1 / (1 + indentation_penalty)


def evaluate_import_format(lines):
    """
    Evaluate import formatting violations and return a penalty score.
    """
    import_penalty = sum(1 for line in lines if line.strip().startswith("import") or line.strip().startswith("from"))
    return 1 / (1 + import_penalty)


def evaluate_line_continuation(lines):
    """
    Evaluate line continuation formatting violations and return a penalty score.
    """
    continuation_penalty = sum(1 for line in lines if line.rstrip().endswith("\\"))
    return 1 / (1 + continuation_penalty)


def evaluate_string_formatting(lines):
    """
    Evaluate string formatting violations and return a penalty score.
    """
    # Example: Penalize for not using f-strings (Python 3.6+)
    formatting_penalty = sum(1 for line in lines if "{" in line and "}" in line and not line.lstrip().startswith("f"))
    return 1 / (1 + formatting_penalty)


def evaluate_function_calls(lines):
    """
    Evaluate function call formatting violations and return a penalty score.
    """
    function_call_penalty = sum(1 for line in lines if "(" in line and not line.lstrip().endswith(")"))
    return 1 / (1 + function_call_penalty)


def evaluate_extra_whitespace(lines):
    """
    Evaluate extra whitespace violations and return a penalty score.
    """
    whitespace_penalty = sum(1 for line in lines if len(line) != len(line.rstrip()))
    return 1 / (1 + whitespace_penalty)


def evaluate_comments(lines):
    """
    Evaluate comment formatting violations and return a penalty score.
    """
    # Example: Penalize for not using '#' for comments
    comment_penalty = sum(1 for line in lines if line.strip().startswith("//"))
    return 1 / (1 + comment_penalty)


def evaluate_snake_case(lines):
    """
    Evaluate variable naming violations and return a penalty score.
    """
    # Example: Penalize for not using snake_case for variable names
    snake_case_penalty = sum(
        1 for line in lines if any(word.isidentifier() and word.lower() != word for word in line.split()))
    return 1 / (1 + snake_case_penalty)


def evaluate_block_structure(lines):
    """
    Evaluate block structure formatting violations and return a penalty score.
    """
    # Example: Penalize for not using consistent indentation for blocks
    block_structure_penalty = sum(
        1 for line in lines if line.strip().startswith("if") or line.strip().startswith("else"))
    return 1 / (1 + block_structure_penalty)


def evaluate_special_syntax_rules(lines):
    """
    Evaluate violations related to special syntax rules and return a penalty score.
    """
    # Example: Penalize for not using a specific syntax rule
    special_syntax_penalty = sum(1 for line in lines if "your_special_syntax_rule" in line)
    return 1 / (1 + special_syntax_penalty)


def evaluate_code(code_content):
    """
    Evaluate code based on multiple aspects and return an overall score.
    """
    # Split code content into lines
    lines = code_content.split('\n')

    # Evaluate line length, indentation, spacing, import format, line continuation,
    # string formatting, function calls, extra whitespace, comments, snake case,
    # block structure, and special syntax rules
    line_length_score = evaluate_line_length(lines)
    indentation_score = evaluate_indentation(lines)
    spacing_score = evaluate_spacing(lines)
    import_format_score = evaluate_import_format(lines)
    line_continuation_score = evaluate_line_continuation(lines)
    string_formatting_score = evaluate_string_formatting(lines)
    function_calls_score = evaluate_function_calls(lines)
    extra_whitespace_score = evaluate_extra_whitespace(lines)
    comments_score = evaluate_comments(lines)
    snake_case_score = evaluate_snake_case(lines)
    block_structure_score = evaluate_block_structure(lines)
    special_syntax_score = evaluate_special_syntax_rules(lines)

    # Combine scores based on your desired weighting
    score = (line_length_score + indentation_score + spacing_score +
             import_format_score + line_continuation_score +
             string_formatting_score + function_calls_score +
             extra_whitespace_score + comments_score +
             snake_case_score + block_structure_score +
             special_syntax_score) / 12

    return score
