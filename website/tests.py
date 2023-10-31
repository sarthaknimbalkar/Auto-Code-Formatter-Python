
import math, sys

class ExampleClass:
    def __init__(self):
        self.some_value = 5

    def some_method(self, x, y):
        return x + y

    def another_method(self, a, b):
        return a * b

def some_function(arg1, arg2):
    return arg1 - arg2

# This is a comment
if True:
    print("This is a test")
    if False:
        print("Nested if block")
    else:
        print("Nested else block")
    for i in range(5):
        if i % 2 == 0:
            print(f"Even number: {i}")
        else:
            print(f"Odd number: {i}")
    try:
        result = 10 / 0
    except ZeroDivisionError:
        print("Cannot divide by zero")

# A long line to test line length enforcement. This line is longer than the specified limit in some of the functions. So, it should be split into multiple lines based on the maximum line length specified.
a_very_long_variable_name_to_test_line_length_enforcement = 10

# String formatting test
name = "Alice"
age = 30
formatted_string = "My name is %s and I am %d years old." % (name, age)

# Dictionary and list test
example_dict = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3', 'key4': 'value4'}
example_list = [1, 2, 3, 4, 5]

# Tuple test
example_tuple = (1, 2, 3, 4, 5)

# Function call with various arguments
result1 = some_function(10, 5)
result2 = some_function(20, 8)

# Raw text with multiple lines
raw_text = '''
This is a raw text example.sdvasdvadfac ac a advadsvadfcasdcasdcsdasdvasdvsva sd asd dfadsc asd
It spans multiple lines csdcsadvsdvsdavavasdvasvdsdfsda fsdafsd sadfa fdh fh fdhadf d f
to test raw text handling. asd fsdfasdfdf asdf asdfdsgdfae fgdfh ad gdf gerf gerg erg ad
'''