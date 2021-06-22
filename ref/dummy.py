import sys

def sort(list):
    return sorted(list)

if __name__ == "__main__":
    a = sys.argv[1][1:-1].split(',')
    for x in sort(a): print(x, '', end="")