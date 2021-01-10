class Calculator:
    def __init__(self):
        self.vars = dict()
        self.operators = {'+', '-', '*', '/', '(', ')', '^'}
        self.priorities = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
        self.main()

    def main(self):
        while True:
            inp = input()
            if inp.startswith('/'):
                self.check_command(inp)
                continue

            out = ''.join(inp.split())
            while '++' in out:
                out = out.replace('++', '+')
            while '---' in out:
                out = out.replace('---', '-')
            while '--' in out:
                out = out.replace('--', '+')

            for i in self.operators:
                out = out.replace(i, ' ' + i + ' ')

            split_inp = out.split()
            if not out:
                continue
            elif '=' in out:  # adding variables
                self.get_vars(out)
                continue
            else:
                if split_inp.count('(') != split_inp.count(')'):
                    print('Invalid expression')
                    continue
                restart = False
                for a, b in zip(split_inp, split_inp[1:]):
                    if a == '/' and b == '/' or a == '*' and b == '*':
                        print('Invalid expression')
                        restart = True
                        break
                if restart:
                    continue
                if len(split_inp) == 1 and split_inp[0] not in self.vars:
                    print('Unknown variable')

                print(*self.compute_postfix(self.infix_to_postfix(out)))

    @staticmethod
    def check_command(inp):
        if inp == '/exit':
            print('Bye!')
            exit()
        if inp == '/help':
            print('The calculator supports the SUM, the SUB, the MULT,'
                  'the DIV and the POW of numbers or variables')
        else:
            print('Unknown command')

    def get_vars(self, inp):
        try:
            k, v = (i.strip() for i in inp.split('='))
        except ValueError:
            print('Invalid identifier')
        else:
            if not k.isalpha():
                print('Invalid identifier')
                return
            if v in self.vars:
                self.vars[k] = self.vars[v]
            elif not v.isdigit():
                print('Invalid identifier')
                return
            else:
                self.vars.update([(k, v)])
            return

    def infix_to_postfix(self, raw_input):
        stack = []
        output = []
        for char in raw_input.split():
            # if an operand then put it directly in postfix expression
            if char not in self.operators:
                output.append(char)
            # else operators should be put in stack
            elif char == '(':
                stack.append('(')
            elif char == ')':
                while stack and stack[-1] != '(':
                    output += stack.pop()
                stack.pop()
            else:
                # lesser priority can't be on top on higher
                # or equal priority so pop and put in output
                while stack and stack[-1] != '(' \
                        and self.priorities[char] <= self.priorities[stack[-1]]:
                    output += stack.pop()
                stack.append(char)
        while stack:
            output += stack.pop()
        return output

    def compute_postfix(self, post_expr):
        result = []
        for i in post_expr:
            if i.isdigit():
                result.append(int(i))
            elif i in self.vars:
                result.append(int(self.vars[i]))
            elif i in self.operators:
                op2 = result.pop()
                op1 = result.pop()
                result.append(self.calc(i, op1, op2))
        return result

    @staticmethod
    def calc(operator, operand1, operand2):
        if operator == '+':
            return operand1 + operand2
        elif operator == '-':
            return operand1 - operand2
        elif operator == '*':
            return operand1 * operand2
        elif operator == '/':
            return operand1 // operand2
        elif operator == '^':
            return operand1 ** operand2


if __name__ == '__main__':
    Calculator()
