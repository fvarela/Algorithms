# Uses python3
import sys

def fibonacci_sum_naive(n):
    if n <= 1:
        return n

    previous = 0
    current  = 1
    sum      = 1

    for _ in range(n - 1):
        previous, current = current, previous + current
        sum += current

    return sum % 10

def good_model(n):
    def get_last_digit(n):
        if n<=1:
            return n
        seq = [0,1]
        if n>1:
            for i in range(1,n):
                seq.append(seq[i]%10+seq[i-1]%10)
        return seq[n]%10
    return (get_last_digit(n) + get_last_digit(n+1) -1)%10

if __name__ == '__main__':
    input = sys.stdin.read()
    n = int(input)
    print(good_model(n))
