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
        stripped_line = line.strip()  # Strip from both sides
        if stripped_line:  # If the line is not just spaces
            if current_indent == 0 and stripped_line.startswith(('def ', 'class ')):
                indented_line = stripped_line
            else:
                indented_line = ' ' * current_indent + stripped_line
        else:
            indented_line = line

        if stripped_line.endswith(':'):
            current_indent += spaces
        elif stripped_line.startswith('else:'):
            current_indent -= spaces

        indented_code.append(indented_line)

    return '\n'.join(indented_code)

# Example usage
code = """
class MyClass(object):
def myFunction(self, x, y):
                        # This is a comment
if x + y > z:
return x - y
else:
return x + y
"""

formatted_code = enforce_indentation(code)
print(formatted_code)
