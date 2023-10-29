import re


# Enforce proper indentation in the code content.
def enforce_indentation(code_content, spaces=4):
    lines = code_content.split('\n')
    indented_code = []
    current_indent = 0

    for line in lines:
        stripped_line = line.strip()
        if stripped_line:  # Check if the line is not empty after stripping
            leading_spaces = len(line) - len(stripped_line)  # Calculate leading spaces
            if any(stripped_line.startswith(keyword) for keyword in
                   ['def ', 'class ', 'elif ', 'except', 'finally', 'for ', 'if ', 'try', 'while ', 'with ']):
                indented_line = ' ' * current_indent + stripped_line
                if stripped_line.endswith(':') and not stripped_line.startswith('else:'):
                    current_indent += spaces
            elif stripped_line.startswith('else:') and len(stripped_line) == 5:
                current_indent -= spaces
                indented_line = ' ' * current_indent + stripped_line
                current_indent += spaces
            else:
                indented_line = ' ' * current_indent + line.lstrip()  # Preserve original leading spaces
            indented_code.append(indented_line)
        else:
            indented_line = ' ' * current_indent + stripped_line  # Preserve original leading spaces
            indented_code.append(indented_line)
    return '\n'.join(indented_code)


def enforce_spacing(text, spaces=4):
    lines = text.split('\n')
    spaced_text = []

    for line in lines:
        stripped_line = line.strip()

        if stripped_line.startswith("#"):  # Skip lines starting with #
            spaced_text.append(line)
        else:
            leading_spaces = len(line) - len(stripped_line)
            if leading_spaces:
                current_indent = ' ' * leading_spaces
                line = current_indent + stripped_line

            spaced_text.append(line)

    return '\n'.join(spaced_text)


def enforce_line_length(text, max_line_length=79):
    lines = text.split('\n')
    processed_lines = []

    for line in lines:
        if len(line) > max_line_length and not line.lstrip().startswith("print"):
            words = line.split()
            current_line = ''
            for word in words:
                if len(current_line) + len(word) + 1 <= max_line_length:
                    if current_line:
                        current_line += ' ' + word
                    else:
                        current_line += word
                else:
                    processed_lines.append(current_line)
                    current_line = word
            if current_line:
                processed_lines.append(current_line)
        else:
            processed_lines.append(line)

    return '\n'.join(processed_lines)


# Format import statements as per PEP8 standards.
def format_imports(import_statements):
    imports = import_statements.split('\n')
    formatted_imports = []
    current_section = ''

    for imp in imports:
        if imp.strip().startswith(('import', 'from')):
            if current_section:
                formatted_imports.append('\n')
            current_section = imp
            formatted_imports.append(imp)
        else:
            formatted_imports.append(imp)

    return '\n'.join(formatted_imports)


# Format line continuation in the code content as per PEP8 standards.
def format_line_continuation(code_content):
    lines = code_content.split('\n')
    formatted_code = []

    continuation = False
    for line in lines:
        stripped_line = line.rstrip()
        if continuation:
            formatted_code[-1] += ' ' + stripped_line.lstrip()
            continuation = stripped_line.endswith('\\')
        elif stripped_line.endswith('\\'):
            continuation = True
            formatted_code.append(stripped_line[:-1].rstrip())
        else:
            formatted_code.append(stripped_line)

    formatted_code = [re.sub(r'\\', '', line) for line in formatted_code]

    return '\n'.join(formatted_code)


# Format string formatting in the code content as per PEP8 standards.
def format_string_formatting(code_content):
    pattern = re.compile(r'%\((\w+)\)[sd]?')
    formatted_code = re.sub(pattern, r'{\1}', code_content)
    return formatted_code


# Format function and method calls in the code content as per PEP8 standards.
def format_function_calls(code_content):
    pattern = re.compile(r',\s*')
    formatted_code = re.sub(pattern, ', ', code_content)
    return formatted_code


# Remove extra whitespaces from the code content while preserving necessary indentation.
def remove_extra_whitespace(code_content):
    lines = code_content.split('\n')
    formatted_code = []

    for line in lines:
        leading_spaces = re.match(r'^\s*', line).group()
        stripped_line = re.sub(r'\s+', ' ', line)
        formatted_code.append(leading_spaces + stripped_line.strip())

    return '\n'.join(formatted_code)


# # Format comments in the code content as per PEP8 standards.
def format_comments(code_content):
    lines = code_content.split('\n')
    formatted_code = []

    for line in lines:
        line = re.sub(r'\s*#', ' #', line)
        formatted_code.append(line)

    return '\n'.join(formatted_code)


# Convert variable names to lowercase with underscores (snake_case).
def convert_to_snake_case(code_content):
    formatted_code = re.sub(r'([a-z])([A-Z])', r'\1_\2', code_content)
    formatted_code = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', formatted_code)
    formatted_code = formatted_code.lower()
    return formatted_code


# Format block structure in the code content as per PEP8 standards.
def format_block_structure(code_content, spaces=4):
    lines = code_content.split('\n')
    formatted_code = []
    current_indent = 0

    for line in lines:
        stripped_line = line.strip()
        if stripped_line:
            if stripped_line.endswith(':') and not (
                    stripped_line.startswith('else') or stripped_line.startswith('elif')):
                formatted_code.append(' ' * current_indent + stripped_line)
                current_indent += spaces
            elif stripped_line.startswith('else') or stripped_line.startswith('elif'):
                current_indent -= spaces
                formatted_code.append(' ' * current_indent + stripped_line)
                current_indent += spaces
            else:
                formatted_code.append(' ' * current_indent + stripped_line)
        else:
            formatted_code.append(' ' * current_indent + line)  # Preserve original leading spaces
    return '\n'.join(formatted_code)


# Format special syntax rules in the code content as per PEP8 standards.
def format_special_syntax_rules(code_content):
    lines = code_content.split('\n')
    formatted_code = []

    for line in lines:
        if line.strip().startswith('@'):  # Check for lines starting with '@'
            formatted_code.append('\n' + line)  # Add a newline before the line
        else:
            formatted_code.append(line)

    return '\n'.join(formatted_code)


# # Original sample code
# original_code = """
# # Sample code for testing the formatting functions
# def example_function(argument1, argument2, argument3):
#     if argument1 == 'test':
#         print('This is a test.')
#     elif argument2 == 'sample':
#         print('This is a sample.')
#     else:
#         print('No match found.')
#
# class ExampleClass:
#     def __init__(self, name):
#         self.name = name
#
#     def get_name(self):
#         return self.name
#
# import os
# import sys
# # This is a sample comment
# # Another comment line
#
# sample_string = "This is a %s string." % "sample"
# sample_list = [1, 2, 3, 4, 5]
# sample_variable = 10
#
# if sample_variable > 5:
#     print("Variable is greater than 5.")
# if sample_variable < 15:
#     print("Variable is less than 15.")
# """
#
# # Create a copy of the original code
# code_copy = original_code
#
# # Apply each formatting function to the copy of the code
# code_copy = enforce_indentation(code_copy)
# code_copy = enforce_spacing(code_copy)
# code_copy = enforce_line_length(code_copy)
# code_copy = format_imports(code_copy)
# code_copy = format_line_continuation(code_copy)
# code_copy = format_string_formatting(code_copy)
# code_copy = format_function_calls(code_copy)
# code_copy = remove_extra_whitespace(code_copy)
# code_copy = format_comments(code_copy)
# code_copy = convert_to_snake_case(code_copy)
# code_copy = format_block_structure(code_copy)
# code_copy = format_special_syntax_rules(code_copy)
#
# # Print the formatted code copy
# print(code_copy)

