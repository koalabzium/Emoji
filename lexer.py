import sys

# Token types
TOK_PRINT = 0
TOK_ID = 1
TOK_VAR = 2
TOK_INT = 3
TOK_FLOAT = 4
TOK_STR = 5
TOK_ASS = 6
TOK_ADD = 7
TOK_SUB = 8
TOK_MUL = 9
TOK_DIV = 10
TOK_LPAREN = 11
TOK_RPAREN = 12
TOK_IF = 13
TOK_WHILE = 14
TOK_DO = 15
TOK_END = 16
TOK_END_IF = 17
TOK_READ = 18
TOK_EQ = 19
TOK_LESS = 20
TOK_MORE = 21
TOK_THEN = 22

# AST nodetypes
AST_DECL = 0
AST_ASSIGN = 1
AST_PRINT = 2
AST_INT = 3
AST_FLOAT = 4
AST_ID = 5
AST_BINOP = 6
AST_WHILE = 7
AST_STR = 8
AST_COND = 9
AST_IF = 10


def error(msg):
    print("Error: " + msg)
    sys.exit(1)


def tok(type, value):
    return {"toktype": type, "value": value}


def astnode(nodetype, **args):
    return dict(nodetype=nodetype, **args)


def lexer(code):
    i = 0
    tokens = []
    len_of_code = len(code)
    while i < len_of_code:
        el = code[i]

        if el.isspace():
            pass

        elif el == "(":
            i += 1
            if code[i] == "☯":
                while i < len_of_code and code[i] != "\n":
                    i += 1
            elif code[i] == " ":
                i += 5
                tokens.append(tok(TOK_PRINT, None))
            elif code[i] == "•":
                i += 6
                tokens.append(tok(TOK_IF, None))

        elif el == "ᕕ":
            i += 6
            tokens.append(tok(TOK_THEN, None))

        elif el == "¯":
            i += 8
            tokens.append(tok(TOK_END_IF, None))

        elif el == "＼":
            i += 6
            tokens.append(tok(TOK_ASS,None))

        elif el == '✿':
            tokens.append(tok(TOK_ADD, None))
        elif el == "❤":
            tokens.append(tok(TOK_SUB, None))
        elif el == "✰":
            tokens.append(tok(TOK_MUL, None))
        elif el == "๑":
            tokens.append(tok(TOK_DIV, None))
        elif el == "{":
            tokens.append(tok(TOK_LPAREN, None))
        elif el == "}":
            tokens.append(tok(TOK_RPAREN, None))

        elif el == "☆":
            string = ""
            i += 6
            while code[i] != "☆":
                string += code[i]
                i += 1
            i += 5
            tokens.append(tok(TOK_STR, string))

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

        elif el == "<":
            i += 12
            tokens.append(tok(TOK_WHILE, None))

        elif el == "_":
            i += 12
            tokens.append(tok(TOK_DO, None))

        elif el == "ʢ":
            i += 4
            tokens.append(tok(TOK_END, None))

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

    return tokens


def parser(toks):
    def consume_next_tok(tok_type):
        if tok_type == toks[0]["toktype"]:
            t = toks.pop(0)
            return t
        else:
            error("I expected %d, but found %d" % (tok_type, toks[0]["toktype"]))

    def peek_next_tok():
        if toks:
            return toks[0]["toktype"]
        else:
            return None

    def start():
        sts = get_statements()
        return {
            "stmts": sts,
        }

    def get_statements():
        stmts = []
        while peek_next_tok() in (TOK_PRINT, TOK_ID, TOK_WHILE, TOK_IF):
            stmts.append(get_single_stmt())
        return stmts

    def get_single_stmt():
        next_tok = peek_next_tok()
        if next_tok == TOK_ID:
            id = consume_next_tok(TOK_ID)
            consume_next_tok(TOK_ASS)
            e = expr()
            return astnode(AST_ASSIGN, left=id["value"], right=e)
        elif next_tok == TOK_PRINT:
            consume_next_tok(TOK_PRINT)
            e = expr()
            return astnode(AST_PRINT, expr=e)

        elif next_tok == TOK_WHILE:
            consume_next_tok(TOK_WHILE)
            e = condition()
            consume_next_tok(TOK_DO)
            body = get_statements()
            consume_next_tok(TOK_END)
            return astnode(AST_WHILE, expr=e, body=body)

        elif next_tok == TOK_IF:
            consume_next_tok(TOK_IF)
            c = condition()
            consume_next_tok(TOK_THEN)
            body = get_statements()
            consume_next_tok(TOK_END_IF)
            return astnode(AST_IF, expr=c, body=body)


        else:
            error("illegal statement")

    def condition():
        left = expr()
        next_tok = peek_next_tok()
        if next_tok == TOK_EQ:
            consume_next_tok(TOK_EQ)
            right = expr()
            return astnode(AST_COND, op="==", left=left, right=right)
        elif next_tok == TOK_MORE:
            consume_next_tok(TOK_MORE)
            right = expr()
            return astnode(AST_COND, op=">", left=left, right=right)
        elif next_tok == TOK_LESS:
            consume_next_tok(TOK_LESS)
            right = expr()
            return astnode(AST_COND, op="<", left=left, right=right)
        return left
        # consume_next_tok(TOK_END_COND)


    def expr():
        t = term()
        next_tok = peek_next_tok()
        while next_tok in (TOK_ADD, TOK_SUB):
            if next_tok == TOK_ADD:
                consume_next_tok(TOK_ADD)
                t2 = term()
                t3 = astnode(AST_BINOP, op="+", left=t, right=t2)
                t = t3
            elif next_tok == TOK_SUB:
                consume_next_tok(TOK_SUB)
                t2 = term()
                t3 = astnode(AST_BINOP, op="-", left=t, right=t2)
                t = t3
            next_tok = peek_next_tok()
        return t

    def term():
        f = factor()  # ast_id a
        next_tok = peek_next_tok()  # 21 >
        while next_tok in (TOK_MUL, TOK_DIV):
            if next_tok == TOK_MUL:
                consume_next_tok(TOK_MUL)
                f2 = factor()
                f3 = astnode(AST_BINOP, op="*", left=f, right=f2)
                f = f3
            elif next_tok == TOK_DIV:
                consume_next_tok(TOK_DIV)
                f2 = factor()
                f3 = astnode(AST_BINOP, op="/", left=f, right=f2)
                f = f3
            next_tok = peek_next_tok()
        return f



    def factor():
        next_tok = peek_next_tok()
        if next_tok == TOK_LPAREN:
            consume_next_tok(TOK_LPAREN)
            e = expr()
            consume_next_tok(TOK_RPAREN)
            return e
        elif next_tok == TOK_INT:
            tok = consume_next_tok(TOK_INT)
            return astnode(AST_INT, value=tok["value"])
        elif next_tok == TOK_FLOAT:
            tok = consume_next_tok(TOK_FLOAT)
            return astnode(AST_FLOAT, value=tok["value"])
        elif next_tok == TOK_ID:
            tok = consume_next_tok(TOK_ID)
            return astnode(AST_ID, name=tok["value"])
        elif next_tok == TOK_STR:
            tok = consume_next_tok(TOK_STR)
            return astnode(AST_STR, value = tok["value"])
        else:
            error("illegal token %d" % next_tok)

    return start()


curr_tmp = 0


def codegen(ast):
    variables = []

    def new_temp():
        global curr_tmp
        curr_tmp += 1
        return "tmp" + str(curr_tmp)

    def gen_stmt(stmt):
        if stmt["nodetype"] == AST_ASSIGN:
            expr_loc = gen_expr(stmt["right"])
            if stmt["left"] in variables:
                print("%s = %s" % (stmt["left"], expr_loc))
            else:
                variables.append(stmt["left"])
                print("let %s = %s" % (stmt["left"], expr_loc))
        elif stmt["nodetype"] == AST_PRINT:
            expr_loc = gen_expr(stmt["expr"])
            print('console.log(' + expr_loc + ')')

        elif stmt["nodetype"] == AST_WHILE:
            expr_loc = gen_expr(stmt["expr"])
            print("while (%s) { " % expr_loc)
            for body_stmt in stmt["body"]:
                gen_stmt(body_stmt)
            gen_expr(stmt["expr"], expr_loc)
            print("}")

        elif stmt["nodetype"] == AST_IF:
            expr_loc = gen_expr(stmt["expr"])
            print("if (%s) { " % expr_loc)
            for body_stmt in stmt["body"]:
                gen_stmt(body_stmt)
            gen_expr(stmt["expr"], expr_loc)
            print("}")

    def gen_expr(expr, loc_name=None):
        if expr["nodetype"] in (AST_INT, AST_FLOAT):
            loc = loc_name or new_temp()
            print("let %s = %s;" % (loc, expr["value"]))
            return loc
        elif expr["nodetype"] == AST_ID:
            return expr["name"]
        elif expr["nodetype"] == AST_STR:
            return "\"" + str(expr["value"]) + "\""
        elif expr["nodetype"] == AST_BINOP:
            left_loc = gen_expr(expr["left"])
            right_loc = gen_expr(expr["right"])
            loc = new_temp()
            print("let %s = %s %s %s;" % (loc, left_loc, expr["op"], right_loc))
            return loc
        elif expr["nodetype"] == AST_COND:
            left_loc = gen_expr(expr["left"])
            right_loc = gen_expr(expr["right"])
            return "%s %s %s" % (left_loc, expr["op"], right_loc)


    for stmt in ast["stmts"]:
        gen_stmt(stmt)


def main():
    with open('demo.txt') as f:
        read_data = f.read()

    codegen(parser(lexer(read_data)))


if __name__ == "__main__":
    main()
