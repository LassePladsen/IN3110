"""
Created on 14.09.2023
Exercise 1 https://pages.github.uio.no/IN3110/assignments/exercises/week3.html
"""

import sys

class RPN_Calc:
    """Reverse polish notation calculator, that is to say the operators (+, -, etc.) comes after its two operands.
    For example 2 + 3 * 5 would instead in RPN be 2 3 + 5 *."""

    def __init__(self) -> None:
        self.stack = []  # list to keep track of the inputs

    def next(self, input_: str) -> None:
        """Adds the next number to the stack, or if input_ is an operator it calculates the result from the last two
        numbers in the stack and replaces them with this new single number."""
        if input_ in ["+", "-", "*", "/", "**"]:  # operators
            if len(self.stack) < 2:  # not enough numbers to operate
                return
            prev = self.stack.pop()
            prev_prev = self.stack.pop()
            self.stack.append(str(eval(prev_prev + input_ + prev)))

        elif input_ == "^":  # convert power symbol to '**'
            self.next("**")

        elif input_.lower() in ["q", "quit", "quit()", "exit", "exit()", "e"]:  # exit script
            print("Exiting calculator...")
            sys.exit(0)

        elif input_.lower() in ["c", "cls", "clear", "restart"]:  # Restart: clear the stack
            print("Clearing the stack...")
            self.stack = []

        elif input_.lower() in ["p", "print"]:  # print last number of stack
            print(self.stack[-1])

        elif input_.replace(".","").isnumeric():  # number
            self.stack.append(input_)

        else:  # unknown input
            # print(input_)
            print("ERROR: UNKNOWN INPUT, TRY AGAIN.")

    def parse(self, input_: str) -> None:
        """Parses through a input mathematical expression string and feeds it into self.next()."""
        for elem in input_.split(" "):
            self.next(elem)

    def run(self):
        """Runs the calculator loop."""
        while True:
            input_ = input("$ ")
            input_ = input_.strip()  # strip edge whitespaces
            if len(input_.split(" ")) > 1:  # more than one input
                self.parse(input_)
            else:
                self.next(input_)



if __name__ == "__main__":
    instance = RPN_Calc()
    if len(sys.argv) > 1:  # parse command-line inputs and print before running loop
        instance.parse(" ".join(sys.argv[1:]))
        instance.next("p")
    instance.run()
