import random
import sys
import pdb
import time
from terminaltables import AsciiTable
import colorama
from colorama import Fore, Style, Back
colorama.init()


def model_good(n,module):
    seq = [0,1]
    fmod = [0,1]
    period = 2
    for i in range(1,n):
        seq.append(seq[i]+seq[i-1])
        fmod.append(seq[-1]%module)
        period +=1
        if fmod[-2] == 0 and fmod[-1] == 1:
            fmod = fmod[:-2]
            break
    rest = n%(len(fmod))
    return(fmod[rest])
    

def model_dummy(n,module):
    if n <= 1:
         return n

    previous = 0
    current  = 1

    for _ in range(n - 1):
        previous,current = current, previous + current
    return current % module

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
def random_input_generator(seed, values):
    random.seed=seed
    _list = []
    for val in values:
        _list.append(random.randint(val[0], val[1]))
    return _list



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
def wait_for_input_after_error():
    global PROMP_ON_ERRORS
    if PROMP_ON_ERRORS:
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



def good_model_test(_input, test_name, known_result=False):
    do_the_test = test_presentation_and_prompt_user(test_name=test_name, additional_info= f"Input list: {_input}.")
    if do_the_test:
        for i, value in enumerate(_input):
            (good_output, good_time) = test_model(model_good,value)
            result = None
            matches = True
            #pdb.set_trace()
            if known_result != False:
                (matches,result) = check_values(good_output, known_result)
            else:
                result = 'Unknown'
            table_data=[["Test #", "Input", "Model", "Output", "Time", "Result"],
                        [i,value, model_good.__name__, good_output, good_time, result]]
            print_table(table_data, end=True)
            if not matches:
                wait_for_input_after_error()
        wait_for_input()
def stress_tests(number_of_tests, values):
    do_the_test = test_presentation_and_prompt_user(test_name="Stress tests", additional_info=f"{number_of_tests} tests to be performed.")
    if do_the_test:
        for i in range(number_of_tests):
            _input = random_input_generator(seed=i, values=values)
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
            if not _continue:
                wait_for_input_after_error()
        PROMP_ON_ERRORS = True
        wait_for_input()     


DUMMY_MODEL=True
GOOD_MODEL = True
RANDOM_INPUT=False
PROMPT_USER = True
PROMP_ON_ERRORS = True
number_of_tests = 30
sample_input_1=[239,1000]
sample_output_1 = 161
sample_input_2=[2816213588,239]
sample_output_2 = 151
boundary_input=[[1,int(1e14)], [2,1000]]
stress_tests_boundary = [[1,int(1e5)], [2,1000]]

print(f"\n{Style.BRIGHT}Fibonacci module for huge Fibonacci numbers Algorithm.{Style.RESET_ALL}\n")
table_data = [['Task', 'Given two integersn and m, output Fn mod m (that is, the remainder of Fn when divided by m).'],
                ['Constraints', f'{boundary_input[0][0]}<=n<={boundary_input[0][1]}, {boundary_input[1][0]}<=m<={boundary_input[1][1]}'],
                ['Output Format', 'Output Fn mod m'],
                ['Sample 1', f'input {sample_input_1[0]}, {sample_input_1[1]} output {sample_output_1}'],
                ['Sample 2', f'input {sample_input_2[0]}, {sample_input_2[1]} output {sample_output_2}']]
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
        good_model_test(_input=[sample_input_1], test_name="Sample", known_result=sample_output_1)
        good_model_test(_input=[sample_input_2], test_name="Sample", known_result=sample_output_2)
    elif choice == '2':
        good_model_test(_input=[[1, 2], [1, 534], [1, 1000], [int(1e14), 2], [int(1e14), 234], [int(1e14), 1000], [int(1e7), 2], [int(1e7), 1000]], test_name="Boundary")
    elif choice == '3':
        stress_tests(number_of_tests=number_of_tests, values=stress_tests_boundary)
    elif choice == '4':
        PROMPT_USER = True
        good_model_test(_input=[sample_input_1], test_name="Sample", known_result=sample_output_1)
        good_model_test(_input=[sample_input_2], test_name="Sample", known_result=sample_output_2)
        good_model_test(_input=[[1, 2], [1, 534], [1, 1000], [int(1e14), 2], [int(1e14), 234], [int(1e14), 1000], [int(1e7), 2], [int(1e7), 1000]], test_name="Boundary")   
        stress_tests(number_of_tests=number_of_tests, values=stress_tests_boundary)
    elif choice == '5':
        PROMPT_USER = False
        good_model_test(_input=[sample_input_1], test_name="Sample", known_result=sample_output_1)
        good_model_test(_input=[sample_input_2], test_name="Sample", known_result=sample_output_2)
        good_model_test(_input=[[1, 2], [1, 534], [1, 1000], [int(1e14), 2], [int(1e14), 234], [int(1e14), 1000], [int(1e7), 2], [int(1e7), 1000]], test_name="Boundary")
        stress_tests(number_of_tests=number_of_tests, values=stress_tests_boundary)
    elif choice == '6':
        sys.exit()