import argparse
import logging
import src.constants as cst
from src.nam import NAM

def main():
    logger = logging.getLogger(__name__)
    nam_object = NAM(filepath=args.filepath, skip_whitespaces=args.ignore_whitespaces, max_iterations=args.max_iterations)
    nam_object.parse_file()
    while True:
        try:
            line = input("Input line: ")
            result = nam_object.apply(line)
            logger.info(f"Result: {result}")
        except (KeyboardInterrupt, EOFError):
            print("\nBye!")
            break

if __name__ == '__main__':

    logging.basicConfig(
        level=cst.LOG_LEVEL,
        handlers = cst.HANDLERS,
        format = cst.FORMAT,
    )

    parser = argparse.ArgumentParser(
        description=
        """
        NAM emulator. Syntax:
        - a->b: replaces first encountered 'a' with 'b'

        - "a->b
           b->c": first will try to replace 'a' with 'b'. If no 'a' is found, will try to replace 'b' with 'c'. If not found, stops emulator

        - a->.b: replaces first encountered 'a' with 'b' ans stops emulator
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument('filepath', type=str, help='Path to file with rules')
    parser.add_argument('--ignore-whitespaces', "-iw", help='Will ignore whitespaces in rules', action='store_true')
    parser.add_argument('--max_iterations', "-mi", help='Maximum iterations', type=int, default=128)
    args = parser.parse_args()

    main()