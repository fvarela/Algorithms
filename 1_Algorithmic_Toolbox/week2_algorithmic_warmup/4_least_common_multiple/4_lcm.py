# Uses python3
import sys

def lcm_naive(a, b):
    for l in range(1, a*b + 1):
        if l % a == 0 and l % b == 0:
            return l

    return a*b

def model_good(a,b):
    if a < b:
        lower = a
        higher = b
    else:
        lower = b
        higher = a
    factor = 1
    while True:
        if(higher*factor)%lower==0:
            return higher*factor
        else:
            factor +=1


if __name__ == '__main__':
    input = sys.stdin.read()
    a, b = map(int, input.split())
    print(model_good(a, b))

