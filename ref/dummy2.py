import sys
a = ''
def diff(s):
    global a
    for i in range(len(s)-2):
        b = abs(int(s[i]) - int(s[i+1]))
        if b > 5:
            a += '1'
        else:
            a += '0'

if __name__ == "__main__":
    x = sys.argv[1]
    diff(x)
    print(a)