import re


def enforce_indentation(code_content, spaces=4):
    """
    Enforce proper indentation in the code content.
    Args:
        code_content (str): The content of the code to be formatted.
        spaces (int): The number of spaces for each indentation level.
    Returns:
        str: The code content with corrected indentation.
    """
    lines = code_content.split('\n')
    indented_code = []
    current_indent = 0

    for line in lines:
        stripped_line = line.lstrip()  # Strip only from the left
        if stripped_line:
            leading_spaces = len(line) - len(stripped_line)
            if leading_spaces < current_indent:  # Adjust the current indent if necessary
                current_indent = leading_spaces
            if stripped_line.startswith(
                    ('def ', 'class ', 'elif ', 'else:', 'except', 'finally', 'for ', 'if ', 'try', 'while ', 'with ')):
                indented_line = ' ' * current_indent + stripped_line
            else:
                indented_line = ' ' * (current_indent + spaces) + stripped_line
            indented_code.append(indented_line)
        else:
            indented_code.append(line)

    return '\n'.join(indented_code)


# Spacing
def enforce_spacing(text, spaces=4):
    """
    Enforce proper spacing in the text content.
    Args:
        text (str): The text content to be formatted.
        spaces (int): The number of spaces for each indentation level.
    Returns:
        str: The text content with corrected spacing.
    """
    lines = text.split('\n')
    spaced_text = []
    current_indent = 0
    class_indent = 0

    for line in lines:
        stripped_line = line.strip()

        if stripped_line.startswith("#"):  # Skip lines starting with #
            spaced_text.append(line)
        else:
            leading_spaces = len(line) - len(stripped_line)

            if stripped_line.startswith('class ') or stripped_line.startswith('def '):
                current_indent = leading_spaces

            if not any(stripped_line.startswith(block) for block in ('def ', 'class ')):
                line = ' ' * current_indent + ' '.join(stripped_line.split())

            spaced_text.append(line)

    return '\n'.join(spaced_text)


# Line Length
def enforce_line_length(text, max_line_length=79):
    """
    Enforce a specific maximum line length in the text content.
    Args:
        text (str): The text content to be formatted.
        max_line_length (int): The maximum length for each line.
    Returns:
        str: The text content with lines limited to the maximum length.
    """
    words = text.split()
    lines = []
    current_line = words[0]

    for word in words[1:]:
        if len(current_line) + len(word) + 1 <= max_line_length:
            current_line += ' ' + word
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return '\n'.join(lines)


# Imports
def format_imports(import_statements):
    """
    Format import statements as per PEP8 standards.
    Args:
        import_statements (str): The import statements to be formatted.
    Returns:
        str: The formatted import statements.
    """
    imports = import_statements.split('\n')
    formatted_imports = []
    current_section = ''

    for imp in imports:
        if imp.startswith('import') or imp.startswith('from'):
            if current_section:
                formatted_imports.append('\n')
            current_section = imp
            formatted_imports.append(imp)
        else:
            formatted_imports.append(imp)

    return '\n'.join(formatted_imports)


# Line Continuation
def format_line_continuation(code_content):
    """
    Format line continuation in the code content as per PEP8 standards.
    Args:
        code_content (str): The content of the code to be formatted.
    Returns:
        str: The code content with corrected line continuation.
    """
    lines = code_content.split('\n')
    formatted_code = []

    continuation = False
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.endswith('\\'):
            continuation = True
            formatted_code.append(stripped_line[:-1].strip())
        elif continuation:
            formatted_code[-1] += stripped_line
            continuation = False
        else:
            formatted_code.append(stripped_line)

    return '\n'.join(formatted_code)


# String Formatting
def format_string_formatting(code_content):
    """
    Format string formatting in the code content as per PEP8 standards.
    Args:
        code_content (str): The content of the code to be formatted.
    Returns:
        str: The code content with corrected string formatting.
    """
    pattern = re.compile(r'%\((\w+)\)\w')
    formatted_code = re.sub(pattern, r'{\1}', code_content)
    return formatted_code


# Function and Method Call Formatting
def format_function_calls(code_content):
    """
    Format function and method calls in the code content as per PEP8 standards.
    Args:
        code_content (str): The content of the code to be formatted.
    Returns:
        str: The code content with corrected function and method calls.
    """
    pattern = re.compile(r'\s*,\s*')
    formatted_code = re.sub(pattern, ', ', code_content)
    return formatted_code


# Whitespace Removal
def remove_extra_whitespace(code_content):
    """
    Remove extra whitespaces from the code content while preserving necessary indentation.
    Args:
        code_content (str): The content of the code to be formatted.
    Returns:
        str: The code content with extra whitespaces removed.
    """
    lines = code_content.split('\n')
    formatted_code = []

    for line in lines:
        stripped_line = re.sub(' +', ' ', line)
        formatted_code.append(stripped_line)

    return '\n'.join(formatted_code)


# Does not work
# Updated Comment Formatting
def format_comments(code_content):
    """
    Format comments in the code content as per PEP8 standards.
    Args:
        code_content (str): The content of the code to be formatted.
    Returns:
        str: The code content with formatted comments.
    """
    lines = code_content.split('\n')
    formatted_code = []

    for line in lines:
        if '#' in line:
            line = re.sub(r'\s*#', ' #', line)
        formatted_code.append(line)

    return '\n'.join(formatted_code)


# Naming Conventions
def convert_to_snake_case(code_content):
    """
    Convert variable names to lowercase with underscores (snake_case).
    Args:
        code_content (str): The content of the code to be formatted.
    Returns:
        str: The code content with variable names in snake_case.
    """
    formatted_code = re.sub(r'([a-z])([A-Z])', r'\1_\2', code_content)
    formatted_code = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', formatted_code)
    formatted_code = formatted_code.lower()
    return formatted_code


# Block Structure
def format_block_structure(code_content, spaces=4):
    """
    Format block structure in the code content as per PEP8 standards.
    Args:
        code_content (str): The content of the code to be formatted.
        spaces (int): The number of spaces for each indentation level.
    Returns:
        str: The code content with corrected block structure.
    """
    lines = code_content.split('\n')
    formatted_code = []
    current_indent = 0

    for line in lines:
        line = line.strip()
        if line:
            if line.endswith(':') and not line.startswith('else') and not line.startswith('elif'):
                formatted_code.append(' ' * current_indent + line)
                current_indent += spaces
            elif line.startswith('else') or line.startswith('elif'):
                current_indent -= spaces
                formatted_code.append(' ' * current_indent + line)
                current_indent += spaces
            else:
                formatted_code.append(' ' * current_indent + line)

    return '\n'.join(formatted_code)


# Does not work
# Updated File and Class Organization
def format_file_and_class_organization(code_content):
    """
    Format file and class organization in the code content as per PEP8 standards.
    Args:
        code_content (str): The content of the code to be formatted.
    Returns:
        str: The code content with corrected file and class organization.
    """
    lines = code_content.split('\n')
    formatted_code = []

    in_class = False
    class_indent = 0

    for line in lines:
        line = line.strip()
        if line.startswith('class '):
            if in_class:
                formatted_code.append('')
            in_class = True
            formatted_code.append(line)
            class_indent += 4  # Adjust the indentation for nested classes
        elif line and not line.startswith('def ') and not line.startswith('@'):
            in_class = False
            class_indent = 0
            formatted_code.append(line)
        else:
            formatted_code.append(' ' * class_indent + line)

    return '\n'.join(formatted_code)


# Special Syntax Rules
def format_special_syntax_rules(code_content):
    """
    Format special syntax rules in the code content as per PEP8 standards.
    Args:
        code_content (str): The content of the code to be formatted.
    Returns:
        str: The code content with corrected special syntax rules.
    """
    lines = code_content.split('\n')
    formatted_code = []

    for line in lines:
        if line.strip().startswith('@'):  # Check for lines starting with '@'
            formatted_code.append('\n' + line.strip())  # Add a newline before the line
        else:
            formatted_code.append(line)

    return '\n'.join(formatted_code)

