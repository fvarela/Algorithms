import sys
def model_good(n, debug=False):
    if debug:
        print(f"Model Good. Processing input: {n}\n")
    coins = [10, 5, 1]
    amount_left = n
    total_coins = 0
    for coin in coins:
        if amount_left >= 0:
            number_of_coins = amount_left//coin
            amount_left -= number_of_coins*coin
            total_coins += number_of_coins
            if debug:
                print(f"Added {number_of_coins} coins of value {coin}\n")
            #pdb.set_trace()
        else:
            break
    return total_coins


def model_dummy(n, debug=False):
    coins = [10, 5, 1]
    amount_left = n
    total_coins = 0
    for coin in coins:
        if amount_left >= 0:
            number_of_coins = amount_left//coin
            amount_left -= number_of_coins*coin
            total_coins += number_of_coins
        else:
            break
    return total_coins


if __name__ == '__main__':
    n = int(sys.stdin.read())
    print(model_good(n))
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

        model_output = model(_input[0],debug=DEBUG)
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
    DEBUG = False
    DUMMY_MODEL=True
    GOOD_MODEL = True
    RANDOM_INPUT=False
    PROMPT_USER = True
    PROMP_ON_ERRORS = True
    number_of_tests = 1000
    sample_input_1=[2]
    sample_output_1 = 2
    sample_1_text = '(2=1+1)'
    sample_input_2=[28]
    sample_output_2 = 6
    sample_2_text = '(28=10+10+5+1+1+1)'
    boundary_input=[[1,int(1e3)]]
    stress_tests_boundary = [[0,int(1e3)]]

    print(f"\n{Style.BRIGHT}Money Change Algorithm.{Style.RESET_ALL}\n")
    table_data = [['Task', "The goal in this problem is to find the minimum number of coins needed to change\n"+ 
                            "the input value (an integer) into coiins wit denominations 1,5 and 10"],
                    ['Input', 'The input consists of a single integer m'],
                    ['Constraints', f'{boundary_input[0][0]}<=m<={boundary_input[0][1]}'],
                    ['Output Format', 'Output the minimum number of coins with denominations 1, 5, 10 that chages m'],
                    ['Sample', f'input {sample_input_1[0]}, output {sample_output_1}. {sample_1_text}.'],
                    ['Sample', f'input {sample_input_2[0]}, output {sample_output_2}. {sample_2_text}.']]


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
            good_model_test(_input=[[1], [int(1e3)]], test_name="Boundary") 
        elif choice == '3':
            stress_tests(number_of_tests=number_of_tests, values=stress_tests_boundary)
        elif choice == '4':
            PROMPT_USER = True
            good_model_test(_input=[sample_input_1], test_name="Sample", known_result=sample_output_1)
            good_model_test(_input=[sample_input_2], test_name="Sample", known_result=sample_output_2)
            good_model_test(_input=[[1], [int(1e3)]], test_name="Boundary")  
            stress_tests(number_of_tests=number_of_tests, values=stress_tests_boundary)
        elif choice == '5':
            PROMPT_USER = False
            good_model_test(_input=[sample_input_1], test_name="Sample", known_result=sample_output_1)
            good_model_test(_input=[sample_input_2], test_name="Sample", known_result=sample_output_2)
            good_model_test(_input=[[1], [int(1e3)]], test_name="Boundary")  
            stress_tests(number_of_tests=number_of_tests, values=stress_tests_boundary)
        elif choice == '6':
            sys.exit()


