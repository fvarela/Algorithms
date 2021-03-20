# Uses python3
import sys

def fibonacci_partial_sum_naive(from_, to):
    sum = 0

    current = 0
    next  = 1

    for i in range(to + 1):
        if i >= from_:
            sum += current

        current, next = next, current + next

    return sum % 10

def model_good(from_, to):

    def get_sum_last_digit(n):
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
        if target_index >=len(fmod):
            target_index = target_index%10
        raw_value = fmod[target_index]
        rest = (raw_value+9)%10
        return(rest)
    if to == 0:
        last = 0
    else:
        last = get_sum_last_digit(to)
    if from_ == 0:
        first = 0
    else:
        first = get_sum_last_digit(from_-1)
    return(last-first+10)%10

if __name__ == '__main__':
    input = sys.stdin.read();
    from_, to = map(int, input.split())
    print(model_good(from_, to))