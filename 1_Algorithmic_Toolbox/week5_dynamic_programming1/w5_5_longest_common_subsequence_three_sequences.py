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
   

def model_good(first, second, third, debug=False):
    if debug: print(f"Model good. Inputs:{first}, {second}, {third}.")
    memoization = {}
    def lcs (s1, s2, s3, i, j, k):
        key = str(i)+','+str(j)+','+str(k)
        if key in memoization.keys():
            return memoization[key]
        if i == 0 or j ==0 or k == 0:
            result = 0
        elif s1[i-1] == s2[j-1] == s3[k-1]:
            result = 1 + lcs(s1, s2, s3, i-1, j-1, k-1)
        else:
            result =  max (lcs(s1,s2,s3,i-1,j,k), lcs(s1,s2,s3,i,j-1,k), lcs(s1,s2,s3,i,j,k-1))
        memoization[key] = result
        return result
    return lcs(first, second, third, len(first), len(second), len(third))

def model_dummy(first, second, third, debug=False):
    if debug: print(f"Model good. Inputs:{first}, {second}, {third}.")
    def lcs (s1, s2, s3, i, j, k):
        if i == 0 or j ==0 or k == 0:
            return 0
        if s1[i-1] == s2[j-1] == s3[k-1]:
            return 1 + lcs(s1, s2, s3, i-1, j-1, k-1)
        return max (lcs(s1,s2,s3,i-1,j,k), lcs(s1,s2,s3,i,j-1,k), lcs(s1,s2,s3,i,j,k-1))
    return lcs(first, second, third, len(first), len(second), len(third))


if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    an = data[0]
    data = data[1:]
    a = data[:an]
    data = data[an:]
    bn = data[0]
    data = data[1:]
    b = data[:bn]
    data = data[bn:]
    cn = data[0]
    data = data[1:]
    c = data[:cn]
    print(model_good(a, b, c))


else:
    import random
    import pdb
    import time
    from terminaltables import AsciiTable
    import colorama
    from colorama import Fore, Style, Back
    colorama.init()

    def test_model(model, data):

        # model input: x[0, 3], y:[0, 4]

        model_start = time.time()
        model_output=[]
        model_output = model(data[0],data[1],data[2], debug=DEBUG)
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
        if PROMPT_ON_ERRORS:
            choice = None
            while choice not in ('y','x', 'a'):
                choice = input("Press 'y' to continue, 'a' to continue and not be asked again, 'x' to exit.\n")
                if choice == 'x':
                    sys.exit()
                elif choice == 'a':
                    PROMPT_ON_ERRORS = False
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
            array1 = []
            array2 = []
            for _ in range(0, random.randint(1,10)):
                array1.append(random.randint(0,5))
            for _ in range(0, random.randint(1,10)):
                array2.append(random.randint(0,5))
            return [array1,array2]

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
    DEBUG = True

    ONLY_DUMMY = False

    SAMPLE = True
    BOUNDARY = False
    STRESS = False

    RANDOM_INPUT=True
    PROMPT_USER = True
    PROMPT_ON_ERRORS = True
    number_of_tests = 500

    sample_input_1= [[1,2,3],[2,1,3],[1,3,5]]
    sample_output_1 = 2
    sample_1_text = ''
    sample_input_2=[[8,3,2,1,7],[8,2,1,3,8,10,7],[6,8,3,1,4,7]]
    sample_output_2 = 3 
    sample_2_text = ''

    stress_tests_boundary = [1,1000]

    decimal_preccision = 4

    print(f"\n{Style.BRIGHT}Longest Common Subsequence of Three Sequences Algorithm.{Style.RESET_ALL}\n")
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
              
            if BOUNDARY: 
                good_model_test(_input=[[1]], test_name="Boundary")
                good_model_test(_input=[[1e3]], test_name="Boundary")
            if STRESS:
                stress_tests(number_of_tests=number_of_tests, boundaries=stress_tests_boundary)

        elif choice == 'x':
            sys.exit()


