import re

class Reporter:
    """
    Formats the results of pyflakes checks to users.
    """
    def __init__(self):
        self.diagnostics = []

    def unexpectedError(self, filename, msg):
        """
        An unexpected error occurred attemptinh to process C{filename}.

        @param filename: The path to a file that we could not process.
        @ptype filename: C{unicode}
        @param msg: A message explaining the problem.
        @ptype msg: C{unicode}
        """
        self.diagnostics.append(f"1{filename}: {msg}\n")

    def syntaxError(self, filename, msg, lineno, offset, text):
        """
        There was a syntax error in C{filename}.

        @param filename: The path to the file with the syntax error.
        @ptype filename: C{unicode}
        @param msg: An explanation of the syntax error.
        @ptype msg: C{unicode}
        @param lineno: The line number where the syntax error occurred.
        @ptype lineno: C{int}
        @param offset: The column on which the syntax error occurred, or None.
        @ptype offset: C{int}
        @param text: The source code containing the syntax error.
        @ptype text: C{unicode}
        """
        if text is None:
            line = None
        else:
            line = text.splitlines()[-1]

        # lineno might be None if the error was during tokenization
        # lineno might be 0 if the error came from stdin
        lineno = max(lineno or 0, 1)

        if offset is not None:
            # some versions of python emit an offset of -1 for certain encoding errors
            offset = max(offset, 1)
            self.diagnostics.append('1%s:%d:%d: %s\n' %
                               (filename, lineno, offset, msg))
        else:
            self.diagnostics.append('1%s:%d: %s\n' % (filename, lineno, msg))

        if line is not None:
            self.diagnostics.append(line)
            self.diagnostics.append('\n')
            if offset is not None:
                self.diagnostics.append(re.sub(r'\S', ' ', line[:offset - 1]) +
                                   "^\n")

    def flake(self, message):
        """
        pyflakes found something wrong with the code.

        @param: A L{pyflakes.messages.Message}.
        """
        self.diagnostics.append("2"+str(message))
        self.diagnostics.append('\n')
