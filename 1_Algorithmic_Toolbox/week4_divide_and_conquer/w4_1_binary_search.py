import sys
import pdb
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s:%(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
if __name__ != '__main':
    logger.addHandler(stream_handler)


def model_good(a, x, debug=False):
    def binary_search(a, low, high, key):
        
        if debug: print(f"Binary search input: A: {a} - x: {x}. Between indexes {low} and {high}\n")
        mid = (high+low)//2
        if low > high:
            return -1
        elif a[mid] == x:
            if debug: print(f"Value {x} found at position {mid}\n")
            return mid
        elif a[mid]<x:
            if debug: print(f"Value in the middle: {a[mid]} is smaller than {x}. Recursive call with the right size of the array: {a[mid+1:]}\n")
            return binary_search(a=a, low=mid+1, high=high, key=x)
        elif a[mid]>x:
            if debug: print(f"Value in the middle: {a[mid]} is greater than {x}. Recursive call with the left size of the array: {a[:mid]}\n")
            return binary_search(a=a, low=low, high=mid-1, key=x)
    left, right = 0, len(a)-1
    return binary_search(a=a, low=left, high=right, key=x)



def model_dummy(a,x, debug=False):
    #Linear search
    if debug: print(f"Linear model input: {a}, {x}\n")
    for i in range(len(a)):
        if a[i] == x:
            return i
    return -1



if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n = data[0]
    m = data[n + 1]
    a = data[1 : n + 1]
    for x in data[n + 2:]:
        # replace with the call to binary_search when implemented
        print(model_good(a, x), end = ' ')


else:
    import random
    import pdb
    import time
    from terminaltables import AsciiTable
    import colorama
    from colorama import Fore, Style, Back
    colorama.init()

    def test_model(model, model_input):
        model_start = time.time()
        model_output=[]
        for value in model_input[1]:
            model_output.append(model(model_input[0], value,debug=DEBUG))
        total_time = round(time.time() - model_start,2)
        if type(model_output) is float:
            model_output = round(model_output, decimal_preccision)
        return (model_output, total_time)

    def check_values(first_value, second_value):
        if type(first_value) is float:
            first_value = round(first_value, decimal_preccision)
        if type(second_value) is float:
            second_value = round(second_value, decimal_preccision)
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
        array = []
        for i in range(0, random.randint(values[1][0], values[1][1])):
            array.append(random.randint(values[2][0], values[2][1]))
        #Number of items to search
        values_to_search = []
        for i in range(0, random.randint(values[0][0], values[0][1])):
            if random.randint(1,10) >5:
                random_index = random.randint(0, len(array)-1)
                values_to_search.append(array[random_index])
            else:
                values_to_search.append(random.randint(values[2][0],values[2][1]))
        return [sorted(array), values_to_search]
        
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
                (good_output, good_time) = test_model(model_good, value.copy())
                result = None
                matches = True
                if known_result is not False:
                    (matches,result) = check_values(good_output, known_result)
                else:
                    result = 'Unknown'
                table_data=[["Test #", "Input", "Model", "Output", "Time", "Result"],
                            [i,value, model_good.__name__, good_output , good_time, result]]
                print_table(table_data, end=True)
                if not matches:
                    pdb.set_trace()
                    wait_for_input_after_error()
            wait_for_input()
    def stress_tests(number_of_tests, values):
        global PROMP_ON_ERRORS
        do_the_test = test_presentation_and_prompt_user(test_name="Stress tests", additional_info=f"{number_of_tests} tests to be performed.")
        if do_the_test:
            for i in range(number_of_tests):
                _input = random_input_generator(seed=i, values=values) if RANDOM_INPUT else [i]
                table_data = []
                table_data.append(["Test #", "Input", "Model", "Output", "Time", "Result"])
                (good_output, good_time) = test_model(model_good, _input)
                (dummy_output, dummy_time) = test_model(model_dummy, _input)
                (_continue, result) = check_values(good_output, dummy_output)
                if len(_input.__str__())>40:
                    _input = _input.__str__()[0:40] + '...'
                if len(good_output.__str__())>40:
                    good_output = good_output.__str__()[0:4] + '...'
                if len(dummy_output.__str__())>40:
                    dummy_output = dummy_output.__str__()[0:40] + '...'
                if result and len(result.__str__())>40:
                    result = result.__str__()[0:40] + '...'

            
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
    DEBUG = False

    SAMPLE = True
    BOUNDARY = False
    STRESS = True

    RANDOM_INPUT=True
    PROMPT_USER = True
    PROMP_ON_ERRORS = True
    number_of_tests = 1000
    sample_input_1=[[1,5,8,12,13], [8,1,23,1,11]]
    sample_output_1 = [2, 0, -1, 0, -1]
    sample_1_text = ''
    sample_input_2=[[1,5,8,12,13], [8,1,23,1,11,13]]
    sample_output_2 = [2, 0, -1, 0, -1, 4]
    sample_1_text = ''

    stress_tests_boundary = [[1,10], [1,10], [1, 10]]
    # [1,int(1e5)] Numero de valores que hay que buscar en el array
    # [1,int(3e4)] Numero de valores que tiene el array
    # [1,int(3e9)] Valores de array y valores que hay que buscar
    decimal_preccision = 4

    print(f"\n{Style.BRIGHT}Binary Search Algorithm.{Style.RESET_ALL}\n")
    choices = []
    if SAMPLE: choices.append('s')
    if BOUNDARY: choices.append('b')
    if STRESS: choices.append('t')
    if len(choices) >1: 
        choices.append('a')
    choices.append('x')
    while True:
        choice = None
        while choice not in choices:
            print("Choose an option:\n")
            if SAMPLE: print(f"{Style.BRIGHT}s{Style.RESET_ALL} Execute Sample tests - Test algorithm only")
            if BOUNDARY: print(f"{Style.BRIGHT}b{Style.RESET_ALL} Execute Boundary tests - Test algorithm only")
            if STRESS: print(f"{Style.BRIGHT}t{Style.RESET_ALL} Execute Stress tests - Test algorithm vs 'Dummy' algorithm")
            if 'a' in choices: print(f"{Style.BRIGHT}a{Style.RESET_ALL} Execute all tests without prompts")
            print(f"{Style.BRIGHT}x{Style.RESET_ALL} Exit")
            choice = input()
            print()
            
        if choice == 's':
            good_model_test(_input=[sample_input_1], test_name="Sample", known_result=sample_output_1)
            good_model_test(_input=[sample_input_2], test_name="Sample", known_result=sample_output_2)

        elif choice == 'b':
            good_model_test(_input=[[1]], test_name="Boundary")
            good_model_test(_input=[[1e3]], test_name="Boundary")
        elif choice == 't':
            stress_tests(number_of_tests=number_of_tests, values=stress_tests_boundary)
        elif choice == 'a':
            PROMPT_USER = False
            if SAMPLE: good_model_test(_input=[sample_input_1], test_name="Sample", known_result=sample_output_1)
            if BOUNDARY: 
                good_model_test(_input=[[1]], test_name="Boundary")
                good_model_test(_input=[[1e3]], test_name="Boundary")
            if STRESS:
                stress_tests(number_of_tests=number_of_tests, values=stress_tests_boundary)

        elif choice == 'x':
            sys.exit()


