import os
import sys


def print_hi(name):
    print(f"Hi, {name}")


def main():
    print("\tcalling print_hi()")
    print_hi("Luke")
    print("\treturned from calling print_hi()")


if __name__ == "__main__":
    print("calling main")
    main()
    print("returned from calling main")
