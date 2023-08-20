import sys

def red(text, styles = []):
    return color(text, 31, styles)
def green(text, styles = []):
    return color(text, 32, styles)
def yellow(text, styles = []):
    return color(text, 33, styles)
def blue(text, styles = []):
    return color(text, 34, styles)
def magenta(text, styles = []):
    return color(text, 35, styles)
def cyan(text, styles = []):
    return color(text, 36, styles)
def white(text, styles = []):
    return color(text, 37, styles)
def rainbow_text(text, end = ""):
    colors = ['\033[31m', '\033[33m', '\033[32m', '\033[36m', '\033[34m', '\033[35m']
    i = 0
    for char in text:
        print(colors[i % len(colors)] + char, end='')
        i += 1
    print('\033[0m', end=end)
def nil(text=""):
    return
def color(text, color, styles = []):
    style = ""
    for s in styles:
        if s == "bold":
            style += "1;"
        elif s == "underline":
            style += "4;"
        elif s == "reverse":
            style += "7;"
        elif s == "concealed":
            style += "8;"
    return "\033["+style+str(color)+"m"+text+"\033[0m"