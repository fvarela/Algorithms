# Uses python3
def calc_fib(n):
    seq = [0,1]
    if n>1:
        for i in range(1,n):
            seq.append(seq[i]+seq[i-1])
    return seq[n]

n = int(input())
print(calc_fib(n))