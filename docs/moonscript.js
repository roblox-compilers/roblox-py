CodeMirror.defineMode("moonscript", function(config, parserConfig) {
    var moonKeywords = parserConfig.keywords || {};
    var moonBuiltins = parserConfig.builtins || {};
    var moonAtoms = parserConfig.atoms || {};
  
    var indentUnit = config.indentUnit;
  
    function prefixRE(words) {
      return new RegExp("^(?:" + words.join("|") + ")\\b");
    }
  
    function wordRE(words) {
      return new RegExp("^(?:" + words.join("|") + "))\\b");
    }
  
    var keywords = prefixRE(Object.keys(moonKeywords));
    var builtins = prefixRE(Object.keys(moonBuiltins));
    var atoms = wordRE(Object.keys(moonAtoms));
  
    var indentStack = [];
  
    function tokenBase(stream, state) {
      var ch = stream.next();
  
      if (ch === "-" && stream.eat("-")) {
        stream.skipToEnd();
        return "comment";
      }
  
      if (ch === "\"" || ch === "'") {
        state.tokenize = tokenString(ch);
        return state.tokenize(stream, state);
      }
  
      if (ch === "[" && stream.match("[")) {
        state.tokenize = tokenLongString();
        return state.tokenize(stream, state);
      }
  
      if (/\d/.test(ch)) {
        stream.eatWhile(/[\w\.]/);
        return "number";
      }
  
      if (ch === ".") {
        if (stream.eat(".")) {
          if (stream.eat(".")) {
            return "operator";
          }
          return "punctuation";
        }
        return "punctuation";
      }
  
      if (ch === "=") {
        if (stream.eat("=")) {
          return "operator";
        }
        return "punctuation";
      }
  
      if (ch === "<" || ch === ">") {
        if (stream.eat("=")) {
          return "operator";
        }
        return "operator";
      }
  
      if (ch === "~") {
        if (stream.eat("=")) {
          return "operator";
        }
        return "punctuation";
      }
  
      if (ch === "+" || ch === "-" || ch === "*" || ch === "/" || ch === "%" || ch === "^") {
        return "operator";
      }
  
      if (ch === "#" || ch === "@" || ch === "$" || ch === "&" || ch === "`") {
        return "punctuation";
      }
  
      if (ch === "{" || ch === "}" || ch === "(" || ch === ")" || ch === "[" || ch === "]") {
        return "bracket";
      }
  
      if (ch === ";" || ch === ",") {
        return "punctuation";
      }
  
      if (/\w/.test(ch)) {
        stream.eatWhile(/\w/);
        var cur = stream.current();
        if (keywords.test(cur)) {
          return "keyword";
        }
        if (builtins.test(cur)) {
          return "builtin";
        }
        if (atoms.test(cur)) {
          return "atom";
        }
        return "variable";
      }
  
      return null;
    }
  
    function tokenString(quote) {
      return function(stream, state) {
        var escaped = false;
        var next;
        while ((next = stream.next()) != null) {
          if (next === quote && !escaped) {
            state.tokenize = tokenBase;
            break;
          }
          escaped = !escaped && next === "\\";
        }
        return "string";
      };
    }
  
    function tokenLongString() {
      return function(stream, state) {
        var bracketCount = 0;
        var next;
        while ((next = stream.next()) != null) {
          if (next === "]" && bracketCount === 2) {
            state.tokenize = tokenBase;
            break;
          }
          if (next === "]") {
            bracketCount++;
          } else {
            bracketCount = 0;
          }
        }
        return "string";
      };
    }
  
    function pushIndent(state, indent) {
      state.indent.push(indent);
    }
  
    function popIndent(state) {
      state.indent.pop();
    }
  
    function topIndent(state) {
      return state.indent[state.indent.length - 1];
    }
  
    return {
      startState: function() {
        return {
          tokenize: tokenBase,
          indent: []
        };
      },
  
      token: function(stream, state) {
        if (stream.eatSpace()) {
          return null;
        }
        var style = state.tokenize(stream, state);
        var currentIndent = topIndent(state);
        if (style === "keyword" && stream.current() === "do") {
          pushIndent(state, currentIndent + indentUnit);
        }
        if (style === "bracket" && stream.current() === "{") {
          pushIndent(state, currentIndent + indentUnit);
        }
        if (style === "bracket" && stream.current() === "}") {
          popIndent(state);
        }
        return style;
      },
  
      indent: function(state, textAfter) {
        if (state.tokenize !== tokenBase) {
          return null;
        }
        var currentIndent = topIndent(state);
        if (/^\s*[\{\[]/.test(textAfter)) {
          return currentIndent;
        }
        if (/^\s*\}/.test(textAfter)) {
          if (state.indent.length > 1) {
            return state.indent[state.indent.length - 2];
          }
          return 0;
        }
        if (/^\s*else/.test(textAfter)) {
          return currentIndent;
        }
        if (/^\s*end/.test(textAfter)) {
          if (state.indent.length > 1) {
            return state.indent[state.indent.length - 2];
          }
          return 0;
        }
        return currentIndent;
      },
  
      lineComment: "--",
      fold: "brace"
    };
  });
  
  CodeMirror.defineMIME("text/x-moonscript", "moonscript");