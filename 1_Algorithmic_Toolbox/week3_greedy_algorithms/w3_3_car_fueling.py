import sys
import pdb
def model_good(distance, tank, stops, debug=False):
    stops.append(distance)
    stops.insert(0,0)
    if debug:
        print(f"Distance: {distance}\n")
        print(f"Tank: {tank}\n")
        print(f"Stops: {stops}\n")
    number_refills = 0
    current_position = 0
    while current_position < len(stops)-1:
        last_position = current_position
        while current_position < len(stops)-1 and (stops[current_position+1] - stops[last_position]) <= tank:
            if debug: print(f"Inside nested while loop: current position: {current_position}. Length of stops: {len(stops)}.\n"+
                            f"Next segment length: {stops[current_position+1] - stops[last_position]}. Tank capacity: {tank}.")
            current_position += 1
            if debug: print(f"Can make it. Going to next stop. Current_position: {current_position}")
        if current_position == last_position:
            if debug: print("Car couldn't make a step")
            return -1
        elif current_position < len(stops)-1:
            number_refills += 1
            if debug: print(f"Still not at the end of the jurney. Refilling at position {current_position}. Distance: {stops[current_position]}. Number of refills so far: {number_refills}\n")
    return number_refills
            


def model_dummy(capacity, weights, values, debug=False):
    return -1

if __name__ == '__main__':
    d, m, _, *stops = map(int, sys.stdin.read().split())
    print(compute_min_refills(d, m, stops))

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
        model_output = model(_input[0][0],_input[1][0],_input[3],debug=DEBUG)
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
    sample_input_1=[[950],[400],[4],[200, 375, 550, 750]]
    sample_output_1 = 2
    sample_1_text = 'Distance 950. Two refills are ok at 375 and 750'
    sample_input_2=[[10],[3],[4],[1, 2, 5, 9]]
    sample_output_2 = -1
    sample_2_text = 'Cannot reach gas station at point 9'
    sample_input_3=[[200],[250],[2],[100, 150]]
    sample_output_3 = 0
    sample_3_text = 'No need to refill the tank. It can travel 250 miles and destination is just 200 miles away.'
    boundary_input=[[1,int(1e5)], [1,400],[1,300],[0,'d']]
    stress_tests_boundary = [[0,int(1e3)]]
    decimal_preccision = 4

    print(f"\n{Style.BRIGHT}Car Fueling Algorithm.{Style.RESET_ALL}\n")
    table_data = [['Task', "You are going to travel to another city that is located 'd' miles away from your home city.\n"+
                            "Your car can travel at most 'm' miles on a full tank and you start witha full tank\n"+
                            "Along your way, there are gas stations at distances stop1, stop2,...,stopn from your home city\n"+
                            "What is the minimum number of refills needed?"],
                    ['Input', 'The firest line contains an iteger d. The second line contains an integer m.\n'+
                                'The third line specifies an integer n. Finally the last line contaisn integers stop1, stop2, stop3,...,stopn\n'+
                                'value and the weight of i-th item, respectively'],
                    ['Output Format', 'Minimun number of refills needed. If it is not possible to reach destination output -1'],
                    ['Constraints', f'{boundary_input[0][0]}<=d<={boundary_input[0][1]}; {boundary_input[1][0]}<=m<={boundary_input[1][1]};\n'+
                                    f'{boundary_input[2][0]}<=n<={boundary_input[2][1]}; {boundary_input[3][0]}<stop1<stop2<...<stopn<={boundary_input[3][1]}'],
            
                    ['Sample', f'input {sample_input_1}, output {sample_output_1}. {sample_1_text}.'],
                    ['Sample', f'input {sample_input_2}, output {sample_output_2}. {sample_2_text}.'],
                    ['Sample', f'input {sample_input_3}, output {sample_output_3}. {sample_3_text}.']]


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


