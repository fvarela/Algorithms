import sys
from collections import namedtuple
import pdb
Segment = namedtuple('Segment', 'start end')

def model_good(segments, debug=False):
    segments = sorted(segments, key=lambda x: x[0])
    if debug: print(f"Segments sorted by its first index:\n{segments}")

    segments_covered = [0]*len(segments)
    if debug: print(f"Initialize segments_covered to an array of zeroes:\n{segments_covered}")
    
    points = []
    if debug: print(f"Start looping the segmentes.")
    
    for i, main_seg in enumerate(segments):
        if debug: print(f"Main loop. Index {i}. Segment: {main_seg}")
    
        if segments_covered[i] == 0:
            if debug: print(f"Segment: {main_seg} has not been covered: segments_covered[i]: {segments_covered[i]}")
    
            current_point = main_seg[0]
            if debug: print(f"current_point set at the begining of main_seg: current_point = {current_point}")
    
            segments_covered_temp = [0]*len(segments)
            segments_covered_temp[i] = 1
            if debug: print(f"segments_covered_temp. All zeroes except for one 1 for the main_seg (index i = {i}):\n{segments_covered_temp}")
            
            for j, new_segment in enumerate(segments[i+1:], start=i+1):
                if debug: print(f"Checking new segment of the list. Current index: {j}. Segment: {new_segment}")

                if new_segment[0]>main_seg[1]:
                    if debug: print(f"new_segment: {new_segment} does not touch the main segment: {main_seg}. Exitting inner loop")
                    break
                else:
                    if debug: print(f"new_segment: {new_segment} touches the main segment: {main_seg}.")
                    if j == i+1:
                        current_point = new_segment[0]
                        if debug: print(f"There are no segments between new_segment: {new_segment} and main_seg: {main_seg}.\n"+
                                        f"We can safely move the current point to the begining of the new segment: {current_point}")
                        segments_covered_temp[j] = 1
                        if debug: print(f"segments_covered_temp now looks like this: {segments_covered_temp}")
                    else:
                        if debug: print(f"There are segments between new_segment: {new_segment} and main_seg: {main_seg}.\n"+
                                        f"Checking if it is safe to move the current_point")
                        overlaps = True
                        for k in range(i+1,j):
                            if segments[k][1] < new_segment[0]:
                                overlaps = False
                                if debug: print(f"No overlapping between segment at index {k}: {segments[k]} and {new_segment}! current_point can not be moved!")
                                break
                        if overlaps:
                            current_point = new_segment[0]
                            segments_covered_temp[j] = 1
                            if debug: 
                                print(f"Overlapping found for all segments between indexes {i} and {j}. Is is safe to move the current_point to the starting point of new_segment: {new_segment[0]}")
                                print(f"Current state of segments_covered_temp: {segments_covered_temp}")
                        else:
                            break
  
            if debug: print(f"Updating the array segments_covered. Before: {segments_covered}")
            for l in range(len(segments_covered_temp)):
                if segments_covered_temp[l] == 1:
                    segments_covered[l] = 1
            if debug: print(f"Updating the array segments_covered. After: {segments_covered}")
            points.append(current_point)
            if debug: print(f"Added current_point: {current_point} to points {points}")
        else:
            if debug: print(f"Skipping! Segment: {main_seg} has been covered: segments_covered[i]: {segments_covered[i]}")
            continue
    if debug:
        return [len(points), points]
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
        if type(model_output) is float:
            model_output = round(model_output, decimal_preccision)
        return (model_output, total_time)
    def check_values(first_value, second_value):
        if type(first_value) is float:
            first_value = round(first_value, decimal_preccision)
        if type(second_value) is float:
            second_value = round(second_value, decimal_preccision)
        #pdb.set_trace()
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
    sample_output_1 = [1,[3]]
    sample_1_text = 'All of them contain the point 3'
    sample_input_2=[[4],[[4,7],[1,3],[2,5],[5,6]]]
    sample_output_2 = [2,[3,6]]
    sample_2_text = '2nd and 3rd contain point 3. 1st and 4th contain 6'
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
            good_model_test(_input=[[[1],[[1,3]]]], test_name="Boundary")
            good_model_test(_input=[[[5],[[1,6],[2,3],[5,6],[4,8],[11,int(1e9)]]]], test_name="Boundary")
        elif choice == 't' and DUMMY_MODEL:
            stress_tests(number_of_tests=number_of_tests, values=stress_tests_boundary)
        elif choice == 'a':
            PROMPT_USER = False
            good_model_test(_input=[sample_input_1], test_name="Sample", known_result=sample_output_1)
            good_model_test(_input=[sample_input_2], test_name="Sample", known_result=sample_output_2)
            good_model_test(_input=[[[1],[[1,3]]]], test_name="Boundary")
            good_model_test(_input=[[[5],[[1,6],[2,3],[5,6],[4,8],[11,int(1e9)]]]], test_name="Boundary")
            if DUMMY_MODEL:
                stress_tests(number_of_tests=number_of_tests, values=stress_tests_boundary)

        elif choice == 'x':
            sys.exit()


