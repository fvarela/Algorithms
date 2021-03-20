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
    if a < b:
        lower = a
        higher = b
    else:
        lower = b
        higher = a
    module = higher%lower
    if module == 0:
        return lower
    else:
        return model_good(lower, module)


if __name__ == "__main__":
    input = sys.stdin.read()
    a, b = map(int, input.split())
    print(model_good(a, b))
