import sys
from collections import namedtuple
import pdb
Segment = namedtuple('Segment', 'start end')

def model_good(segments, debug=False):
    pdb.set_trace()
    segments = sorted(segments, key=lambda x: x[0])
    points = []
    for i, main_seg in enumerate(segments):
        segment_covered[0 for i in range(len(segments))]
        segment_covered[i] = 1
        current_point = main_seg[0]

        for j, other_seg in enumerate(segments, start=i+1):
            if other_seg[0] < main_seg[1]:
                dismiss = False
                for k, cov in enumerate(segment_covered):
                    if cov == 1:
                        if segments[k][1] < other_seg[0]:
                            #No hay solapamiento con un segmento que antes sí solapaba
                            #Salir del for interno
                            dismiss = True
                            break
                if not dismiss:
                    segment_covered[j] = 1
                    current_point = other_seg[0]
            

    #write your code here
    for s in segments:
        points.append(s.start)
        points.append(s.end)
    if debug: 
        print(len(points))
        print(*points)
    return points
            


def model_dummy(capacity, weights, values, debug=False):
    return -1

if __name__ == '__main__':
    input = sys.stdin.read()
    n, *data = map(int, input.split())
    segments = list(map(lambda x: Segment(x[0], x[1]), zip(data[::2], data[1::2])))
    points = model_good(segments)
    print(len(points))
    print(*points)

else:
    import random
    import pdb
    import time
    from terminaltables import AsciiTable
    import colorama
    from colorama import Fore, Style, Back
    colorama.init()

    def test_model(model, _input):
        model_start = time.time()
        model_output = model(_input[1],debug=DEBUG)
        total_time = round(time.time() - model_start,2)
        return (round(model_output, decimal_preccision), total_time)
    def check_values(first_value, second_value):
        if round(first_value,decimal_preccision) == round(second_value,decimal_preccision):
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
                if known_result is not False:
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
                _input = random_input_generator(seed=i, values=values) if RANDOM_INPUT else [i]
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
    DEBUG = True
    DUMMY_MODEL=False
    GOOD_MODEL = True
    RANDOM_INPUT=True
    PROMPT_USER = True
    PROMP_ON_ERRORS = True
    number_of_tests = 1000
    sample_input_1=[[3],[[1,3], [2,5], [3,6]]]
    sample_output_1 = 897
    sample_1_text = '897=23*39'
    sample_input_2=[[4],[[4,7],[1,3],[2,5],[5,6]]]
    sample_output_2 = 23
    sample_2_text = '23=3*4+1*1+(-5)*(-2)'
    stress_tests_boundary = [[0,int(1e3)]]
    decimal_preccision = 4

    print(f"\n{Style.BRIGHT}Collecting Signatures Algorithm.{Style.RESET_ALL}\n")

    while True:
        choice = None
        while choice not in ('s','b','t','a','x'):
            print("Choose an option:\n")
            print(f"{Style.BRIGHT}s{Style.RESET_ALL} Execute Sample tests - Test algorithm only")
            print(f"{Style.BRIGHT}b{Style.RESET_ALL} Execute Boundary tests - Test algorithm only")
            if DUMMY_MODEL:
                print(f"{Style.BRIGHT}t{Style.RESET_ALL} Execute Stress tests - Test algorithm vs 'Dummy' algorithm")
            print(f"{Style.BRIGHT}a{Style.RESET_ALL} Execute all tests without prompts")
            print(f"{Style.BRIGHT}x{Style.RESET_ALL} Exit")
            choice = input()
            print()
            
        if choice == 's':
            good_model_test(_input=[sample_input_1], test_name="Sample", known_result=sample_output_1)
            good_model_test(_input=[sample_input_2], test_name="Sample", known_result=sample_output_2)
        elif choice == 'b':
            
            good_model_test(_input=[[[1],[400],[1],[0.1]]], test_name="Boundary")
            good_model_test(_input=[[[int(1e5)],[400],[4],[200, 375, 550, 750]]], test_name="Boundary") 
            good_model_test(_input=[[[5],[1],[4],[1, 2, 3, 4]]], test_name="Boundary") 
        elif choice == 't' and DUMMY_MODEL:
            stress_tests(number_of_tests=number_of_tests, values=stress_tests_boundary)
        elif choice == 'a':
            PROMPT_USER = False
            good_model_test(_input=[sample_input_1], test_name="Sample", known_result=sample_output_1)
            good_model_test(_input=[sample_input_2], test_name="Sample", known_result=sample_output_2)
            good_model_test(_input=[[[1,0],[[1],[0]]]], test_name="Boundary")
            good_model_test(_input=[[[3,int(2e6)],[[1,int(2e6),300],[0,int(2e6),300]]]], test_name="Boundary") 
            good_model_test(_input=[[[3,int(2e6)],[[1,100,200],[0,50,75]]]], test_name="Boundary") 
            if DUMMY_MODEL:
                stress_tests(number_of_tests=number_of_tests, values=stress_tests_boundary)

        elif choice == 'x':
            sys.exit()


