import sys

# Token types
TOK_PRINT  = 0
TOK_ID     = 1
TOK_VAR    = 2
TOK_INT    = 3
TOK_FLOAT  = 4
TOK_TYPE   = 5
TOK_ASS    = 6
TOK_PLUS   = 7
TOK_MINUS  = 8
TOK_STAR   = 9
TOK_SLASH  = 10
TOK_LPAREN = 11
TOK_RPAREN = 12
TOK_COLON  = 13
TOK_WHILE  = 14
TOK_DO     = 15
TOK_DONE   = 16
TOK_SEMI   = 17
TOK_READ   = 18
TOK_EQ     = 19
TOK_LESS   = 20
TOK_MORE   = 21

# AST nodes
AST_DECL   = 0
AST_ASSIGN = 1
AST_PRINT  = 2
AST_INT    = 3
AST_FLOAT  = 4
AST_ID     = 5
AST_BINOP  = 6
AST_WHILE  = 7
AST_READ   = 8

def error(msg):
    print("Error: " + msg)
    sys.exit(1)

def tok(type, value):
    return { "toktype": type, "value": value }

def lexer(code):
    i = 0
    tokens = []
    len_of_code = len(code)
    while i < len(code):
        el = code[i]

        if el.isspace():
            pass

        elif el == "(":              # komentarz lub przypisanie
            i += 1
            if code[i] == "☯":
                while i < len_of_code and code[i] != "\n":
                    i += 1
            elif code[i] == "^":
                i += 6
                tokens.append(tok(TOK_ASS, None))

        elif el == '✿':
            tokens.append(tok(TOK_PLUS, None))
        elif el == "❤":
            tokens.append(tok(TOK_MINUS, None))
        elif el == "✰":
            tokens.append(tok(TOK_STAR, None))
        elif el == "๑":
            tokens.append(tok(TOK_SLASH, None))
        elif el == "{":
            tokens.append(tok(TOK_LPAREN, None))
        elif el == "}":
            tokens.append(tok(TOK_RPAREN, None))

        # ew dodaj dwukropek, średnik

        elif el.isdigit():
            number = ""

            while i < len_of_code and code[i].isdigit():
                number += code[i]
                i += 1
            if i < len_of_code and code[i] == ".":
                number += "."
                i += 1

                while i < len_of_code and code[i].isdigit():
                    number += code[i]
                    i += 1

                tokens.append(tok(TOK_FLOAT, float(number)))

            else:
                tokens.append(tok(TOK_INT, int(number)))
            i -= 1



        elif el == "φ":
            i += 4
            tokens.append(tok(TOK_PRINT, None))

        elif el == "<":
            i += 12
            tokens.append(tok(TOK_WHILE, None))

        elif el == "_":
            i += 12
            tokens.append(tok(TOK_DO, None))

        elif el == "ʢ":
            i += 4
            tokens.append(tok(TOK_DONE, None))

        elif el == "ʕ":
            i += 1
            if code[i] == "•":
                tokens.append(tok(TOK_EQ, None))
            elif code[i] == "ₒ":
                tokens.append(tok(TOK_LESS, None))
            elif code[i] == "'":
                tokens.append(tok(TOK_MORE, None))
            i += 3

        elif el.isalpha():
            str = ""
            while code[i].isalnum() or code[i] == "_":
                str += code[i]
                i += 1

            tokens.append(tok(TOK_ID, str))
        else:
            error("It seems that I don't understand that char: " + el)
        i += 1
        # ew VAR, TYPE, READ?

    return tokens


def main():
    with open('demo.txt') as f:
        read_data = f.read()

    print(lexer(read_data))

if __name__ == "__main__":
    main()

