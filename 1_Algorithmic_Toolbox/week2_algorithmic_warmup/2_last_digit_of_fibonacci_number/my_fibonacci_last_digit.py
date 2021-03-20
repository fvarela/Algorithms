# Uses python3
import sys

def get_fibonacci_last_digit_naive(n):
    if n <= 1:
        return n

    previous = 0
    current  = 1

    for _ in range(n - 1):
        previous, current = current, previous + current

    return current % 10


def model_good(n):
    if n<=1:
        return n
    seq = [0,1]
    if n>1:
        for i in range(1,n):
            seq.append(seq[i]%10+seq[i-1]%10)
    return seq[n]%10


if __name__ == '__main__':
    input = sys.stdin.read()
    n = int(input)
    print(model_good(n))
