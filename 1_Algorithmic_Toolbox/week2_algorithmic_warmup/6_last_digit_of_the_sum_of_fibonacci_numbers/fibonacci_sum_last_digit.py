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

def model_good(n):
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
    target_index = n%(len(fmod)) + 2
    raw_value = fmod[target_index]
    rest = (raw_value+9)%10
    return(rest)

if __name__ == '__main__':
    input = sys.stdin.read()
    n = int(input)
    print(model_good(n))
