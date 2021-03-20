import random
import sys
import pdb
import time
from terminaltables import AsciiTable
import colorama
from colorama import Fore, Style, Back
colorama.init()

DUMMY_MODEL=True
GOOD_MODEL = True
RANDOM_INPUT=False
PROMPT_USER = True
PROMP_ON_ERRORS = True
number_of_tests = 30

def model_good(a,b):
    if a < b:
        lower = a
        higher = b
    else:
        lower = b
        higher = a
    module = higher%lower
    if module == 0:
        return lower
    else:
        return model_good(lower, module)

def model_dummy(a,b):
    current_gcd = 1
    for d in range(2, min(a, b) + 1):
        if a % d == 0 and b % d == 0:
            if d > current_gcd:
                current_gcd = d
    return current_gcd

def test_model(model, _input):
    model_start = time.time()
    model_output = model(_input[0], _input[1])
    total_time = round(time.time() - model_start,2)
    return (model_output, total_time)

def check_values(first_value, second_value):
    if first_value == second_value:
        return(True,f"{Fore.GREEN}Ok!{Style.RESET_ALL}\n")
    else:
        return(False,f"{Fore.RED}BAD!{Style.RESET_ALL}\n")
 
def print_table(table_data, end):
    table = AsciiTable(table_data)
    if end:
        print(table.table+"\n")
    else:
        print(table.table)
def random_input_generator(seed, low, high):
    random.seed=seed
    return sorted([random.randint(low,high), random.randint(low,high)])
def test_presentation_and_prompt_user(test_name, additional_info = None):
    _string = f"{Style.BRIGHT}{test_name} test{Style.RESET_ALL}. "
    if additional_info:
        _string += additional_info
    _string += "\n"
    print(_string)
    if PROMPT_USER:
        choice = None
        while choice not in ['y','s']:
            choice = input("Press 'y' to continue, 's' to skip...\n")
        if choice == 'y':
            print("")
            return True
        if choice == 's':
            print("Test skipped. Press any key to continue\n")
            return False
    else:
        return True
def wait_for_input():
    if PROMPT_USER:
        input("Test finished. Press enter to continue\n")
    else:
        print("Test finished.\n")
def good_model_test(_input, test_name):
    do_the_test = test_presentation_and_prompt_user(test_name=test_name, additional_info= f"Input list: {_input}.")
    if do_the_test:
        for i, value in enumerate(_input):
            (good_output, good_time) = test_model(model_good,value)
            table_data=[["Test #", "Input", "Model", "Output", "Time"],
                        [i,value, model_good.__name__, good_output, good_time]]
            print_table(table_data, end=True)
        wait_for_input()
def stress_tests(number_of_tests, low, high):
    do_the_test = test_presentation_and_prompt_user(test_name="Stress tests", additional_info=f"{number_of_tests} tests to be performed.")
    if do_the_test:
        for i in range(number_of_tests):
            _input = random_input_generator(seed=i, low=low, high=high)
            table_data = []
            table_data.append(["Test #", "Input", "Model", "Output", "Time", "Result"])
            (good_output, good_time) = test_model(model_good, _input)
            (dummy_output, dummy_time) = test_model(model_dummy, _input)
            (_continue, result) = check_values(good_output, dummy_output)
            table_data.append([i, _input, model_good.__name__, good_output, good_time, result])
            table_data.append([i, _input, model_dummy.__name__, dummy_output, dummy_time, result])
            if i == number_of_tests:
                print_table(table_data, end=True)        
            else:
                print_table(table_data, end=False)
            if not _continue and PROMP_ON_ERRORS:
                choice = None
                while choice not in ('y','x', 'a'):
                    choice = input("Press 'y' to continue, 'a' to continue and not be asked again, 'x' to exit.\n")
                    if choice == 'x':
                        sys.exit()
                    elif choice == 'a':
                        PROMP_ON_ERRORS = False
                        continue
                    elif choice=='y':
                        break
        PROMP_ON_ERRORS = True
        wait_for_input()     



print(f"\n{Style.BRIGHT}Greatest Common Divisor Algorithm.{Style.RESET_ALL}\n")
table_data = [['Task', 'Given two integers a and b, find their greatest common divisor.'],
                ['Constraints', '1<=a,b<=2*10^9'],
                ['Output Format', 'Output the last digit of Fn'],
                ['Sample 1', 'input 18,35 output 1'],
                ['Sample 2', 'input 28851538, 1183019 output 17657']]
table = AsciiTable(table_data)
table.inner_heading_row_border = False
print(table.table+"\n")

while True:
    choice = None
    while choice not in ('1','2','3','4','5','6'):
        print("Choose an option:\n")
        print(f"{Style.BRIGHT}1{Style.RESET_ALL} Execute Sample tests - Test algorithm only")
        print(f"{Style.BRIGHT}2{Style.RESET_ALL} Execute Boundary tests - Test algorithm only")
        print(f"{Style.BRIGHT}3{Style.RESET_ALL} Execute Stress tests - Test algorithm vs 'Dummy' algorithm")
        print(f"{Style.BRIGHT}4{Style.RESET_ALL} Execute all tests with prompts")
        print(f"{Style.BRIGHT}5{Style.RESET_ALL} Execute all tests without prompts")
        print(f"{Style.BRIGHT}6{Style.RESET_ALL} Exit")
        choice = input()
        print()
    
    if choice == '1':
        good_model_test(_input=[[18,35]], test_name="Sample")
        good_model_test(_input=[[28851538,1183019]], test_name="Sample")
    elif choice == '2':
        good_model_test(_input=[[1, 526], [65456, int(1e9)], [1,int(1e9)]], test_name="Boundary")
    elif choice == '3':
        stress_tests(number_of_tests=30, low=1, high=1e4)
    elif choice == '4':
        PROMPT_USER = True
        good_model_test(_input=[[18,35]], test_name="Sample")
        good_model_test(_input=[[1, 526], [65456, int(1e9)], [1,int(1e9)]], test_name="Boundary")
        stress_tests(number_of_tests=30, low=1, high=1e4)
    elif choice == '5':
        PROMPT_USER = False
        good_model_test(_input=[[18,35]], test_name="Sample")
        good_model_test(_input=[[1, 526], [65456, int(1e9)], [1,int(1e9)]], test_name="Boundary")
        stress_tests(number_of_tests=30, low=1, high=1e4)
    elif choice == '6':
        sys.exit()