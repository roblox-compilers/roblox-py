import sys

VERSION = "3.0.0"
TAB = "\t\b\b\b\b"

def warn(msg):
    print("\033[1;33m" + "warning: " + "\033[0m" + msg)
def info(msg):
    print("\033[1;32m" + "info: " + "\033[0m" + msg)
def error(msg):
    print("\033[1;31m" + "error: " + "\033[0m" + msg)
    sys.exit()
    
def usage():
    print("\n"+f"""usage: rbxpy [options]
Available options are:
{tab}-o file   output to 'file' (as a file or directory if -d is used)
{tab}-i file   input from 'file'
{tab}-d        compile all files in current directory 
{tab}-w        watch mode (directory only)
{tab}-v        show version information
{tab}-vd       show version number only""")
    sys.exit()

def version():
    print("\033[1;34m" + "copyright:" + "\033[0m" + " roblox-pyc " + "\033[1m" + VERSION + "\033[0m" + " licensed under the GNU Affero General Public License by " + "\033[1m" + "@AsynchronousAI" + "\033[0m")
    os.exit(0)

arg = sys.argv
if (arg): # being run through interpreter or AOT compiler
    if (len(arg) < 1):
        print("rbxpy: no arguments provided")
        usage()
    
    flags = {}
    for v in (arg):
        if (v[1] == "-") :
            flags[len(flags)+1] = v
        else:
            warn("Unhandled argument: " + v)

    # Run flags 
    mode = "none"
    input = ""
    output = ""
    capture = False
    
    for v in (flags):
        if capture:
            capture = False
            continue
        
        if (v == "-h" or v == "--help"):
            usage()
        elif (v == "-v" or v == "--version"):
            version()
        elif (v == "-vd"):
            print(VERSION)
        elif (v == "-w"):
            mode = "watch"
        elif (v == "-o"):
            capture = True
            mode = "output"
            output = flags[i+1]
        elif not capture:
            input = v
    
    
    # Operate mode
    if (mode == "none"):
        error("No mode specified")
else: # being run through the interpreter
    print("rbxpy: no arguments provided")
    usage()