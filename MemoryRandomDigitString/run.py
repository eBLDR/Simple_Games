import argparse

from memory_random_digit_string.manager import Manager


def main():
    parser = argparse.ArgumentParser(description='Memory random digit string')
    parser.add_argument('--level', help='Set specific start level', default=None)

    args = parser.parse_args()

    manager = Manager(start_level=args.level)
    manager.play_round()
    manager.screen.listen()
    manager.screen.mainloop()


if __name__ == '__main__':
    main()
