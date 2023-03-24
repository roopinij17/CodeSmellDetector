import re

#common pattern to check for a c++ file
pattern = r"^\s*(\w+)\s+(\w+)\s*\((.*)\)\s*({)?\n([\s\S]*?)\n(})?\s*$"


def read_file_contents(file_name):
    #function to read the file
    with open(file_name, 'r') as f:
        file_contents = f.read().split("\n")
        file_contents_remove_white_lines = [x for x in file_contents if x]
        file_contents = "\n".join(file_contents_remove_white_lines)
    return file_contents


def find_all(file_name):
    #checks the pattern using findall
    matches = re.findall(pattern,read_file_contents(file_name), re.MULTILINE)
    return matches


def find_iter(file_name):
    #checks the pattern using finditer
    matches = re.finditer(pattern,read_file_contents(file_name), re.MULTILINE)
    return matches


def print_function(file_name):
    # prints the function names.
    matches = find_all(file_name)
    for match in matches:
        if match[1]:
            print("Function:", match[1])


def detect_long_method(file_name):
    # prints the long method present in the test file.
    matches = find_all(file_name)
    long_method_functions = []
    for match in matches:
        function_name: object = match[1]
        function_code = match[4].strip()
        lines_of_code = sum(1 for line in function_code.split('\n') if line.strip() != '') + 2  #to include the function signature and body
        if lines_of_code > 15:
            long_method_functions.append(function_name)

    if len(long_method_functions) == 0:
        print("Great! No Methods are longer in your code. ")
    else:
        print("The {} function is a Long method. It has {} lines of code".format(function_name,lines_of_code))


def detect_long_parameter(file_name):
    # print the parameter of the functions.
    matches = find_all(file_name)
    long_parameter_functions = {}
    for match in matches:
        function_name = match[1]
        parameters = match[2]
        if (len(parameters.split(',')) > 3):
            long_parameter_functions[len(long_parameter_functions)] = [function_name, parameters]

    if len(long_parameter_functions) == 0:
        print("Great! No Parameters are longer in your code. ")
    else:
        for k, v in long_parameter_functions.items():
            print("{} has a Long Parameter List. Its parameter list contains {} parameters".format(v[0], len(v[1].split(","))))


def jaccard_similarity(str1, str2):
    #jaccard similarity formula
    set1 = set(str1.split())
    set2 = set(str2.split())
    return len(set1.intersection(set2)) / len(set1.union(set2))


def detect_duplicate_functions(file_name):
    #print the duplicate code.
    matches = find_iter(file_name)
    functions = []
    for match in matches:
        function_name = match[2]
        function_signature = match[0]
        function_body = match[5].strip()
        function_definition = f"{function_signature}\n{function_body}"
        functions.append((function_name, function_definition))

    found_similarity = False
    for i in range(len(functions)):
        for j in range(i + 1, len(functions)):
            similarity = jaccard_similarity(functions[i][1], functions[j][1])
            if similarity > 0.75:
                found_similarity = True
                print(f"{functions[i][0]} and {functions[j][0]} are duplicate functions with a jaccard similarity of {similarity}")
    if not found_similarity:
        print("Great No duplicate functions")


file_name = input("Enter the filename:")

welcome_message = """
Welcome to Code Smell Detection!
The file you input contains the following methods/functions: 
"""
print(welcome_message)
print_function(file_name)

user_prompt = """
_______________________________________________________________________
Please choose what you want to do now:
1. Detect long method/function
2. Detect long parameter list
3. Detect duplicated code
4. Quit
Enter your choice (1/2/3/4): """
user_input = ""


while user_input != '4':
    user_input = str(input(user_prompt))
    if str(user_input) not in ['1', '2', '3', '4']:
        print("Input entered is not in the given choices. Please try again.")
    else:
        if str(user_input) == '1':
            detect_long_method(file_name)
        elif str(user_input) == '2':
            detect_long_parameter(file_name)
        elif str(user_input) == '3':
            detect_duplicate_functions(file_name)

exit_prompt = """
You chose 4, Exiting! Thanks for using Code Smell Detector!
_______________________________________________________________________
"""


print(exit_prompt)