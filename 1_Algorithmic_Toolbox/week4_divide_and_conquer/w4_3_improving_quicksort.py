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

def partition3(a, l, r, debug=False):
    #write your code here
    if debug: print(f"\tPartition3 a:{a}, l:{l}, r:{r}")

    #El pivot está en la posición l.
    pivot = a[l]
    if debug: print(f"\tPartition3 pivot:{a[l]}")
    #Dos índices. less_index y equal_index. En inicio los dos iguales a l
    less_index = l
    equal_index = l
    #Vas recorriendo el array desde el pivot (posición l+1)
    for index in range(l+1, r+1):
        if debug: print(f"\t\tPartition3 Inside loop index={index}. Comparing {a[index]} with pivot:{pivot}. a={a}. less_index={less_index}, equal_index={equal_index}")
    #Si el número es menor a pivot aumentas less_index y equal_index

        if a[index] < pivot:
            less_index += 1
            equal_index +=1
            if debug: print(f"\t\tPartition3 Inside loop {a[index]} LESS THAN pivot={pivot}. less_index={less_index}, equal_index={equal_index}")
            if less_index == equal_index:
        #Intercambias ese número por el que esté en less_index
                if debug: print(f"\t\tPartition3 Inside loop {a[index]}. Less index is the same as equal_index")
                a[index], a[less_index] = a[less_index], a[index]
            else:
                if debug: print(f"\t\tPartition3 Inside loop {a[index]}. equal_index is greater. Swapping positions index:{index} and equal_index:{equal_index} first. Before: {a}")
                a[index], a[equal_index] = a[equal_index], a[index]
                if debug: print(f"\t\tPartition3 Inside loop {a[index]}. After: {a}")
                if debug: print(f"\t\tPartition3 Inside loop {a[index]}. Swapping now less_index: {less_index} with equal_index: {equal_index}.")
                a[less_index], a[equal_index] = a[equal_index], a[less_index]
                if debug: print(f"\t\tPartition3 Inside loop {a[index]}. After: {a}")
            if debug: print(f"\t\tPartition3 Inside loop after switching positions: a={a}")

        #Si el número es menor a pivot aumentas equal_index
        elif a[index] == pivot:
            
            equal_index += 1
            if debug: print(f"\t\tPartition3 Inside {a[index]} EQUAL TO pivot={pivot}. less_index={less_index}, equal_index={equal_index}")
            a[index], a[equal_index] = a[equal_index], a[index]
            if debug: print(f"\t\tPartition3 Inside loop after switching positions: a={a}")
        else:
            if debug: print(f"\t\tPartition3 Inside loop {a[index]} is GREATER THAN pivot: {pivot}")
            #Intercambias ese número por el que esté en equal_index
        if debug: print("")
    if debug: print(f"\tPartition3. before swapping indexes l:{l} with less_index:{less_index} a={a}")
    a[less_index], a[l] = a[l], a[less_index]
    if debug: print(f"\tPartition3. after swapping indexes l:{l} with less_index:{less_index} a={a}")
    if debug: print(f"\tPartition3. Returning less_index={less_index} and equal_index={equal_index}. a={a}")
    return (less_index, equal_index)
    

def model_good(a, l, r, debug=False):
    if debug: print(f"Model good. a={a}. l={l}, r={r}")
    if l >= r:
        if debug: print(f"Left is equal or greater than r. Exiting. l={l}, r={r}")
        return
    k = random.randint(l, r)
    if debug: print(f"random index k. k={k}. a[k]={a[k]}")
    a[l], a[k] = a[k], a[l]
    if debug: print(f"a with k in the first position: a={a}.")
    #use partition3
    m1, m2 = partition3(a, l, r, debug=debug)
    model_good(a, l, m1 - 1, debug = debug)
    model_good(a, m2 + 1, r, debug = debug)
    if debug: print(f"Model good. OUTPUT a={a}.")
    

def partition2(a, l, r, debug=False):
    if debug: print(f"Partition2 a:{a}, l:{l}, r:{r}")
    #El pivot está en la posición l. Con esto vas recorriendo todo el array 
    #y si el número es menor te lo llevas a la izquierda
    
    #x es el pivot
    #j es el primer numero mayor que el pivot
    x = a[l]
    j = l
    if debug: print(f"j vale{j}. x vale {x}")

    for i in range(l + 1, r + 1):
        if debug: print(f"Comparando a[i]: {a[i]} con x: {x}")
        if a[i] <= x:
            j += 1
            if debug: print(f"a[i] es menor o igual. j vale {j}")
            #Los intercambias
            if debug: print(f"Antes del intercambio posiciones {i} con {j} es decir, {a[i]} con {a[j]}: {a}")
            a[i], a[j] = a[j], a[i]
            if debug: print(f"Después del intercambio: {a}")
    if debug: print(f"a antes de la última línea en la que se cambian los índices {l} por {j}: {a}")
    a[l], a[j] = a[j], a[l]
    if debug: print(f"a después: {a}. Valor que se devolverá: {j}")
    return j

def model_dummy(a, l, r, debug=False):
   
    #Si el valor de la izquierda es igual o superior al de la derecha no haces nada
    if l >= r:
        return
    #Si el valor de la derecha es superior:
    #Coges el pivot. Un valor al azar
    k = random.randint(l, r)
    
    if debug: print(f"a before moving the pivot {a[k]}: {a}")
    #Mueves el pivot al principio del array para que no moleste
    a[l], a[k] = a[k], a[l]
    if debug: print(f"a after moving pivot: {a}")
    #use partition3
    m = partition2(a, l, r, debug=False)
    if debug: print(f"a after partition {a}. m: {m}")
    model_dummy(a, l, m - 1)
    model_dummy(a, m + 1, r)

if __name__ == '__main__':
    input = sys.stdin.read()
    n, *a = list(map(int, input.split()))
    model_good(a, 0, n - 1)
    for x in a:
        print(x, end=' ')

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
        model_output.append(model(a=_input,l=0,r=len(_input)-1,debug=DEBUG))
        total_time = round(time.time() - model_start,2)
        if type(model_output) is float:
            model_output = round(model_output, decimal_preccision)
        return (_input, total_time)

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
    STRESS = True

    RANDOM_INPUT=True
    PROMPT_USER = True
    PROMP_ON_ERRORS = True
    number_of_tests = 500

    sample_input_1=[[2,3,9,2,2]]
    sample_output_1 = [2,2,2,3,9]
    sample_1_text = ''


    stress_tests_boundary = [1000,500]
    # 10 numeros tendra el array
    # 10 valor máximo (el mínimo es 0)
    decimal_preccision = 4

    print(f"\n{Style.BRIGHT}Improving Quicksort Algorithm.{Style.RESET_ALL}\n")
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


