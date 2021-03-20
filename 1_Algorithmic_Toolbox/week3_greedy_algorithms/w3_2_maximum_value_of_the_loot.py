import sys
import pdb
def model_good(capacity, weights, values, debug=False):
    if debug:
        print(f"Capacity: {capacity}\n")
        print(f"Weights: {weights}\n")
        print(f"Values: {values}\n")
    
    value_per_weight = [values[i]/weights[i] for i in range(len(values))]
    sorted_lists = sorted(zip(value_per_weight, values, weights), reverse=True)
    tuples = zip(*sorted_lists)
    value_per_weight, values, weights = [list(tuple) for tuple in tuples]
    if debug:
        print(f"SORTED Weights: {weights}\n")
        print(f"SORTED Values: {values}\n")
        print(f"SORTED Values per weights: {value_per_weight}\n")
    current_value = 0.
    current_capacity = capacity
    for i in range(len(weights)):
        if current_capacity >0:
            if debug: print(f"PREVIOUS iteration {i}: Current capacity {current_capacity} - Current weight: {weights[i]} - Current value: {current_value}\n")
            if current_capacity >= weights[i]:
                if debug: print(f"The whole item fitted in the bag\n") 
                current_capacity -= weights[i]
                current_value += values[i]
            else:
                item_ratio = current_capacity/weights[i]
                current_capacity = 0
                current_value += values[i]*item_ratio
                if debug: print(f"Only {item_ratio} fitted in the bag\n")
            if debug: print(f"POST iteration {i}: Current capacity {current_capacity} - Current weight: {weights[i]} - Current value: {current_value}\n")
        else:
            break
    if debug: print(f"Result: " + "{:.10f}".format(current_value))
    return current_value

def model_dummy(capacity, weights, values, debug=False):
    value = 0.
    return tva


if __name__ == '__main__':
    data = list(map(int, sys.stdin.read().split()))
    n, capacity = data[0:2]
    values = data[2:(2 * n + 2):2]
    weights = data[3:(2 * n + 2):2]
    opt_value = model_good(capacity, weights, values)
    print("{:.10f}".format(opt_value))

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

        model_output = model(_input[0][1],_input[1][0],_input[1][1],debug=DEBUG)
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
                #pdb.set_trace()
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
    sample_input_1=[[3,50],[[20, 50, 30],[60, 100, 120]]]
    sample_output_1 = 180.0000
    sample_1_text = 'To achieve the value of 180, we take the first and the third item into the bag'
    sample_input_2=[[1,10],[[30],[500]]]
    sample_output_2 = 166.6667
    sample_2_text = 'Here we just take one third of the only available item.'
    boundary_input=[[1,int(1e3)], [0,int(2^6)],[0,int(2^6)],[0,int(2^6)]]
    stress_tests_boundary = [[0,int(1e3)]]
    decimal_preccision = 4

    print(f"\n{Style.BRIGHT}Money Change Algorithm.{Style.RESET_ALL}\n")
    table_data = [['Task', "The goal of this code problem is to implement an algorithm for the fractional knapsack problem."],
                    ['Input', 'The first line o f the input contains the number n of items and the capacity W of a knapsack.\n'+
                                'The next n lines define the values and weights of the items. The i-th line contains integers vi and wi -the\n'+
                                'value and the weight of i-th item, respectively'],
                    ['Constraints', f'{boundary_input[0][0]}<=n<={boundary_input[0][1]}; {boundary_input[1][0]}<=W<={boundary_input[1][1]};\n'+
                                    f'{boundary_input[2][0]}<=vi<={boundary_input[2][1]}; {boundary_input[3][0]}<=wi<={boundary_input[3][1]}'],
                    ['Output Format', 'Output themaximal value of fractions of items that fit into the knapsack. Output the answer with at least 4 digits after the decimal point'],
                    ['Sample', f'input {sample_input_1[0]}, output {sample_output_1}. {sample_1_text}.'],
                    ['Sample', f'input {sample_input_2[0]}, output {sample_output_2}. {sample_2_text}.']]


    table = AsciiTable(table_data)
    table.inner_heading_row_border = False
    print(table.table+"\n")

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
            good_model_test(_input=[[[1,0],[[1],[0]]]], test_name="Boundary")
            good_model_test(_input=[[[3,int(2e6)],[[1,int(2e6),300],[0,int(2e6),300]]]], test_name="Boundary") 
            good_model_test(_input=[[[3,int(2e6)],[[1,100,200],[0,50,75]]]], test_name="Boundary") 
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


