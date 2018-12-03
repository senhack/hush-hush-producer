#!/usr/bin/env python3
import time
import hush


def main():
    hush.start("hush.conf")

    keep_running = True
    while keep_running:
        try:
            time.sleep(1)

        except KeyboardInterrupt:
            keep_running = False
            hush.stop()


if __name__ == '__main__':
    main()
