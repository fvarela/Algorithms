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


def model_good(n, debug=False):
    def is_greater_or_equal(first,previous):
        if debug: print(f"Checking wich one is greater: {first}, {previous}")
        first = str(first)
        previous = str(previous)
        if len(first) != len(previous):
            temp_first = first
            temp_previous = previous
            first = temp_first + temp_previous
            previous = temp_previous + temp_first
        first = int(first)
        previous = int(previous)
        if debug: print(f"Is {first} greater or equal than {previous}?: {first>=previous}")
        return (first>=previous)
        
    answer = ''
    while len(n)>0:
        maxDigit = 0
        maxDigitIndex = 0
        for i,digit in enumerate(n):
            if is_greater_or_equal(int(digit),maxDigit):
                maxDigit = int(digit)
                maxDigitIndex = i
        answer += str(maxDigit)
        n.pop(maxDigitIndex)
    return answer



def model_dummy(n, debug=False):
    res = ""
    for x in a:
        res += x
    return res

if __name__ == '__main__':
    input = sys.stdin.read()
    data = input.split()
    a = data[1:]
    print(model_good(a))


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
        model_output = model(model_input,debug=DEBUG)
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
                
                (good_output, good_time) = test_model(model_good,value.copy())
                result = None
                matches = True
                if known_result is not False:
                    (matches,result) = check_values(good_output, known_result)
                else:
                    result = 'Unknown'
                table_data=[["Test #", "Input", "Model", "Output", "Time", "Result"],
                            [i,value, model_good.__name__, good_output if len(good_output[1])<10 else 'Too large to print', good_time, result]]
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
                table_data.append([i, _input, model_good.__name__, good_output if len(good_output[1])<10 else 'Too large to print', good_time, result])
                table_data.append([i, _input, model_dummy.__name__, dummy_output if len(dummy_output[1])<10 else 'Too large to print', dummy_time, result])
                if i == number_of_tests:
                    print_table(table_data, end=True)        
                else:
                    print_table(table_data, end=False)
                if not _continue:
                    wait_for_input_after_error()
            PROMP_ON_ERRORS = True
            wait_for_input()     
    DEBUG = True
    DUMMY_MODEL=True
    GOOD_MODEL = True
    RANDOM_INPUT=True
    PROMPT_USER = True
    PROMP_ON_ERRORS = True
    number_of_tests = 1000
    # sample_input_1=[2, 8, 2, 3, 6, 4, 1, 1, 10, 6, 3, 3, 6, 1, 3, 8, 4, 6, 1, 10, 8, 4, 10, 4, 1, 3, 2, 3, 2, 6, 1, 5, 2, 9, 8, 5, 10, 8, 7, 9, 6, 4, 2, 6, 3, 8, 8, 9, 8, 2, 9, 10, 3, 10, 7, 5, 7, 1, 7, 5, 1, 4, 7, 6, 1, 10, 5, 4, 8, 4, 2, 7, 8, 1, 1, 7, 4, 1, 1, 9, 8, 6, 5, 9, 9, 3, 7, 6, 3, 10, 8, 10, 7, 2, 5, 1, 1, 9, 9, 5]
    # sample_output_1 = '9999999998888888888887777777776666666666555555554444444443333333333222222222111111111111111101010101010101010'
    sample_input_1=[21,2]
    sample_output_1 = '221'
    sample_1_text = ''
    sample_input_2=[9,4,6,1,9]
    sample_output_2 = '99641'
    sample_2_text = ''
    sample_input_4=[23,39,92]
    sample_output_4 = '923923'
    sample_4_text = ''
    sample_input_5=[57,51,5]
    sample_output_5 = '57551'
    sample_5_text = ''
    sample_input_6=[34,344]
    sample_output_6 = '34434'
    sample_6_text = ''
    sample_input_7=[433,43,34,344]
    sample_output_7 = '4343334434'
    sample_7_text = ''
    sample_input_8=[41,4142]
    sample_output_8 = '414241'
    sample_8_text = ''
    sample_input_9=[797,79,7]
    sample_output_9 = '797977'
    sample_9_text = ''
    sample_input_10=[85,858]
    sample_output_10 = '85885'
    sample_10_text = ''
    sample_input_11=[9,8,1,100,110]
    sample_output_11 = '981110100'
    sample_11_text = ''
    stress_tests_boundary = [[1,int(1e3)]]
    decimal_preccision = 4

    print(f"\n{Style.BRIGHT}Maximum Salary Algorithm.{Style.RESET_ALL}\n")

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
            good_model_test(_input=[sample_input_4], test_name="Sample", known_result=sample_output_4)
            good_model_test(_input=[sample_input_5], test_name="Sample", known_result=sample_output_5)
            good_model_test(_input=[sample_input_6], test_name="Sample", known_result=sample_output_6)
            good_model_test(_input=[sample_input_7], test_name="Sample", known_result=sample_output_7)
            good_model_test(_input=[sample_input_8], test_name="Sample", known_result=sample_output_8)
            good_model_test(_input=[sample_input_9], test_name="Sample", known_result=sample_output_9)
            good_model_test(_input=[sample_input_10], test_name="Sample", known_result=sample_output_10)
            good_model_test(_input=[sample_input_11], test_name="Sample", known_result=sample_output_11)
        elif choice == 'b':
            good_model_test(_input=[[1]], test_name="Boundary")
            good_model_test(_input=[[1e3]], test_name="Boundary")
        elif choice == 't' and DUMMY_MODEL:
            stress_tests(number_of_tests=number_of_tests, values=stress_tests_boundary)
        elif choice == 'a':
            PROMPT_USER = False
            good_model_test(_input=[sample_input_1], test_name="Sample", known_result=sample_output_1)
            good_model_test(_input=[sample_input_2], test_name="Sample", known_result=sample_output_2)
            good_model_test(_input=[sample_input_3], test_name="Sample", known_result=sample_output_3)
            good_model_test(_input=[[1]], test_name="Boundary")
            good_model_test(_input=[[1e3]], test_name="Boundary")
            if DUMMY_MODEL:
                stress_tests(number_of_tests=number_of_tests, values=stress_tests_boundary)

        elif choice == 'x':
            sys.exit()


