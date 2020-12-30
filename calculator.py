from collections import deque
from sys import exit
import re

class Calculator:
    def __init__(self):
        self.split_inp = None
        self.digits = None
        self.ops = None
        self.stack = None
        self.vars = dict()
        self.operators = {'+', '-', '*', '/', '(', ')', '^'}  # set of operators
        self.priority = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}  # dictionary having priorities
        self.main()

    @staticmethod
    def check_command(inp):
        if inp == '/exit':
            print('Bye!')
            exit()
        if inp == '/help':
            print('The calculator supports addition and subtraction where -- equals +')
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

    def assign_values(self):
        if self.vars:
            for key in self.split_inp:
                if key in self.vars:
                    i = self.split_inp.index(key)
                    self.split_inp[i] = self.vars[key]

    def get_digits(self):
        self.digits = [int(n) for n in self.split_inp if n.lstrip('-+').isdigit()]

    def get_operators(self):
        raw_ops = [op for op in self.split_inp if not op[-1].isdigit() and '-' in op or '+' in op or '*' in op]
        self.ops = ['+' if len(op) % 2 == 0 and '+' not in op else op[0] for op in raw_ops]  # -- becomes +

    """def convert_to_stack(self):
        for i in self.digits + self.ops:
            if not self.stack or self.stack[-1] == '(':
                self.stack += i
            elif i in '()*/' and self.stack[-1] in '+-':
                self.stack += i
            """

    def infix_to_postfix(self, raw_input):  # input expression
        stack = []  # initially stack empty
        output = []  # initially output empty
        #print("RAW", raw_input.split())
        #output = [num for num in re.findall(r"\d+", raw_input)]
        #print(output)
        #for i in output:
        #    raw_input = re.sub('i', '', raw_input)
        #print(raw_input.split())
        #for ch in raw_input.split():
        for ch in raw_input.split():
            #if not ch.isdigit() and ch != ' ':
            #print(ch)
            if ch not in self.operators:  # if an operand then put it directly in postfix expression
            #    print(ch)
                output.append(ch)
                #print(output)
            elif ch == '(':  # else operators should be put in stack
            #elif ch.startswith('('):
                stack.append('(')
            #    print(stack)
            elif ch == ')':
            #if ch.startswith(')'):
                while stack and stack[-1] != '(':
                    output += stack.pop()
            #        print(stack)
                stack.pop()
            #    print(stack)
            else:
                # lesser priority can't be on top on higher or equal priority
                # so pop and put in output
                while stack and stack[-1] != '(' and self.priority[ch] <= self.priority[stack[-1]]:
                    output += stack.pop()
            #        print(stack)
                stack.append(ch)
            #print(output)
            #print(stack)
        while stack:
            output += stack.pop()
        #print(output)
        #new = []
        #for i in output:
            #print(i)
        #    if i.isdigit() or i in self.operators:
                #output.remove(i)
        #        new += i
        #print(new)
        return output

    def compute(self):
        last_num = None
        while self.digits and self.ops:
            if last_num is None:
                last_num = self.digits.pop()
            operation = self.ops.pop()
            second = self.digits.pop()
            if operation == '+':
                last_num += second
            elif operation == '-':
                last_num -= second
        if last_num is not None:
            print(last_num)
        else:
            print('Invalid expression')

    def compute_postfix(self, post_expr):
        result = []
        #print(post_expr.strip())
        for i in post_expr:
            #print(i)
            #if i == ' ':
            #    continue
            if i.isdigit():
                result.append(int(i))
            elif i in self.vars:
                result.append(int(self.vars[i]))
                #print("VAR", result)
            elif i in self.operators:
                if i == '+':
                    result.append(result.pop() + result.pop())
                elif i == '-':
                    b = result.pop()
                    a = result.pop()
                    result.append(a - b)
                elif i == '*':
                    result.append(result.pop() * result.pop())
                elif i == '/':
                    b = result.pop()
                    a = result.pop()
                    #if a % b == 0:
                    #    result.append(int(a / b))
                    result.append(a // b)
                elif i == '^':
                    b = result.pop()
                    a = result.pop()
                    result.append(a ** b)
            #print(result)
        return result

    def main(self):
        while True:
            inp = input()
            out = ''.join(inp.split())
            while '++' in out:
                out = out.replace('++', '+')
            while '---' in out:
                out = out.replace('---', '-')
            while '--' in out:
                out = out.replace('--', '+')

            if '+' in out:
                out = out.replace('+', ' + ')
            if '-' in out:
                out = out.replace('-', ' - ')
            if '*' in out:
                out = out.replace('*', ' * ')
            if '/' in out:
                out = out.replace('/', ' / ')
            if '(' in out:
                out = out.replace('(', ' ( ')
            if ')' in out:
                out = out.replace(')', ' ) ')
            else:
                out = out
            out = out.replace('  ', ' ')
            #inp = out.split()
            #print(out)
            #print(type(out))
            #inp = input().strip()
            #inp = input().replace(" ", "")
            #print(inp)
            #inp2 = []
            #for i in self.operators:
            #    inp2 = inp.replace(i, ' {} '.format(i))
            #print(inp2)
            #inp2 = [n for n in re.findall(r"[\+\-\*/\(\)^]", inp)]
            if inp.startswith('/'):
                self.check_command(inp)
                continue
            self.split_inp = out.split()
            if not out:
                continue
            elif '=' in out:  # adding variables
                self.get_vars(out)
                continue
            else:

                if self.split_inp.count('(') != self.split_inp.count(')'):
                    print("Invalid expression")
                    continue
                restart = False
                for a, b in zip(self.split_inp, self.split_inp[1:]):
                    if a == '/' and b == '/' or a == '*' and b == '*':
                        print("Invalid expression")
                        restart = True
                        break
                if restart:
                    continue
                if len(self.split_inp) == 1 and self.split_inp[0] not in self.vars:
                    print('Unknown variable')

                self.assign_values()
                self.get_digits()
                if len(self.digits) == 1:
                    print(self.digits[0])
                    continue
                #print(self.digits)
                self.get_operators()
                #print(self.ops)
                #self.convert_to_stack()
                #inp = inp.strip()
                #print(inp)
                res = self.infix_to_postfix(out)
                #print(res)
                print(*self.compute_postfix(res))


if __name__ == '__main__':
    Calculator()
