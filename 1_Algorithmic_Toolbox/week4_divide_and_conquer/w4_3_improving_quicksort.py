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


def model_good(a, left, right, debug=False):
    if debug: print(f"Model good! Input: {a}. initial left: {left}, right: {right}")
    def recursive_part(left, right):
        if debug: print(f"\nRecursive call! left: {left} - right: {right}")
        if left == right:
            if debug: print(f"Left: {left} == Right: {right}. Returning -1")
            return -1
        if left + 1 == right:
            if debug: print(f"Base case. Only one element in the array. Return it: {a[left]}")
            return a[left]
        mid_index = (left + right)//2
        if debug: print(f"Mid index: {mid_index}")
        first = recursive_part(left, mid_index)
        if debug: print(f"Just past the first variable: {first}")
        second = recursive_part(mid_index, right)
        #Si el valor de la izquierda es igual al valor de la derecha devuélvelo
        if debug: print(f"First and second values: {first} - {second}")
        if first == second: 
            if debug: print(f"Same values. Returning {first}\n")
            return first
        # si no cuenta cada elemento y devuelve el que aparezca más.
        if a[left:right+1].count(first) > a[left:right].count(second):
            if debug: print(f"First {first} appears more times than second in fraction {a[left:right]}. Returning first\n")
            return first
        elif a[left:right+1].count(first) < a[left:right].count(second):
            if debug: print(f"Second {second} appears more times than first in fraction {a[left:right]}. Returning second\n")
            return second
        else:
            if debug: print(f"No winner!\n")
            return -1
    candidate = recursive_part(left, right)
    if a[left:right].count(candidate) > len(a)//2:
        if debug: print(f"Candidate solution: {candidate} actualy appears more than 1/2 of the times\n")
        return candidate
    else:
        if debug: print(f"Candidate {candidate} solution is not good.\n")
        return -1
    return recursive_part(left, right)
    #write your code here
    #PAra todos los demás casos (longitud de array >1)
    #Coger el índice del medio
    #Dos llamadas recursivas partiendo el array a la mitad. Guardar los valores devueltos.

    return -1

def model_dummy(a, left, right, debug=False):
    for element in a:
        if a.count(element) > len(a)/2:
            return element
    return -1

def model_test(a, left, right, debug=False):
    if debug: print(f"Input: {a}")
    for i in range(0,len(a)):
        current_element = a[i]
        count = 0
        for j in range(0, len(a)):
            if a[j] == current_element:
                count += 1
        if debug: print(f"Total count for element {a[i]} at position {i} is: {count}\n")
        if count > len(a)/2:
            return a[i]
    return -1



if __name__ == '__main__':
    input = sys.stdin.read()
    n, *a = list(map(int, input.split()))
    if model_good(a, 0, n) != -1:
        print(1)
    else:
        print(0)

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
        
        model_output.append(model(a=model_input[0],left=0,right=len(model_input[0]),debug=DEBUG))
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
        for i in range(0, values[0]):
            array.append(random.randint(0, values[1]))
        random_value_in_array = array[random.randint(0, len(array)-1)]
        array = [random_value_in_array if random.randint(0,1) == 1 else value for value in array]
        return [array]
        
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
    number_of_tests = 10
    sample_input_1=[[2,3,9,2,2]]
    sample_output_1 = [1]
    sample_1_text = ''
    sample_input_2=[[1,2,3,4]]
    sample_output_2 = [-1]
    sample_2_text = ''
    sample_input_3=[[1,2,3,1]]
    sample_output_3 = [-1]
    sample_3_text = ''

    stress_tests_boundary = [10000,100]
    # 10 numeros tendra el array
    # 10 valor máximo (el mínimo es 0)
    decimal_preccision = 4

    print(f"\n{Style.BRIGHT}Majority Element Algorithm.{Style.RESET_ALL}\n")
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
            good_model_test(_input=[sample_input_3], test_name="Sample", known_result=sample_output_3)

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


