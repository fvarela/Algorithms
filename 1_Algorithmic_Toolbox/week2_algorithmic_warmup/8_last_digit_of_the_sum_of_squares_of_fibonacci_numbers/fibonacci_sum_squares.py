# Uses python3
from sys import stdin

def fibonacci_sum_squares_naive(n):
    if n <= 1:
        return n

    previous = 0
    current  = 1
    sum      = 1

    for _ in range(n - 1):
        previous, current = current, previous + current
        sum += current * current

    return sum % 10

def good_model(n):
    seq = [0,1]
    fmod = [0,1]
    i=1
    while True:
        seq.append(seq[i]+seq[i-1])
        fmod.append(seq[-1]%10)
        if fmod[-2] == 0 and fmod[-1] == 1:
            fmod = fmod[:-2]
            break
        i+=1
    def get_last_digit(m):
        target_index = (m%(len(fmod)))
        rest = fmod[target_index]
        return(rest)
    first_digit = get_last_digit(m = n)
    last_digit = get_last_digit(m = n+1)
    solution = (first_digit*last_digit)%10
    return solution


if __name__ == '__main__':
    n = int(stdin.read())
    print(good_model(n))
