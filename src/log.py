import sys


def error(msg):
    print("\033[91;1merror\033[0m \033[90mPY roblox-py:\033[0m " + msg)
    sys.exit(1)


def warn(msg):
    sys.stderr.write(
        "\033[1;33m"
        + "warning: "
        + "\033[0m"
        + "\033[90mPY roblox-py:\033[0m "
        + msg
        + "\n"
    )


def info(msg):
    sys.stderr.write(
        "\033[1;32m"
        + "info: "
        + "\033[0m"
        + "\033[90mPY roblox-py:\033[0m "
        + msg
        + "\n"
    )
