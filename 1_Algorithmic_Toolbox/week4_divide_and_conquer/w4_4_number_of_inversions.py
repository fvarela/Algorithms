import sys
import pdb
import logging
import random

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s:%(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
if __name__ != '__main':
    logger.addHandler(stream_handler)
   

def model_good(a, b, left, right, debug=False):
    if debug: print(f"\nModel good: a:{a}, b:{b}, left:{left}, right:{right}")
    number_of_inversions = 0
    if right - left <= 1:
        return number_of_inversions
    ave = (left + right) // 2
    number_of_inversions += model_good(a, b, left, ave, debug=debug)
    number_of_inversions += model_good(a, b, ave, right, debug=debug)
    
    if debug: print(f"After recursions. left:{left}, right:{right}")
    #write your code here
    
    middle_index = (left + right)//2
    left_array = a[left:middle_index]
    right_array = a[middle_index:right]
    i=j=0
    k=left
    if debug: print(f"\tleft_array:{left_array}. right_array:{right_array}. Iterating on left array elements")
    for i in range(0, len(left_array)):
        if debug: print(f"\t\tFirst loop. indexes: i:{i}, j{j}, k:{k}. Array a:{a}")
        for w in range(0,len(right_array)):
            if right_array[w]<left_array[i]:
                if debug: print(f"\t\tNEW INVERSION right_array value at index {w} is {right_array[w]}, less than left array at index {i}: {left_array[i]}")
                number_of_inversions += 1

        if j < len(right_array):
            # print(f"Accediendo a right_array: {right_array} con índice {j}")
            while right_array[j]<left_array[i]:
                if debug: print(f"\t\tRight array value index j:{j} -> {right_array[j]} is less than left array value index i:{i} -> {left_array[i]}")
                a[k] = right_array[j]
                j+=1
                k+=1
                if j == len(right_array):
                    break
        a[k] = left_array[i]
        i+=1
        k+=1
    if debug: print(f"\ta after main loop {a}")
    while j!=len(right_array):
        if debug: print(f"\t\tSecond loop. Adding remaining element right_array[j]: {right_array[j]} from right_array to a at position k:{k}")
        a[k] = right_array[j]
        j+=1
        k+=1
    # b= [a[i] for i in range(0, len(a)) if a[i]!=0]
    if debug: print(f"\ta after secondary loop: {a}")
    if debug: print(f"\tReturning inversions_in_this_iteration: {number_of_inversions}")
    return number_of_inversions

def model_dummy(a, b, left, right, debug=False):
    print(f"Model dummy: a:{a}, b:{b}, left:{left}, right:{right}")
    number_of_inversions = 0
    if right - left <= 1:
        return number_of_inversions
    ave = (left + right) // 2
    number_of_inversions += model_dummy(a, b, left, ave)
    number_of_inversions += model_dummy(a, b, ave, right)
    #write your code here
    pdb.set_trace()
    return number_of_inversions


if __name__ == '__main__':
    input = sys.stdin.read()
    n, *a = list(map(int, input.split()))
    b = n * [0]
    #print(f"Parameters: n:{n}, a:{a}, b:{b}")
    print(model_good(a, b, 0, len(a)))

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
        _input = model_input[0].copy()
        model_output.append(model(a=_input,b=len(_input)*[0],left=0,right=len(_input), debug=DEBUG))
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
        for _ in range(0, values[0]):
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
                (good_output, good_time) = test_model(model_good if not ONLY_DUMMY else model_dummy, value.copy())
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
                    good_output = good_output.__str__()[0:40] + '...'
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

    ONLY_DUMMY = False

    SAMPLE = True
    BOUNDARY = False
    STRESS = False

    RANDOM_INPUT=True
    PROMPT_USER = True
    PROMP_ON_ERRORS = True
    number_of_tests = 500

    sample_input_1=[[3,1,5,7,2,3]]
    sample_output_1 = [6]
    sample_1_text = ''
    sample_input_2=[[1,2]]
    sample_output_2 = [0]
    sample_2_text = ''
    sample_input_3=[[2,1,1]]
    sample_output_3 = [2]
    sample_3_text = ''
    sample_input_4=[[3,1,5,7,2,3,5]]
    sample_output_4 = [7]
    sample_4_text = ''
    sample_input_4=[[8,1,4,9,2,5,3,7,4,6]]
    sample_output_4 = [20]
    sample_4_text = ''


    stress_tests_boundary = [1000,500]
    # 10 numeros tendra el array
    # 10 valor máximo (el mínimo es 0)
    decimal_preccision = 4

    print(f"\n{Style.BRIGHT}Number of Inversions Algorithm.{Style.RESET_ALL}\n")
    choices = []
    if SAMPLE: choices.append('s')
    if BOUNDARY: choices.append('b')
    if STRESS: choices.append('t')
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
            good_model_test(_input=[sample_input_4], test_name="Sample", known_result=sample_output_4)
        elif choice == 'b':
            good_model_test(_input=[[1]], test_name="Boundary")
            good_model_test(_input=[[1e3]], test_name="Boundary")
        elif choice == 't':
            stress_tests(number_of_tests=number_of_tests, values=stress_tests_boundary)
        elif choice == 'a':
            PROMPT_USER = False
            if SAMPLE: 
                good_model_test(_input=[sample_input_1], test_name="Sample", known_result=sample_output_1)
                good_model_test(_input=[sample_input_2], test_name="Sample", known_result=sample_output_2)
                good_model_test(_input=[sample_input_3], test_name="Sample", known_result=sample_output_3)
                good_model_test(_input=[sample_input_4], test_name="Sample", known_result=sample_output_4)
            if BOUNDARY: 
                good_model_test(_input=[[1]], test_name="Boundary")
                good_model_test(_input=[[1e3]], test_name="Boundary")
            if STRESS:
                stress_tests(number_of_tests=number_of_tests, values=stress_tests_boundary)

        elif choice == 'x':
            sys.exit()


