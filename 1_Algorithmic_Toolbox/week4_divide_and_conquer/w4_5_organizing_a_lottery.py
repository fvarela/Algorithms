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
   

def model_good(starts, ends, points, debug=False):
    if debug: print(f"model_good. starts:{starts} ends:{ends} points:{points} ")

    all_elements = []
    all_elements=[[x,'l'] for x in starts]
    [all_elements.append([x,'p']) for x in points]
    [all_elements.append([x,'r']) for x in ends]

    cnt = []

    open_intervals = 0
    if debug: print(f"all_elements: {all_elements}")
    #Randomized quick sort
    def randomized_quick_sort(start, end):
        #Base case. Length 1 just return dummy value 0:
        if debug: print(f"all_elements:{all_elements} start:{start} end:{end}")
        if start >= end:
            return 0
        pivot_index = random.randint(start,end-1)
        if debug: print(f"pivot_index:{pivot_index}")
        all_elements[start], all_elements[pivot_index] = all_elements[pivot_index], all_elements[start]
        if debug: print(f"all_elements swapped:{all_elements}")
        i = start+1
        for j in range(start+1,end):
            swapp = False
            if debug: print(f"Iteration {j}. Comparing {all_elements[j]} with {all_elements[start]}")
            if all_elements[j][0] < all_elements[start][0]:
                swapp = True
            elif all_elements[j][0] == all_elements[start][0]:
                if all_elements[j][1]<all_elements[start][1]:
                    swapp=True
            if swapp:
                if debug: print(f"Swapping {all_elements[j]} with {all_elements[i]}")
                all_elements[j], all_elements[i] = all_elements[i], all_elements[j]
                if debug: print(f"all_elements after:{all_elements}")
                i+=1
        all_elements[start], all_elements[i-1] = all_elements[i-1], all_elements[start]
        randomized_quick_sort(start, i-1)
        randomized_quick_sort(i, end)
    randomized_quick_sort(0,len(all_elements))   
    # all_elements.sort()
    results = {}
    
    for array in all_elements:
        if array[1]=='l': open_intervals+=1
        elif array[1]=='r': open_intervals-=1
        elif array[1]=='p': 
            results[array[0]] = open_intervals
    if debug: print(f"Last array: {array}. results: {results}. cnt:{cnt}")
    for i in range(len(points)):
        cnt.append(str(results[points[i]]))
    if debug: print(f"Returning: {cnt}")
    return cnt

def model_dummy(starts, ends, points, debug=False):
    if debug: print(f"model_good. starts:{starts} ends:{ends} points:{points} ")

    all_elements = []
    all_elements=[[x,'l'] for x in starts]
    [all_elements.append([x,'p']) for x in points]
    [all_elements.append([x,'r']) for x in ends]

    cnt = []

    open_intervals = 0
    if debug: print(f"all_elements: {all_elements}")
    all_elements.sort()
    results = {}
    
    for array in all_elements:
        if array[1]=='l': open_intervals+=1
        elif array[1]=='r': open_intervals-=1
        elif array[1]=='p': 
            results[array[0]] = open_intervals
    if debug: print(f"Last array: {array}. results: {results}. cnt:{cnt}")
    for i in range(len(points)):
        cnt.append(str(results[points[i]]))
    if debug: print(f"Returning: {cnt}")
    return cnt

def model_dummy2(starts, ends, points, debug=False):
    if debug: print(f"Model dummy input: starts:{starts} ends:{ends} points:{points}")
    cnt = [0] * len(points)
    for i in range(len(points)):
        for j in range(len(starts)):
            if starts[j] <= points[i] <= ends[j]:
                cnt[i] += 1
    return cnt


if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n = data[0] #number of segments
    m = data[1] #number of points
    starts = data[2:2 * n + 2:2]
    ends   = data[3:2 * n + 2:2]
    points = data[2 * n + 2:]
    #use fast_count_segments
    cnt = model_good(starts, ends, points)
    for x in cnt:
        print(x, end=' ')

else:
    import random
    import pdb
    import time
    from terminaltables import AsciiTable
    import colorama
    from colorama import Fore, Style, Back
    colorama.init()

    def test_model(model, data):

        # Model dummy input: starts:[0, 7] ends:[5, 10] points:[1, 6, 11]

        model_start = time.time()
        model_output=[]
        n = data[0]

        starts = data[2:2 * n + 2:2]
        ends   = data[3:2 * n + 2:2]
        points = data[2 * n + 2:]
        model_output = model(starts, ends, points, debug=DEBUG)
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
    def good_model_test(_input, test_name, test_number=0, known_result=False):
        do_the_test = test_presentation_and_prompt_user(test_name=test_name, additional_info= f"Input list: {_input}.")
        if do_the_test:
            (good_output, good_time) = test_model(model_good if not ONLY_DUMMY else model_dummy, _input)
            result = None
            matches = True
            if known_result is not False:
                (matches,result) = check_values(good_output, known_result)
            else:
                result = 'Unknown'
            table_data=[["Test #", "Input", "Model", "Output", "Time", "Result"],
                        [test_number,_input, model_good.__name__ if not ONLY_DUMMY else model_dummy.__name__, good_output , good_time, result]]
            print_table(table_data, end=True)
            if not matches:
                pdb.set_trace()
                wait_for_input_after_error()
            wait_for_input()
    def stress_tests(number_of_tests, boundaries):
        def random_input_generator(seed, boundaries):
            number_of_points = random.randint(1,5e4)
            number_of_intervals = random.randint(1,5e4)
            array = [number_of_intervals, number_of_points]
            for _ in range(number_of_intervals):
                first_number = random.randint(boundaries[0], boundaries[1]-1)
                second_number = random.randint(first_number, boundaries[1])
                array.append(first_number)
                array.append(second_number)
            for _ in range(number_of_points):
                array.append(random.randint(boundaries[0], boundaries[1]))

            return array

        global PROMP_ON_ERRORS
        do_the_test = test_presentation_and_prompt_user(test_name="Stress tests", additional_info=f"{number_of_tests} tests to be performed.")
        if do_the_test:
            for i in range(number_of_tests):
                _input = random_input_generator(seed=i, boundaries=boundaries) if RANDOM_INPUT else [i]
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
    STRESS = True

    RANDOM_INPUT=True
    PROMPT_USER = True
    PROMP_ON_ERRORS = True
    number_of_tests = 2000

    sample_input_1=[1, 1, int(1e-8), int(1e8), 0]
    sample_output_1 = ['1']
    sample_1_text = ''
    sample_input_2=[1,1,-100,100,int(1e8)]
    sample_output_2 = ['0']
    sample_2_text = ''
    sample_input_3=[3,2,0,5,-3,2,7,10,1,6]
    sample_output_3 = ['2','0']
    sample_3_text = ''


    stress_tests_boundary = [int(-1e8),int(1e8)]
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
            good_model_test(_input=sample_input_1, test_name="Sample", test_number=1, known_result=sample_output_1)
            good_model_test(_input=sample_input_2, test_name="Sample", test_number=2, known_result=sample_output_2)
            good_model_test(_input=sample_input_3, test_name="Sample", test_number=3, known_result=sample_output_3)
        elif choice == 'b':
            good_model_test(_input=[[1]], test_name="Boundary")
            good_model_test(_input=[[1e3]], test_name="Boundary")
        elif choice == 't':
            stress_tests(number_of_tests=number_of_tests, boundaries=stress_tests_boundary)
        elif choice == 'a':
            PROMPT_USER = False
            if SAMPLE: 
                good_model_test(_input=sample_input_1, test_name="Sample", test_number=1, known_result=sample_output_1)
                good_model_test(_input=sample_input_2, test_name="Sample", test_number=2, known_result=sample_output_2)
                good_model_test(_input=sample_input_3, test_name="Sample", test_number=3, known_result=sample_output_3)
            if BOUNDARY: 
                good_model_test(_input=[[1]], test_name="Boundary")
                good_model_test(_input=[[1e3]], test_name="Boundary")
            if STRESS:
                stress_tests(number_of_tests=number_of_tests, boundaries=stress_tests_boundary)

        elif choice == 'x':
            sys.exit()


