def adjust_indentation(code, spaces=4):
    lines = code.split('\n')
    current_indent = 0
    formatted_code = ""
    for line in lines:
        stripped_line = line.strip()
        if stripped_line:
            if stripped_line[-1] in (':', '{', '['):
                formatted_code += ' ' * current_indent + stripped_line + '\n'
                current_indent += spaces
            elif stripped_line[0] in ('}', ']'):
                current_indent = max(0, current_indent - spaces)
                formatted_code += ' ' * current_indent + stripped_line + '\n'
            else:
                formatted_code += ' ' * current_indent + stripped_line + '\n'
        else:
            formatted_code += '\n'

    # Adjusting the indentation of specific lines
    formatted_code = formatted_code.replace(' ' * spaces * 2, ' ' * spaces, 1)
    formatted_code = formatted_code.replace(' ' * spaces * 3, ' ' * spaces, 1)
    formatted_code = formatted_code.replace(' ' * spaces * 4, ' ' * spaces, 1)

    return formatted_code




import re


def adjust_spacing(code):
    # Ensure single space around operators and after commas
    code = re.sub(r'(\S)([=+\-*/%<>&|^])(\S)', r'\1 \2 \3', code)
    code = re.sub(r',', r', ', code)

    # Adjust the indentation after spacing modifications
    lines = code.split('\n')
    adjusted_lines = []
    current_indent = 0
    for line in lines:
        leading_space_count = len(line) - len(line.lstrip())
        current_indent += leading_space_count
        adjusted_lines.append(' ' * current_indent + line.lstrip())
        current_indent = max(0, current_indent - 4)

    return '\n'.join(adjusted_lines)


# Example usage:
unformatted_code = '''
def binary_search(arr, x):
start = 0
end = len(arr) - 1
while start <= end:
        mid = start + (end - start) // 2
        if arr[mid] == x:
            return mid
        elif arr[mid] < x:
            start = mid + 1
        else:
            end = mid - 1
    return -1

'''

# Applying indentation adjustment
indented_code = adjust_indentation(unformatted_code)
print("Code after adjusting indentation:\n", indented_code)

# # Applying spacing adjustment
# adjusted_code = adjust_spacing(indented_code)
# print("\nCode after adjusting spacing:\n", adjusted_code)

