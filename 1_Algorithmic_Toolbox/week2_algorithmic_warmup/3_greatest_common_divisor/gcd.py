# Uses python3
import sys

def gcd_naive(a, b):
    current_gcd = 1
    for d in range(2, min(a, b) + 1):
        if a % d == 0 and b % d == 0:
            if d > current_gcd:
                current_gcd = d

    return current_gcd

def model_good(a,b):
    if n<=1:
        return n
    seq = [0,1]
    if n>1:
        for i in range(1,n):
            seq.append(seq[i]%10+seq[i-1]%10)
    return seq[n]%10

if __name__ == "__main__":
    input = sys.stdin.read()
    a, b = map(int, input.split())
    print(model_good(a, b))
