import sys

def test(s):
    if "123" in s:
        print("s contains 123")
    elif "a" in s and "b" in s:
        print("s cointans a and b")
    elif "4" in s and "8" in s:
        print("s cointans 4 and 8")
    elif len(s) < 7:
        print("s len is < 7")
    elif len(s) < 10:
        print("s len is < 10")
    elif len(s) < 13:
        print("s len is < 13")
    elif len(s) < 20:
        print("s len is < 20")
    elif len(s) < 23:
        print("s len is < 23")
    else:
        raise Exception("this is else branch")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Need one more arguments")
    test(sys.argv[1])