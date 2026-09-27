import argparse
import sys

from toolkit.calculator import calculate
from toolkit.converter import convert
from toolkit.errors import ToolkitError


def command_parser() -> argparse.ArgumentParser:
    """Собирает парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        prog="toolkit",
        description="Калькулятор и конвертер величин",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Подкоманда calc: один позиционный аргумент
    calc = subparsers.add_parser("calc", help='Вычислить выражение, python -m toolkit calc "EXPRESSION"')
    calc.add_argument("expression", nargs=argparse.REMAINDER, help="Арифметическое выражение")

    # Подкоманда convert: значение + два именованных флага
    conv = subparsers.add_parser("convert", help="Конвертировать величину, python -m toolkit convert VALUE --from UNIT --to UNIT")
    conv.add_argument("value", help="Числовое значение")
    conv.add_argument("--from", dest="from_unit", required=True,
                      help="Исходная единица")
    conv.add_argument("--to", dest="to_unit", required=True,
                      help="Целевая единица")

    return parser

def main() -> None:
    parser = command_parser()
    args = parser.parse_args()

    try:
        if args.command == "calc":
            if not args.expression:
                print("Ошибка: не указано выражение", file=sys.stderr)
                sys.exit(2)
            if len(args.expression) > 1:
                print("Ошибка: слишком много аргументов", file=sys.stderr)
                sys.exit(2)
            result = calculate(args.expression)
        elif args.command == "convert":
            result = convert(args.value, args.from_unit, args.to_unit)
        else:
            print(f"Ошибка: неизвестная команда {args.command!r}",
                  file=sys.stderr)
            sys.exit(2)
    except ToolkitError as e:
        print(e.__class__,e, file=sys.stderr)
        sys.exit(2)

    print(result)
    

if __name__ == "__main__":
    main()
