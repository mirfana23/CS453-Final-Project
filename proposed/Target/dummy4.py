import sys

def sum_count(s):
    c = 0
    for i in s:
        c += int(i)

    if c > 40:
        print('0')
    else:
        print('1')

if __name__ == "__main__":
    a = sys.argv[1]
    sum_count(a)