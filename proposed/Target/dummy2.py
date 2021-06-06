import sys

def error(s):
    if '123' in s:
        print('0')
    elif '34' in s:
        print('0')
    elif '567' in s:
        print('0')
    elif '78' in s:
        print('0')
    elif '90' in s:
        print('0')
    else:
        print('1')

if __name__ == "__main__":
    a = sys.argv[1]
    error(a)
