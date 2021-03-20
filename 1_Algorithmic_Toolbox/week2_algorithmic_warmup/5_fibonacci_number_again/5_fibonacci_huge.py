# Uses python3
import sys

def get_fibonacci_huge_naive(n, m):
    if n <= 1:
        return n

    previous = 0
    current  = 1

    for _ in range(n - 1):
        previous, current = current, previous + current

    return current % m


def model_good(n, module):
    seq = [0,1]
    fmod = [0,1]
    period = 2
    for i in range(1,n):
        seq.append(seq[i]+seq[i-1])
        fmod.append(seq[-1]%module)
        period +=1
        if fmod[-2] == 0 and fmod[-1] == 1:
            fmod = fmod[:-2]
            break
    rest = n%(len(fmod))
    return(fmod[rest])

if __name__ == '__main__':
    input = sys.stdin.read();
    n, m = map(int, input.split())
    print(model_good(n, m))
