#!/usr/bin/python3
from unicode_doctor import DecodeEncodeUnicodeDoctor, ForcedAsciiUnicodeDoctor


if __name__ == "__main__":
    testset = [
        ("Daniël", "DaniÃ«l"),
        ("Daniël", "DaniÙl"),
        ("Daniël", "Daniel"),
        ("Daniël", "Danil"),
        ("Daniël", "Dani?l"),
    ]

    for testcase in testset:
        for imp in [DecodeEncodeUnicodeDoctor, ForcedAsciiUnicodeDoctor]:
            for res in imp.make_guess(str_good=testcase[0], str_bad=testcase[1]):
                print(res)
                if res.acceptable:
                    print("This is acceptable")
                else:
                    print("This is BAD")
                print()
