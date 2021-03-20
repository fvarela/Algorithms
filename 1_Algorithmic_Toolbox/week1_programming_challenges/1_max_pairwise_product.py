# python3


def max_pairwise_product(numbers):
    n = len(numbers)
    first = numbers[0]
    second = numbers[1]
    for number in numbers[2:]:
        if number > min(first,second):
            if first < second:
                first = number
            else:
                second = number
    return first*second


# def model_good(numbers):
#     n = len(numbers)
#     first = numbers[0]
#     second = numbers[1]
#     for number in numbers[2:]:
#         if number > min(first,second):
#             if first < second:
#                 first = number
#             else:
#                 second = number
#     return first*second



if __name__ == '__main__':
    input_n = int(input())
    input_numbers = [int(x) for x in input().split()]
    print(max_pairwise_product(input_numbers))
