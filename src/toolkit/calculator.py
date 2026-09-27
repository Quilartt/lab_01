from .errors import (
    DivisionByZero,
    EmptyExpression,
    InvalidNumber,
    MissingOperand,
    MissingOperator,
    TwoOperators,
    UnknownSymbol,
)


def tokenize_fsm(expr: str) -> list[tuple[str, float | str]]:
    """Переводит арифметическое выражение в токены"""
    tokens = []
    state = "START"
    current_token = ""

    for char in expr:
        # Начальная обработка: пропускаем пробелы, начинаем число или знак
        if state == "START":
            if char.isspace():
                continue
            if char.isdigit():
                state = "NUMBER"
                current_token = char
            elif char in ["+", "-", "*", "/"]:
                tokens.append(("OP", char))
            else:
                raise UnknownSymbol(f"Недопустимый символ: {char}")

        elif state == "NUMBER":
            # Собираем число
            if char.isspace():
                if current_token[-1] == ".":
                    raise InvalidNumber(f"Недопустимое число: {current_token}")
                else:
                    tokens.append(("NUMBER", float(current_token)))
                    state = "START"
                    current_token = ""
            elif char.isdigit():
                current_token += char
            elif char in ["-", "+", "/", "*"]:
                if current_token[-1] == ".":
                    raise InvalidNumber(f"Недопустимое число: {current_token}")
                else:
                    tokens.append(("NUMBER", float(current_token)))
                    tokens.append(("OP", char))
                    current_token = ""
                    state = "START"
            elif char == ".":
                if current_token.count(".") < 1:
                    current_token += char
                else:
                    raise InvalidNumber(f"Недопустимое число: {current_token+char}")
            else:
                raise UnknownSymbol(f"Недопустимый символ: {char}")

    # Завершающая обработка
    if state == "NUMBER":
        if current_token[-1] == ".":
            raise InvalidNumber(f"Недопустимое число: {current_token}")
        else:
            tokens.append(("NUMBER", float(current_token)))

    if len(tokens) > 0:
        return tokens
    else:
        raise EmptyExpression("Пустая строка ввода")


def validate_tokens(tokens: list[tuple[str, float | str]]) -> list[tuple[str, float | str]]:
    """Проверка синтаксиса и разметка унарных знаков"""
    res_tokens = []
    prev = ""
    count_numbers = 0
    for typ, value in tokens:
        if typ == "NUMBER":
            if prev == "NUMBER":
                raise MissingOperator("Пропущен оператор между числами")

            res_tokens.append(("NUMBER", value))
            count_numbers += 1
        
        # Выделение унарных операций
        if typ == "OP":
            if value in "-+" and (prev == "" or prev == "OP"):
                res_tokens.append(("OP", "u" + value))
            elif prev == "OP":
                raise TwoOperators(f"Недопустимая операция: {value}")
            elif prev == "":
                raise MissingOperand("Пропущен операнд в начале выражения")
            else:
                res_tokens.append(("OP", value))
        prev = typ

    if count_numbers == 0:
        raise EmptyExpression("Выражение не содержит чисел")
    
    if prev == "OP":
        raise MissingOperand("Пропущен операнд в конце выражения")

    return res_tokens



MY_DICT = {"u+": 3, "u-": 3, "*": 2, "/": 2, "+": 1, "-": 1}


def to_rpn(tokens: list[tuple[str, float | str]]) -> list[float | str]:
    """Перевод в обратную польскую нотацию (RPN) алгоритмом Дейкстры"""

    my_stack = []
    output = []
    for char in tokens:
        if char[0] == "NUMBER":
            output.append(char[1])
        elif char[0] == "OP":
            if char[1] in {"u+", "u-"}:
                while my_stack and MY_DICT[my_stack[-1]] > MY_DICT[char[1]]:
                    output.append(my_stack.pop())
            else:
                while my_stack and MY_DICT[my_stack[-1]] >= MY_DICT[char[1]]:
                    output.append(my_stack.pop())

            my_stack.append(char[1])

    # Завершающая обработка
    while my_stack:
        output.append(my_stack.pop())
    return output


def eval_rpn(rpn_expr: list[float | str]) -> float:
    """Вычисление значения постфиксного выражения"""

    my_stack = []
    # Вычисление через стек
    for char in rpn_expr:
        if isinstance(char, float):
            my_stack.append(char)
        elif char == "u-":
            my_stack.append(-my_stack.pop())
        elif char == "u+":
            pass
        else:
            b = my_stack.pop()
            a = my_stack.pop()
            if char == "+":
                my_stack.append(a + b)
            elif char == "-":
                my_stack.append(a - b)
            elif char == "*":
                my_stack.append(a * b)
            elif char == "/":
                if b == 0:
                    raise DivisionByZero(f"Деление на 0 недопустимо: {a}/{b}")
                else:
                    my_stack.append(a / b)
    return my_stack[0]


def calculate(expression: str) -> float:
    """Связывает токенизацию, валидацию, перевод в RPN и финальный расчет выражения"""

    tokens = tokenize_fsm(expression)
    tokens = validate_tokens(tokens)
    rpn = to_rpn(tokens)

    return eval_rpn(rpn)
     
