import sys

def quicksort(numbers, low, high):
    i = low
    j = high
    pivot = numbers[int(low + (high-low)/2)]
    while i <= j:
        while numbers[i] < pivot:
            i+= 1
        while numbers[j] > pivot:
            j -= 1
        if i <= j:
            exchange(numbers, i, j)
        i += 1
        j -= 1
    if low < j:
        quicksort(numbers, low, j)
    if i < high:
        quicksort(numbers, i, high)


def exchange(numbers, i, j):
    temp = numbers[i]
    numbers[i] = numbers[j]
    numbers[j] = temp

if __name__ == "__main__":
    a = sys.argv[1][1:-1].split(',')
    quicksort(a, 0, len(a) - 1)
    for x in a: print(x, '', end="")
