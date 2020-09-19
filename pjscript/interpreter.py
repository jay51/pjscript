#!/usr/bin/env  python3
import sys
from collections import OrderedDict

# TODO: add obj testing

# fmt: off
class Tokens():
    OR          = "|"
    AND         = "&"
    NOT         = "!"
    PLUSPLUS    = "++"
    PLUSPLUS    = "++"
    MINUSMINUS  = "--"
    DOT         = "."
    PLUS        = "+"
    MINUS       = "-"
    MUL         = "*"
    DIV         = "/"
    GT          = ">"
    LT          = "<"
    GTE         = ">="
    LTE         = "<="
    EQUALEQUAL  = "=="
    NOTEQUAL    = "!="
    COMMENT     = "/*"
    COMMA       = ","
    LPAREN      = "("
    RPAREN      = ")"
    LCURLY      = "{"
    RCURLY      = "}"
    LBRACK      = "["
    RBRACK      = "]"
    COLON       = ":"
    SEMI        = ";"
    EQUAL       = "="
    EOF         = "EOF"
    STRING      = "STRING"
    NUMBER      = "NUMBER"
    IDENTIFIER  = "IDENTIFIER"
    # RESERVED_KEYWORDS
    _null       = "null"
    _var        = "var"
    _function   = "function"
    _return     = "return"
    _for        = "for"
    _if         = "if"
    _else       = "else"
# fmt: on


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def equal(self, type):
        return self.type == type

    def __str__(self):
        return "< {type} : {value} >".format(type=self.type, value=self.value)

    __repr__ = __str__


class Lexer:
    def __init__(self, text):
        self.text = text
        self.length = len(text)
        self.pos = 0
        self.curr_char = self.text[self.pos]

    def __iter__(self):
        return self

    def __next__(self):
        if self.curr_char:
            return self.get_next_token()
        else:
            raise StopIteration

    def advance(self):
        self.pos += 1
        if self.pos > self.length - 1:
            self.curr_char = None
        else:
            self.curr_char = self.text[self.pos]

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > self.length - 1:
            return None
        return self.text[peek_pos]

    def skip_comment(self):
        # skip "/*"
        self.advance()
        self.advance()
        while True:
            if self.curr_char == "*" and self.peek() == "/":
                break
            elif self.curr_char == "/" and self.peek() == "*":
                self.skip_comment()
            else:
                self.advance()
        # skip "*/"
        self.advance()
        self.advance()

    def skip_whitespace(self):
        while self.curr_char != None and self.curr_char.isspace():
            self.advance()

    def collect_string(self):
        value = ""
        while self.curr_char != '"':
            value += self.curr_char
            self.advance()
        self.advance()
        token = Token(Tokens.STRING, value)
        return token

    def collect_number(self):
        value = ""
        while self.curr_char != None and self.curr_char.isdigit():
            value += self.curr_char
            self.advance()
        token = Token(Tokens.NUMBER, value)
        return token

    def identifier(self):
        id = ""
        while self.curr_char != None and self.curr_char.isalnum():
            id += self.curr_char
            self.advance()

        if hasattr(Tokens, "_" + id):
            token_type = getattr(Tokens, "_" + id)  # RESERVED_KEYWORDS
            return Token(token_type, id)
        else:
            return Token(Tokens.IDENTIFIER, id)

    def get_next_token(self):
        while self.curr_char != None:
            if self.curr_char.isspace():
                self.skip_whitespace()
                continue

            if self.curr_char == "/" and self.peek() == "*":
                self.skip_comment()

            if self.curr_char == Tokens.DOT:
                self.advance()
                return Token(Tokens.DOT, Tokens.DOT)

            if self.curr_char == Tokens.COMMA:
                self.advance()
                return Token(Tokens.COMMA, Tokens.COMMA)

            if self.curr_char == Tokens.COLON:
                self.advance()
                return Token(Tokens.COLON, Tokens.COLON)

            if self.curr_char == Tokens.LPAREN:
                self.advance()
                return Token(Tokens.LPAREN, Tokens.LPAREN)

            if self.curr_char == Tokens.RPAREN:
                self.advance()
                return Token(Tokens.RPAREN, Tokens.RPAREN)

            if self.curr_char == Tokens.LCURLY:
                self.advance()
                return Token(Tokens.LCURLY, Tokens.LCURLY)

            if self.curr_char == Tokens.RCURLY:
                self.advance()
                return Token(Tokens.RCURLY, Tokens.RCURLY)

            if self.curr_char == Tokens.LBRACK:
                self.advance()
                return Token(Tokens.LBRACK, Tokens.LBRACK)

            if self.curr_char == Tokens.RBRACK:
                self.advance()
                return Token(Tokens.RBRACK, Tokens.RBRACK)

            if self.curr_char == Tokens.PLUS and self.peek() == Tokens.PLUS:
                self.advance()
                self.advance()
                return Token(Tokens.PLUSPLUS, Tokens.PLUSPLUS)

            if self.curr_char == Tokens.MINUS and self.peek() == Tokens.MINUS:
                self.advance()
                self.advance()
                return Token(Tokens.MINUSMINUS, Tokens.MINUSMINUS)

            if self.curr_char == Tokens.PLUS:
                self.advance()
                return Token(Tokens.PLUS, Tokens.PLUS)

            if self.curr_char == Tokens.MINUS:
                self.advance()
                return Token(Tokens.MINUS, Tokens.MINUS)

            if self.curr_char == Tokens.MUL:
                self.advance()
                return Token(Tokens.MUL, Tokens.MUL)

            if self.curr_char == Tokens.DIV:
                self.advance()
                return Token(Tokens.DIV, Tokens.DIV)

            if self.curr_char == Tokens.GT and self.peek() == Tokens.EQUAL:
                self.advance()
                self.advance()
                return Token(Tokens.GTE, Tokens.GTE)

            if self.curr_char == Tokens.LT and self.peek() == Tokens.EQUAL:
                self.advance()
                self.advance()
                return Token(Tokens.LTE, Tokens.LTE)

            if self.curr_char == Tokens.EQUAL and self.peek() == Tokens.EQUAL:
                self.advance()
                self.advance()
                return Token(Tokens.EQUALEQUAL, Tokens.EQUALEQUAL)

            if self.curr_char == Tokens.NOT and self.peek() == Tokens.EQUAL:
                self.advance()
                self.advance()
                return Token(Tokens.NOTEQUAL, Tokens.NOTEQUAL)

            # LOGICAL NOT
            if self.curr_char == Tokens.NOT:
                self.advance()
                return Token(Tokens.NOT, Tokens.NOT)

            # LOGICAL OR
            if self.curr_char == Tokens.OR:
                self.advance()
                if self.curr_char == Tokens.OR:
                    self.advance()
                    return Token(Tokens.OR, Tokens.OR)

            # LOGICAL AND
            if self.curr_char == Tokens.AND:
                self.advance()
                if self.curr_char == Tokens.AND:
                    self.advance()
                    return Token(Tokens.AND, Tokens.AND)

            if self.curr_char == Tokens.GT:
                self.advance()
                return Token(Tokens.GT, Tokens.GT)

            if self.curr_char == Tokens.LT:
                self.advance()
                return Token(Tokens.LT, Tokens.LT)

            if self.curr_char == Tokens.SEMI:
                self.advance()
                return Token(Tokens.SEMI, Tokens.SEMI)

            if self.curr_char == Tokens.EQUAL:
                self.advance()
                return Token(Tokens.EQUAL, Tokens.EQUAL)

            if self.curr_char and self.curr_char.isalpha():
                return self.identifier()

            if self.curr_char == '"':
                self.advance()
                return self.collect_string()

            if self.curr_char and self.curr_char.isdigit():
                return self.collect_number()

        return Token(Tokens.EOF, Tokens.EOF)


# TODO: update the AST grammar
# PARSER
"""
AST
Program {
    ...
    body:[
        VarDeclaration, # var name = 2;
        Var_assigne, # name = 2;
        CallExpression # log(name)
    ]
}

Program
    body: [Statement*]


Statement:
        | CallExpression
        | VarDeclaration
        | Var_assigne
        | FuncDeclaration
        | ForLoop
        | IfStmt
        | Return
        | NoOp


CallExpression
    callee: id
    args: []


ForLoop: # for(var i =0; i<5; i++){...};
    var_dec: VarDeclaration | Var_assigne | NoOp
    condition: Expression | NoOp
    expr: Expression | NoOp
    body: Program


IfStmt: if ( 1 == 0) {...} else if (1 == 1) {...} else{...};
    condition: Expression | NoOp
    else_if_stmt: IfStmt
    else_stmt: Program
    body: Program



VarDeclaration, # var name = "jack";
    type: var
    left: identifier
    right: expression


FuncDeclaration, # function name(){};
    name: identifier
    params: [identifier*]
    body: Program


Var_assigne, # name = "jack";
    left: identifier
    right: expression


Return: # return 2 * add(2, 2)
    expr: expression

expression: term ( ((+ | - | == | !=) term) | ((< | > | >= | <=) expression) )*

expr: expression ((&& | `||` | !) expression)*

term: atom ((* | /) atom)*

atom: factor ((-- | ++))*

factor: String
        | STRING
        | ARRAY
        | OBJ
        | Num
        | id
        | + factor
        | - factor
        | (( -- | ++ ))? factor
        | "(" expression ")"
        | None


id: CallExpression
    | Var_assigne
    | identifier
    | ++ identifier
    | -- identifier
    | identifier[]


identifier: [a-zA-Z][a-zA-Z0-9_]

"""


class Program:
    def __init__(self, body, scope=None):
        self.scope = scope
        self.body = body

    def __str__(self):
        return """< {}
            {}
        />""".format(
            self.__class__.__name__, self.body
        )

    __repr__ = __str__


class Num:
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __str__(self):
        return "<{} : {}>".format(self.__class__.__name__, self.value)

    __repr__ = __str__


class Null:
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __str__(self):
        return "<{} : {}>".format(self.__class__.__name__, self.value)

    __repr__ = __str__


class String:
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __str__(self):
        return "<{} : {}>".format(self.__class__.__name__, self.value)

    __repr__ = __str__


class Array:
    def __init__(self, arr_elements):
        self.values = arr_elements

    def __str__(self):
        return "< {} : {} />".format(self.__class__.__name__, self.values)

    __repr__ = __str__


class Obj:
    def __init__(self, obj):
        self.obj = obj

    def __str__(self):
        string = ""
        for key, val in self.obj.items():
            string += f"\t{key}: {val}\n"

        return """< {} \n{} />""".format(self.__class__.__name__, string)

    __repr__ = __str__


class Identifier:
    def __init__(self, token, indeces=None, prop=None):
        self.token = token
        self.value = token.value  # var name
        self.indeces = indeces
        self.prop = prop

    def __str__(self):
        return "< {} | {} | {} >".format(self.__class__.__name__, self.value, self.prop)

    __repr__ = __str__


class VarDeclaration:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "{} <\n\t{} \n/>".format(self.__class__.__name__, self.right)

    __repr__ = __str__


class FuncDeclaration:
    def __init__(self, params, body, name=None):
        self.name = name if name else "anonymous"
        self.params = params
        self.body = body

    def __str__(self):
        return "{} < {} : \n\t{} />".format(
            self.__class__.__name__, self.params, self.body
        )

    __repr__ = __str__


class ForLoop:
    def __init__(self, var_dec, condition, expr, body):
        self.var = var_dec
        self.condition = condition
        self.expr = expr
        self.body = body

    def __str__(self):
        return "{} < \n\t{} | \n\t{} | \n\t{} | \n\t{} \n/>".format(
            self.__class__.__name__, self.var, self.condition, self.expr, self.body
        )

    __repr__ = __str__


class IfStmt:
    def __init__(self, condition, body, else_if_stmt, else_stmt):
        self.condition = condition
        self.body = body
        self.else_if_stmt = else_if_stmt
        self.else_stmt = else_stmt

    def __str__(self):
        return "{} < {} | {} | {} | \n\t{} \n/>".format(
            self.__class__.__name__,
            self.condition,
            self.else_if_stmt or "else if part",
            self.else_stmt or "else part",
            self.body,
        )

    __repr__ = __str__


class Assignment:
    def __init__(self, left, right, indeces=None):
        self.left = left
        self.right = right
        self.indeces = indeces

    def __str__(self):
        return "{} < {} : {}  -> {} />".format(
            self.__class__.__name__,
            self.left,
            self.right.__class__.__name__,
            self.right.value,
        )

    __repr__ = __str__


class CallExpression:
    def __init__(self, identifier, args):
        self.identifier = identifier
        self.args = args
        # self.default_ret = Tokens._null
        self.default_ret = Null(Token(Tokens._null, Tokens._null))

    def __str__(self):
        return "<{} : {}  -> {}>".format(
            self.__class__.__name__, self.identifier, self.args
        )

    __repr__ = __str__


class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return "BinOp( {} {} {})".format(self.left, self.op, self.right)

    __repr__ = __str__


class PostIncDecOp:
    def __init__(self, left, op):
        self.left = left
        self.op = op

    def __str__(self):
        return "PostIncDecOp( {} {} )".format(self.left, self.op)

    __repr__ = __str__


class PreIncDecOp:
    def __init__(self, left, op):
        self.left = left
        self.op = op

    def __str__(self):
        return "PreIncDecOp( {} {} )".format(self.left, self.op)

    __repr__ = __str__


class UnaryOp:
    def __init__(self, op, expr):
        self.expr = expr
        self.op = op

    def __str__(self):
        return "UnaryOp( {} {} )".format(self.op, self.expr)

    __repr__ = __str__


class ReturnStmt:
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return "Return( {} )".format(self.expr)

    __repr__ = __str__


class NoOp:
    pass


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.curr_token = self.lexer.get_next_token()

    def error(self, token):
        raise Exception("token {} not equal, {}".format(token, self.curr_token))

    def consume(self, type):
        if self.curr_token.equal(type):
            self.curr_token = self.lexer.get_next_token()
        else:
            self.error(type)

    def program(self, scope):
        body = []
        node = self.statement()
        if isinstance(node, NoOp):
            print("empty file")
            sys.exit()

        body.append(node)
        while True:
            if self.curr_token.type == Tokens.SEMI:
                self.consume(Tokens.SEMI)
                node = self.statement()
                if isinstance(node, NoOp):
                    break
                body.append(node)

            elif self.curr_token.type != Tokens.SEMI:
                raise Exception("missing ;")

        return Program(body, scope)

    def statement(self):
        if self.curr_token.type == Tokens._var:
            node = self.var_declaration()
            return node

        elif self.curr_token.type == Tokens.IDENTIFIER:
            node = self.id()
            return node

        elif self.curr_token.type == Tokens._function:
            node = self.func_declaration()
            return node

        elif self.curr_token.type == Tokens._return:
            node = self.return_stmt()
            return node

        elif self.curr_token.type == Tokens._for:
            node = self.for_stmt()
            return node

        elif self.curr_token.type == Tokens.PLUSPLUS:
            node = self.expr()
            return node

        elif self.curr_token.type == Tokens.MINUSMINUS:
            node = self.expr()
            return node

        elif self.curr_token.type == Tokens._if:
            node = self.if_stmt()
            return node

        elif self.curr_token.type == Tokens.EOF:
            node = NoOp()
            return node

        return NoOp()

    def var_declaration(self):
        self.consume(Tokens._var)
        left = self.curr_token.value
        self.consume(Tokens.IDENTIFIER)
        self.consume(Tokens.EQUAL)
        right = self.expr()
        return VarDeclaration(left, right)

    def func_declaration(self):
        self.consume(Tokens._function)
        name = None
        if self.curr_token.type == Tokens.IDENTIFIER:
            name = self.curr_token.value
            self.consume(Tokens.IDENTIFIER)

        self.consume(Tokens.LPAREN)
        node = self.expr()
        params = []
        if not isinstance(node, NoOp):
            params.append(node)

        while self.curr_token.type == Tokens.COMMA:
            self.consume(Tokens.COMMA)
            params.append(self.expr())

        self.consume(Tokens.RPAREN)
        self.consume(Tokens.LCURLY)
        body = self.program(name)

        self.consume(Tokens.RCURLY)
        return FuncDeclaration(params, body, name)

    def for_stmt(self):
        self.consume(Tokens._for)
        self.consume(Tokens.LPAREN)

        if self.curr_token.type == Tokens._var:
            var = self.var_declaration()
        elif self.curr_token.type == Tokens.IDENTIFIER:
            var = self.id()
        else:
            var = NoOp()

        self.consume(Tokens.SEMI)
        condition = self.expr()
        self.consume(Tokens.SEMI)
        expr = self.expr()
        self.consume(Tokens.RPAREN)
        self.consume(Tokens.LCURLY)
        body = self.program("for")
        self.consume(Tokens.RCURLY)
        return ForLoop(var, condition, expr, body)

    def if_stmt(self):
        self.consume(Tokens._if)
        self.consume(Tokens.LPAREN)
        condition = self.expr()
        self.consume(Tokens.RPAREN)
        self.consume(Tokens.LCURLY)
        body = self.program("if")
        self.consume(Tokens.RCURLY)

        if self.curr_token.type == Tokens._else:
            self.consume(Tokens._else)
            if self.curr_token.type == Tokens._if:
                else_if_stmt = self.if_stmt()
                return IfStmt(condition, body, else_if_stmt, None)

            self.consume(Tokens.LCURLY)
            else_body = self.program("else")
            self.consume(Tokens.RCURLY)
            return IfStmt(condition, body, None, else_body)

        # in the case of no `else if` or `else` parts
        return IfStmt(condition, body, None, None)

    def return_stmt(self):
        self.consume(Tokens._return)
        expr = self.expr()
        # `return;` with no thing to return will return NoOp which returns True
        # but JS behievor is to return Null, so we're doing that. is it consistent with the language? idk.
        if isinstance(expr, NoOp):
            default_ret = Null(Token(Tokens._null, Tokens._null))
            return ReturnStmt(default_ret)
        return ReturnStmt(expr)

    # TODO: improve code reuse
    def id(self):
        token = self.curr_token
        self.consume(Tokens.IDENTIFIER)
        # function call
        if self.curr_token.type == Tokens.LPAREN:
            return self.function_call(token)

        if self.curr_token.type == Tokens.EQUAL:
            left = token.value
            self.consume(Tokens.EQUAL)
            right = self.expr()
            return Assignment(left, right)

        if self.curr_token.type == Tokens.DOT:
            self.consume(Tokens.DOT)
            prop = self.expr()
            return Identifier(token, None, prop)

        # if To parse `x[1] = 1`
        # else To parse `var y = x[1]`
        if self.curr_token.type == Tokens.LBRACK:
            self.consume(Tokens.LBRACK)
            index = self.expr()
            self.consume(Tokens.RBRACK)
            indeces = [index]

            while True:
                if self.curr_token.type == Tokens.LBRACK:
                    self.consume(Tokens.LBRACK)
                    index = self.expr()
                    self.consume(Tokens.RBRACK)
                    indeces.append(index)
                else:
                    break

            if self.curr_token.type == Tokens.EQUAL:
                left = token.value
                self.consume(Tokens.EQUAL)
                right = self.expr()
                return Assignment(left, right, indeces)

            else:
                return Identifier(token, indeces)

        if self.curr_token.type == Tokens.PLUSPLUS:
            op = self.curr_token
            self.consume(Tokens.PLUSPLUS)
            return PostIncDecOp(token, op)

        if self.curr_token.type == Tokens.MINUSMINUS:
            op = self.curr_token
            self.consume(Tokens.MINUSMINUS)
            return PostIncDecOp(token, op)

        # variable
        return Identifier(token)

    def function_call(self, token):
        args = []
        self.consume(Tokens.LPAREN)
        # print(self.curr_token)
        node = self.expr()
        if not isinstance(node, NoOp):
            args.append(node)
        # print(self.curr_token)
        while self.curr_token.type == Tokens.COMMA:
            self.consume(Tokens.COMMA)
            args.append(self.expr())
        # print(self.curr_token)
        self.consume(Tokens.RPAREN)
        return CallExpression(token.value, args)

    def parse_obj(self):
        obj = dict()

        self.consume(Tokens.LCURLY)
        if self.curr_token.type == Tokens.IDENTIFIER:
            prop_name = self.curr_token.value
            self.consume(Tokens.IDENTIFIER)
            self.consume(Tokens.COLON)
            prop_val = self.expression()
            obj[prop_name] = prop_val

            while self.curr_token.type == Tokens.COMMA:
                self.consume(Tokens.COMMA)
                prop_name = self.curr_token.value
                self.consume(Tokens.IDENTIFIER)
                self.consume(Tokens.COLON)
                prop_val = self.expression()
                obj[prop_name] = prop_val

        self.consume(Tokens.RCURLY)
        return Obj(obj)

    def factor(self):
        token = self.curr_token

        if token.type == Tokens.STRING:
            return self.parse_string()

        elif token.type == Tokens.IDENTIFIER:
            return self.id()

        elif token.type == Tokens.NUMBER:
            return self.parse_number()

        elif token.type == Tokens._null:
            self.consume(Tokens._null)
            return Null(token)

        elif token.type == Tokens._function:
            return self.func_declaration()

        elif token.type == Tokens.PLUS:
            self.consume(Tokens.PLUS)
            node = UnaryOp(token, self.factor())
            return node

        elif token.type == Tokens.MINUS:
            self.consume(Tokens.MINUS)
            node = UnaryOp(token, self.factor())
            return node

        elif token.type == Tokens.LBRACK:
            self.consume(Tokens.LBRACK)
            arr_elements = []
            node = self.expr()
            if not isinstance(node, NoOp):
                arr_elements.append(node)

            while self.curr_token.type == Tokens.COMMA:
                self.consume(Tokens.COMMA)
                arr_elements.append(self.expr())

            self.consume(Tokens.RBRACK)
            node = Array(arr_elements)
            return node

        elif token.type == Tokens.LCURLY:
            return self.parse_obj()

        elif token.type == Tokens.LPAREN:
            self.consume(Tokens.LPAREN)
            node = self.expr()
            self.consume(Tokens.RPAREN)
            return node

        elif token.type == Tokens.PLUSPLUS:
            self.consume(Tokens.PLUSPLUS)
            node = PreIncDecOp(self.factor(), token)
            return node

        elif token.type == Tokens.MINUSMINUS:
            self.consume(Tokens.MINUSMINUS)
            node = PreIncDecOp(self.factor(), token)
            return node

        # print("not considerd", self.curr_token.type)
        return NoOp()
        # return None

    def atom(self):
        node = self.factor()
        while self.curr_token.type in (Tokens.PLUSPLUS, Tokens.MINUSMINUS):
            token = self.curr_token
            if token.type == Tokens.PLUSPLUS:
                self.consume(Tokens.PLUSPLUS)

            if token.type == Tokens.MINUSMINUS:
                self.consume(Tokens.MINUSMINUS)

            node = PostIncDecOp(node, token)

        return node

    def term(self):
        node = self.atom()

        while self.curr_token.type in (Tokens.MUL, Tokens.DIV):
            token = self.curr_token
            if token.type == Tokens.MUL:
                self.consume(Tokens.MUL)
            if token.type == Tokens.DIV:
                self.consume(Tokens.DIV)

            node = BinOp(left=node, op=token, right=self.factor())
        return node

    def expression(self):
        node = self.term()
        while self.curr_token.type in (
            Tokens.PLUS,
            Tokens.MINUS,
            Tokens.EQUALEQUAL,
            Tokens.NOTEQUAL,
        ):
            token = self.curr_token
            if token.type == Tokens.EQUALEQUAL:
                self.consume(Tokens.EQUALEQUAL)
            if token.type == Tokens.NOTEQUAL:
                self.consume(Tokens.NOTEQUAL)
            if token.type == Tokens.PLUS:
                self.consume(Tokens.PLUS)
            if token.type == Tokens.MINUS:
                self.consume(Tokens.MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        while self.curr_token.type in (Tokens.GT, Tokens.LT, Tokens.GTE, Tokens.LTE):
            token = self.curr_token
            if token.type == Tokens.GT:
                self.consume(Tokens.GT)
            if token.type == Tokens.LT:
                self.consume(Tokens.LT)
            if token.type == Tokens.GTE:
                self.consume(Tokens.GTE)
            if token.type == Tokens.LTE:
                self.consume(Tokens.LTE)

            node = BinOp(left=node, op=token, right=self.expression())

        return node

    def expr(self):
        node = self.expression()
        # These operators are evaluated last
        while self.curr_token.type in (Tokens.OR, Tokens.AND, Tokens.NOT):
            token = self.curr_token
            if token.type == Tokens.OR:
                self.consume(Tokens.OR)
            if token.type == Tokens.AND:
                self.consume(Tokens.AND)
            if token.type == Tokens.NOT:
                self.consume(Tokens.NOT)

            node = BinOp(left=node, op=token, right=self.expression())

        return node

    def parse_string(self):
        token = self.curr_token
        self.consume(Tokens.STRING)
        return String(token)

    def parse_number(self):
        token = self.curr_token
        self.consume(Tokens.NUMBER)
        return Num(token)

    def parse(self):
        program = self.program("global")
        return program


class SymbolTable:
    def __init__(self, func_name, level, parent_scope):
        self.func_name = func_name
        self.level = level
        self.parent_scope = parent_scope
        self.table = OrderedDict()

    def __str__(self):
        h1 = "SCOPE (SCOPED SYMBOL TABLE)"
        lines = ["\n", h1, "=" * len(h1)]
        for header_name, header_value in (
            ("Scope name", self.func_name),
            ("Scope level", self.level),
            (
                "Enclosing scope",
                self.parent_scope.func_name if self.parent_scope else None,
            ),
        ):
            lines.append("%-15s: %s" % (header_name, header_value))

        h2 = "Scope (Scoped symbol table) contents"
        lines.extend([h2, "-" * len(h2)])
        lines.extend(("%7s: %r" % (key, value)) for key, value in self.table.items())

        lines.append("\n")
        s = "\n".join(lines)
        return s

    __repr__ = __str__

    def insert(self, name, value):
        self.table[name] = value

    def reassign(self, name, value):
        old_val = self.table.get(name)
        if old_val is not None:
            self.table[name] = value
            return value

        if self.level == 1:
            return None

        return self.parent_scope.reassign(name, value)

    def remove(self, name):
        return self.table.pop(name)

    def get(self, name):
        value = self.table.get(name)
        if value is not None:
            return value

        if self.level == 1:
            return None

        return self.parent_scope.get(name)


# interpreter
class NodeVisiter:
    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        # print(method_name)
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception("No visit_{} method".format(type(node).__name__))


class BuiltIn:
    @staticmethod
    def log(*args):
        for param in args:
            print(param, end=" ")
        print()
        return 0

    @staticmethod
    def add(*args):
        # print(args)
        # print(sum(args))
        return sum(args)


class Interpreter(NodeVisiter):
    def __init__(self, tree):
        # self.current_scope = SymbolTable("global", 1, None)
        self.current_scope = None
        self.tree = tree

    def error(self, val):
        raise Exception("identifier {} not defined".format(val))

    def visit_Program(self, node):
        level = self.current_scope.level + 1 if self.current_scope else 1
        self.current_scope = SymbolTable(node.scope, level, self.current_scope)
        for stmt in node.body:
            if isinstance(stmt, ReturnStmt):
                self.current_scope = self.current_scope.parent_scope
                return self.visit(stmt)

            elif isinstance(stmt, ForLoop):
                # if node is not None, means forloop's encountered a Return_stmt
                # and node is what's being or should be returend
                node = self.visit(stmt)
                if node is not None:
                    self.current_scope = self.current_scope.parent_scope
                    return node

            elif isinstance(stmt, IfStmt):
                # if node is not None, means IfStmt's encountered a Return_stmt
                # and node is what's being or should be returend
                node = self.visit(stmt)
                if node is not None:
                    self.current_scope = self.current_scope.parent_scope
                    return node

            else:
                self.visit(stmt)

        self.current_scope = self.current_scope.parent_scope
        return None

    def visit_CallExpression(self, node):
        args = node.args
        # we support only the log and add function right now
        function = getattr(BuiltIn, node.identifier, None)
        if function is not None:
            arguments = []
            for param in args:
                arguments.append(self.visit(param))
            return function(*arguments)

        else:
            func = self.current_scope.get(node.identifier)
            if func is None:
                self.error(node.identifier)

            func_param_length = len(func.params)
            func_arg_length = len(node.args)
            if func_param_length != func_arg_length:
                raise Exception(
                    "{} Expectes {} args, but found {} args".format(
                        func.name, func_param_length, func_arg_length
                    )
                )

            for idx, param in enumerate(func.params):
                if isinstance(param, NoOp) or node.args[idx] is None:
                    print(
                        "Warning: param is {} and arg is {} ".format(
                            param, node.args[idx]
                        )
                    )
                    continue
                # print("idx: {}, param: {}, args: {}".format(idx, param.value, node.args[idx].value))
                self.visit(VarDeclaration(param.value, node.args[idx]))

            # if function body did not return anything use default return
            ret_node = self.visit(func.body)
            ret_node = self.visit(node.default_ret) if ret_node is None else ret_node

            for idx, param in enumerate(func.params):
                if isinstance(param, NoOp) or node.args[idx] is None:
                    continue
                self.current_scope.remove(param.value)

            return ret_node

    def visit_VarDeclaration(self, node):
        name = node.left
        value = self.visit(node.right)
        self.current_scope.insert(name, value)
        return name

    def visit_ForLoop(self, node):
        # decalare the var first
        self.visit(node.var)
        condition_result = self.visit(node.condition)
        while condition_result and condition_result is not None:
            ret_node = self.visit(node.body)
            # if ret_node is not None, means we've returned from function
            if ret_node is not None:
                return ret_node
            self.visit(node.expr)
            condition_result = self.visit(node.condition)

        return None

    def visit_IfStmt(self, node):
        condition_result = self.visit(node.condition)
        if condition_result:
            return self.visit(node.body)

        # it's going to be treated just like another if statement
        elif node.else_if_stmt is not None:
            return self.visit(node.else_if_stmt)

        elif node.else_stmt is not None:
            return self.visit(node.else_stmt)

        return None

    def visit_FuncDeclaration(self, node):
        if node.name != "anonymous":
            self.current_scope.insert(node.name, node)
        return node

    def visit_ReturnStmt(self, node):
        return self.visit(node.expr)

    def visit_BinOp(self, node):
        if node.op.type == Tokens.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        if node.op.type == Tokens.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        if node.op.type == Tokens.MUL:
            return self.visit(node.left) * self.visit(node.right)
        if node.op.type == Tokens.DIV:
            return self.visit(node.left) // self.visit(node.right)
        if node.op.type == Tokens.GT:
            return self.visit(node.left) > self.visit(node.right)
        if node.op.type == Tokens.LT:
            return self.visit(node.left) < self.visit(node.right)
        if node.op.type == Tokens.GTE:
            return self.visit(node.left) >= self.visit(node.right)
        if node.op.type == Tokens.LTE:
            return self.visit(node.left) >= self.visit(node.right)
        if node.op.type == Tokens.EQUALEQUAL:
            return self.visit(node.left) == self.visit(node.right)
        if node.op.type == Tokens.NOTEQUAL:
            return self.visit(node.left) != self.visit(node.right)

        if node.op.type == Tokens.OR:
            return self.visit(node.left) or self.visit(node.right)

        if node.op.type == Tokens.AND:
            return self.visit(node.left) and self.visit(node.right)

        if node.op.type == Tokens.NOT:
            return not self.visit(node.right)

    def visit_PostIncDecOp(self, node):
        value = self.current_scope.get(node.left.value)
        new_value = value + 1 if node.op.type == Tokens.PLUSPLUS else value - 1
        if self.current_scope.reassign(node.left.value, new_value) is None:
            self.error(node.left.value)
        return value

    def visit_PreIncDecOp(self, node):
        value = self.current_scope.get(node.left.value)
        new_value = value + 1 if node.op.type == Tokens.PLUSPLUS else value - 1
        self.current_scope.reassign(node.left.value, new_value)
        return new_value

    def visit_UnaryOp(self, node):
        if node.op.type == Tokens.PLUS:
            return +self.visit(node.expr)
        if node.op.type == Tokens.MINUS:
            return -self.visit(node.expr)

    # THIS IS FOR REASSIGNMENT
    def visit_Assignment(self, node):
        name = node.left  # var name
        value = self.visit(node.right)  # expr
        if node.indeces is not None:
            arr = self.current_scope.get(name)
            arr_sub = arr
            for idx, v in enumerate(node.indeces):
                if len(node.indeces) == idx + 1:
                    index = self.visit(v)
                    arr_sub[index] = value
                else:
                    index = self.visit(v)
                    arr_sub = arr_sub[index]

            self.current_scope.reassign(name, arr)

        else:
            if self.current_scope.reassign(name, value) is None:
                self.error(node.left)

        return name

    def visit_Identifier(self, node):
        value = self.current_scope.get(node.value)
        if value is None:
            self.error(node.value)
        if node.indeces is not None:
            for v in node.indeces:
                index = self.visit(v)
                value = value[index]
            return value

        # prop is a property on an object. each identifier will have a prop set to None by default.
        # To access a nested prop, we link props togather. <prop: name> -> <prop: first> -> <String: "jack">
        prop = node.prop
        if prop is not None:
            val = value
            while prop is not None:
                # hack to make functions inside objects work
                if isinstance(prop, CallExpression):
                    val = self.visit(val.get(prop.identifier))
                    val = self.visit(val.body)
                    prop = None
                else:
                    # to make it work with sub identifiers/objects/props
                    # age = {born: <num: 23>, died: <num: 232>}
                    val = self.visit(val.get(prop.value))
                    if hasattr(prop, "indeces"):
                        if prop.indeces is not None:
                            for v in prop.indeces:
                                index = self.visit(v)
                                val = val[index]
                    prop = prop.prop
                # print("born ", prop.prop.value, val.get(prop.prop.value))

            return val

        return value

    def visit_String(self, node):
        return node.value

    def visit_Null(self, node):
        return node.value

    def visit_Num(self, node):
        return int(node.value)

    def visit_Array(self, node):
        return [self.visit(val) for val in node.values]

    def visit_Obj(self, node):
        return node.obj
        # return {key: self.visit(val) for key, val in node.obj.items()}

    def visit_NoOp(self, node):
        return True

    def interpret(self):
        self.visit(self.tree)
