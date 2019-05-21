import sys
from checkWithOriginal import lex

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

def astnode(nodetype, **args):
    return dict(nodetype=nodetype, **args)

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

def parser(toks):

    #change iterator to the next token and delete it
    def consume(tok_type):
        if tok_type == toks[0]["toktype"]:
            t = toks.pop(0)
            return t
        else:
            error("expected %d, found %d" % (tok_type, toks[0]["toktype"]))

    def peek():
        if toks:
            return toks[0]["toktype"]
        else:
            return None

    def program():
        ds = decls()
        sts = stmts()
        return {
            "decls": ds,
            "stmts": sts,
        }

    def decls():
        decls = []
        while peek() == TOK_VAR:
            decls.append(decl())
        return decls

    def decl():
        if peek() == TOK_VAR:
            consume(TOK_VAR)
            id = consume(TOK_ID)
            consume(TOK_COLON)
            ty = consume(TOK_TYPE)
            return astnode(AST_DECL, id=id["value"], type=ty["value"])
        else:
            error("not a valid declaration")

    def stmts():
        stmts = []
        while peek() in (TOK_PRINT, TOK_READ, TOK_ID, TOK_WHILE):
            stmts.append(stmt())
        return stmts

    def stmt():
        next_tok = peek()
        if next_tok == TOK_ID:
            id = consume(TOK_ID)
            consume(TOK_ASS)
            e = expr()
            return astnode(AST_ASSIGN, lhs=id["value"], rhs=e)
        elif next_tok == TOK_PRINT:
            consume(TOK_PRINT)
            e = expr()
            return astnode(AST_PRINT, expr=e)
        elif next_tok == TOK_READ:
            consume(TOK_READ)
            id = consume(TOK_ID)
            return astnode(AST_READ, id=id)
        elif next_tok == TOK_WHILE:
            consume(TOK_WHILE)
            e = expr()  # a
            consume(TOK_DO)
            body = stmts()
            consume(TOK_DONE)
            return astnode(AST_WHILE, expr=e, body=body)
        else:
            error("illegal statement")

    def expr():
        t = term()
        print(t)
        next_tok = peek()
        while next_tok in (TOK_PLUS, TOK_MINUS):
            if next_tok == TOK_PLUS:
                consume(TOK_PLUS)
                t2 = term()
                t = astnode(AST_BINOP, op="+", lhs=t, rhs=t2)
            elif next_tok == TOK_MINUS:
                consume(TOK_MINUS)
                t2 = term()
                t = astnode(AST_BINOP, op="-", lhs=t, rhs=t2)
            next_tok = peek()
        return t

    def term():
        c = costam()       # ast_id a
        print(c)
        next_tok = peek()    # 21 >
        while next_tok in (TOK_STAR, TOK_SLASH):
            if next_tok == TOK_STAR:
                consume(TOK_STAR)
                c2 = costam()
                c = astnode(AST_BINOP, op="*", lhs=c, rhs=c2)
            elif next_tok == TOK_SLASH:
                consume(TOK_SLASH)
                c2 = costam()
                c = astnode(AST_BINOP, op="/", lhs=c, rhs=c2)
            next_tok = peek()
        return c

    def costam():
        f = factor()
        next_tok = peek()
        while next_tok in (TOK_LESS, TOK_MORE, TOK_EQ):
            if next_tok == TOK_LESS:
                consume(TOK_LESS)
                f2 = factor()
                f = astnode(AST_BINOP, op="<", lhs=f, rhs=f2)
            elif next_tok == TOK_MORE:
                consume(TOK_LESS)
                f2 = factor()
                f = astnode(AST_BINOP, op=">", lhs=f, rhs=f2)
            elif next_tok == TOK_EQ:
                consume(TOK_LESS)
                f2 = factor()
                f = astnode(AST_BINOP, op="==", lhs=f, rhs=f2)

        return f

    def factor():
        next_tok = peek()
        if next_tok == TOK_LPAREN:
            consume(TOK_LPAREN)
            e = expr()
            consume(TOK_RPAREN)
            return e
        elif next_tok == TOK_INT:
            tok = consume(TOK_INT)
            return astnode(AST_INT, value=tok["value"])
        elif next_tok == TOK_FLOAT:
            tok = consume(TOK_FLOAT)
            return astnode(AST_FLOAT, value=tok["value"])
        elif next_tok == TOK_ID:
            tok = consume(TOK_ID)
            return astnode(AST_ID, name=tok["value"])
        else:
            error("illegal token %d" % next_tok)

    return program()

curr_tmp = 0
def codegen(ast, symtab):

    def new_temp():
        """Return a new, unique temporary variable name."""
        global curr_tmp
        curr_tmp += 1
        return "t_" + str(curr_tmp)

    variables = []
    def gen_stmt(stmt):
        if stmt["nodetype"] == AST_ASSIGN:
            expr_loc = gen_expr(stmt["rhs"])
            if stmt["lhs"] in variables:
                print("%s = %s" % (stmt["lhs"], expr_loc))
            else:
                variables.append(stmt["lhs"])
                print("let %s = %s" % (stmt["lhs"], expr_loc))
        elif stmt["nodetype"] == AST_PRINT:
            expr_loc = gen_expr(stmt["expr"])
            print('console.log(' + expr_loc + ')')
        # elif stmt["nodetype"] == AST_READ:
        #     id = stmt["id"]["value"]
        #     if symtab[id] == "int":
        #         flag = "d"
        #     else:
        #         flag = "f"
        #     print('scanf("%%%s", &%s);' % (flag, id))
        elif stmt["nodetype"] == AST_WHILE:
            expr_loc = gen_expr(stmt["expr"])
            print("while (%s) { " % expr_loc)
            for body_stmt in stmt["body"]:
                gen_stmt(body_stmt)
            gen_expr(stmt["expr"], expr_loc)
            print("}")

    def gen_expr(expr, loc_name=None):
        if expr["nodetype"] in (AST_INT, AST_FLOAT):
            loc = loc_name or new_temp()
            print("let %s = %s;" % ( loc, expr["value"]))
            return loc
        elif expr["nodetype"] == AST_ID:
            return expr["name"]
        elif expr["nodetype"] == AST_BINOP:
            lhs_loc = gen_expr(expr["lhs"])
            rhs_loc = gen_expr(expr["rhs"])
            loc = new_temp()
            print("let %s = %s %s %s;" % ( loc, lhs_loc, expr["op"], rhs_loc))
            return loc

    # Add the usual C headers and main declaration.


    # Add the C statements to the main function.
    for stmt in ast["stmts"]:
        gen_stmt(stmt)


def main():
    with open('demo.txt') as f:
        read_data = f.read()

    with open('demo2.txt') as f:
        read_data2 = f.read()
    # print(lexer(read_data))
    ast = parser(lexer(read_data))
    print(ast)
    # codegen(ast, {'a':'int'})

if __name__ == "__main__":
    main()

