import sys
import main

if __name__ == "__main__":
    usage = ""

    # TODO implement args version to function as module receiving user input
    args = sys.argv
    print(args)
    while len(args) < 2:
        print("Invalid parameters")
        print(usage)
    main(*args[1:])
