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
    epilog=(
        "Примеры:\n"
        '  python -m toolkit calc "2+7*8"\n'
        "  python -m toolkit convert 100 --from mm --to m"
    ),
    formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # calc: выражение
    calc = subparsers.add_parser("calc", help="Вычислить выражение")
    calc.add_argument(
        "expression",
        help="Арифметическое выражение",
    )

    # convert: значение + два флага
    conv = subparsers.add_parser("convert", help="Конвертировать величину")
    conv.add_argument("value", help="Числовое значение")
    conv.add_argument("--from", dest="from_unit", required=True,
                      help="Исходная единица")
    conv.add_argument("--to", dest="to_unit", required=True,
                      help="Целевая единица")

    return parser


def main(argv: list[str] | None = None) -> None:
    """Точка входа CLI."""
    parser = command_parser()
    args, extra = parser.parse_known_args(argv)

    if args.command == "calc":
        parts = list(args.expression) + list(extra)
        expression = " ".join(parts)
        if not expression.strip():
            parser.error("calc: не указано выражение")
        result = calculate(expression)
        if str(result)[-2:] == ".0":
            result = str(result)[:-2]
    else:
        result = convert(args.value, args.from_unit, args.to_unit)

    print(result)


if __name__ == "__main__":
    try: 
        main()
    except ToolkitError as e:
        print(e.__class__, e, file=sys.stderr)
        sys.exit(2)
    