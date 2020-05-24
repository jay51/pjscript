from collections import OrderedDict

example = """

var x = 2;
log("x: ", x);

var y = x++ * 2;
log("y: ", y);
log("x: ", x);

"""

class Tokens():
    PLUSPLUS    = "++"
    MINUSMINUS  = "--"
    PLUS        = "+"
    MINUS       = "-"
    MUL         = "*"
    DIV         = "/"
    COMMENT     = "/*"
    COMMA       = ","
    LPAREN      = "("
    RPAREN      = ")"
    LCURLY      = "{"
    RCURLY      = "}"
    SEMI        = ";"
    ASSIGN      = "="
    EOF         = "EOF"
    ID          = "ID"
    STRING      = "STRING"
    NUMBER      = "NUMBER"
    IDENTIFIER  = "IDENTIFIER"
    # RESERVED_KEYWORDS
    _var         = "var"
    _function    = "function"
    _return      = "return"
    
    
class Token():
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
    def equal(self, type):
        return self.type == type

    def __str__(self):
        return "< {type} : {value} >".format(type=self.type, value=self.value)
    __repr__ = __str__
    
    
    
    
class Lexer():
    
    def __init__(self, text):
        self.text = text
        self.length = len(text) - 1
        self.pos = 0
        self.curr_char = self.text[self.pos]
        
        
    def __iter__(self):
        return self
        
        
    def __next__(self):
        if(self.curr_char):
            return self.get_next_token()
        else:
            raise StopIteration
            
            
    def advance(self):
        self.pos +=1
        if(self.pos > self.length - 1):
            self.curr_char = None
        else:
            self.curr_char = self.text[self.pos]


    def peek(self):
        peek_pos = self.pos + 1
        if(peek_pos > self.length - 1):
            return None
        return self.text[peek_pos]
        
        
    # /*comment*/
    def skip_comment(self):
        # skip "/*"
        self.advance()
        self.advance()
        while(True):
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
        while(self.curr_char != None and self.curr_char.isspace()):
            self.advance()
            
            
    def collect_string(self):
        value = ""
        while(self.curr_char != "\""):
            value += self.curr_char
            self.advance()
        self.advance()
        token = Token(Tokens.STRING, value)
        return token


    def collect_number(self):
        value = ""
        while(self.curr_char != None and self.curr_char.isdigit()):
            value += self.curr_char
            self.advance()
        token = Token(Tokens.NUMBER, value)
        return token
        
        
    def identifier(self):
        id = ""
        while(self.curr_char != None and self.curr_char.isalnum()):
            id += self.curr_char
            self.advance()

        if hasattr(Tokens, "_" + id):
            token_type = getattr(Tokens, "_" + id) # RESERVED_KEYWORDS (var, log)
            return Token(token_type, id)
        else:
            return Token(Tokens.IDENTIFIER, id)
            
            
            
    def get_next_token(self):
        while(self.curr_char != None):
            if self.curr_char.isspace() :
                self.skip_whitespace()
                continue

            if self.curr_char == "/" and self.peek() == "*":
                self.skip_comment()

            if self.curr_char == Tokens.COMMA:
                self.advance()
                return Token(Tokens.COMMA, Tokens.COMMA)

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

            if self.curr_char == Tokens.SEMI:
                self.advance()
                return Token(Tokens.SEMI, Tokens.SEMI)

            if self.curr_char == Tokens.ASSIGN:
                self.advance()
                return Token(Tokens.ASSIGN, Tokens.ASSIGN)

            if self.curr_char and self.curr_char.isalpha():
                return self.identifier()

            if self.curr_char == "\"":
                self.advance()
                return self.collect_string()

            if self.curr_char and self.curr_char.isdigit():
                return self.collect_number()
        return Token(Tokens.EOF, Tokens.EOF)
        
        
# THIS WILL SHOW YOU THE TOKENS
lexer = Lexer(example)
# for token in lexer:
    # print(token)
    
    
# parser
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
        | Return
        | NoOp


CallExpression
    callee: id
    args: []


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

expression: term ((+ | -) term)*

term: factor ((* | /) factor)*

factor: String
        | STRING
        | Num
        | id
        | + factor
        | - factor
        | "(" expression ")"
        | None



id: CallExpression
    | Var_assigne
    | identifier


identifier: [a-zA-Z][a-zA-Z0-9_]

"""


class Program():
    def __init__(self, body, scope=None):
        self.scope = scope
        self.body = body
        
    def __str__(self):
        return "<{} : {}>".format(self.__class__.__name__, self.body)
        
    __repr__ = __str__
        

class Num():
    def __init__(self, token):
        self.token = token
        self.value = token.value
        
    def __str__(self):
        return "<{} : {}>".format(self.__class__.__name__, self.value)

    __repr__ = __str__

        
class String():
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __str__(self):
        return "<{} : {}>".format(self.__class__.__name__, self.value)

    __repr__ = __str__


class Identifier():
    def __init__(self, token):
        self.token = token
        self.value = token.value # var name

    def __str__(self):
        return "<{} : {}>".format(self.__class__.__name__, self.value)

    __repr__ = __str__
    
        
        
class VarDeclaration():
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "VarDeclaration<{} : {}  -> {}>".format(self.left, self.right.__class__.__name__, self.right)

    __repr__ = __str__
    

class FuncDeclaration():
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __str__(self):
        return "FuncDeclaration<{} : {} >".format(self.params, self.body)

    __repr__ = __str__



class Assignment():
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "Assignment<{} : {}  -> {}>".format(self.left, self.right.__class__.__name__, self.right.value)

    __repr__ = __str__
    
    
class CallExpression():
    def __init__(self, identifier, args):
        self.identifier = identifier
        self.args = args
        
    def __str__(self):
        return "<{} : {}  -> {}>".format(self.__class__.__name__, self.identifier, self.args)
    __repr__ = __str__
    
    
    
class BinOp():
    def __init__(self, left,  op, right):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return "BinOp( {} {} {})".format(self.left, self.op, self.right)

    __repr__ = __str__


class PostIncDecOp():
    def __init__(self, left, op):
        self.left = left
        self.op = op

    def __str__(self):
        return "PostIncDecOp( {} {} )".format(self.left, self.op)

    __repr__ = __str__


class PreIncDecOp():
    def __init__(self, left, op):
        self.left = left
        self.op = op

    def __str__(self):
        return "PreIncDecOp( {} {} )".format(self.left, self.op)

    __repr__ = __str__


class UnaryOp():
    def __init__(self, op, expr):
        self.expr = expr
        self.op = op

    def __str__(self):
        return "UnaryOp( {} {} )".format(self.op, self.expr)

    __repr__ = __str__


class ReturnStmt():
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return "Return( {} )".format(self.expr)

    __repr__ = __str__


class NoOp():
    pass
    
    
class Parser():
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
        body.append(self.statement())
        while(self.curr_token.type == Tokens.SEMI):
            self.consume(Tokens.SEMI)
            body.append(self.statement())
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
        elif self.curr_token.type == Tokens.EOF:
            node = NoOp()
            return node

        return NoOp()
        
        
    def var_declaration(self):
        self.consume(Tokens._var)
        left = self.curr_token.value
        self.consume(Tokens.IDENTIFIER)
        self.consume(Tokens.ASSIGN)
        right = self.expression()
        return VarDeclaration(left, right)

        
    def func_declaration(self):
        self.consume(Tokens._function)
        name  = self.curr_token.value
        self.consume(Tokens.IDENTIFIER)
        self.consume(Tokens.LPAREN)
        params = [self.expression()]
        while(self.curr_token.type == Tokens.COMMA):
            self.consume(Tokens.COMMA)
            params.append(self.expression())

        self.consume(Tokens.RPAREN)
        self.consume(Tokens.LCURLY)
        body = self.program(name)

        self.consume(Tokens.RCURLY)
        return FuncDeclaration(name, params, body)


    def return_stmt(self):
        self.consume(Tokens._return)
        expr = self.expression()
        return ReturnStmt(expr)



    def id(self):
        token = self.curr_token
        self.consume(Tokens.IDENTIFIER)
        # function call
        if self.curr_token.type == Tokens.LPAREN:
            return self.function_call(token)

        if self.curr_token.type == Tokens.ASSIGN:
            return self.var_assigne(token)

        # variable
        return Identifier(token)


    def var_assigne(self, token):
        left = token.value
        self.consume(Tokens.ASSIGN)
        right = self.expression()
        return Assignment(left, right)
        
    
    def function_call(self, token):
        args = []
        self.consume(Tokens.LPAREN)
        #print(self.curr_token)
        args.append(self.expression())
        #print(self.curr_token)
        while(self.curr_token.type == Tokens.COMMA):
            self.consume(Tokens.COMMA)
            args.append(self.expression())
        # print(self.curr_token)
        self.consume(Tokens.RPAREN)
        return CallExpression(token.value, args)
        
        
    def factor(self):
        token = self.curr_token

        if token.type == Tokens.STRING:
            return self.parse_string()

        elif token.type == Tokens.IDENTIFIER:
            return self.id()

        elif token.type == Tokens.NUMBER:
            return self.parse_number()

        elif token.type == Tokens.PLUS:
            self.consume(Tokens.PLUS)
            node = UnaryOp(token, self.factor())
            return node

        elif token.type == Tokens.MINUS:
            self.consume(Tokens.MINUS)
            node = UnaryOp(token, self.factor())
            return node

        elif token.type == Tokens.LPAREN:
            self.consume(Tokens.LPAREN)
            node = self.expression()
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
        # return NoOp()
        return None
        


    def atom(self):
        node = self.factor()
        while(self.curr_token.type in (Tokens.PLUSPLUS, Tokens.MINUSMINUS)):
            token = self.curr_token
            if token.type == Tokens.PLUSPLUS:
                self.consume(Tokens.PLUSPLUS)

            if token.type == Tokens.MINUSMINUS:
                self.consume(Tokens.MINUSMINUS)

            node = PostIncDecOp(node, token)

        return node

        

    def term(self):
        node = self.atom()

        while(self.curr_token.type in (Tokens.MUL, Tokens.DIV)):
            token = self.curr_token
            if token.type == Tokens.MUL:
                self.consume(Tokens.MUL)
            if token.type == Tokens.DIV:
                self.consume(Tokens.DIV)

            node = BinOp(left=node, op=token, right=self.factor())
        return node



    def expression(self):
        node = self.term()
        while(self.curr_token.type in (Tokens.PLUS, Tokens.MINUS)):
            token = self.curr_token
            if token.type == Tokens.PLUS:
                self.consume(Tokens.PLUS)
            if token.type == Tokens.MINUS:
                self.consume(Tokens.MINUS)

            node = BinOp(left=node, op=token, right=self.term())
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
        
        


class SymbolTable():
    def __init__(self, func_name, level, parent_scope):
        self.func_name = func_name
        self.level = level
        self.parent_scope = parent_scope
        self.table = OrderedDict()


    def __str__(self):
        return """
        name: {}
        level: {}
        parent_scope: {}
        table: {}
        """.format(self.func_name, self.level, self.parent_scope, self.table)

    __repr__ = __str__

    def insert(self, name, value):
        self.table[name] = value

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
class NodeVisiter():
    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        # print(method_name)
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
        
    def generic_visit(self, node):
        raise Exception("No visit_{} method".format(type(node).__name__))
 


class BuiltIn():

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
        raise Exception("var {} not defined".format(val))
        
    def visit_Program(self, node):

        level = self.current_scope.level+1 if self.current_scope else 1
        self.current_scope = SymbolTable(node.scope, level, self.current_scope)
        for stmt in node.body:
            if isinstance(stmt, ReturnStmt):
                return self.visit(stmt)
            else:
                self.visit(stmt)

        self.current_scope = self.current_scope.parent_scope


    def visit_CallExpression(self, node):
        args = node.args
        function = node.identifier
        # we support only the log and add function right now
        if getattr(BuiltIn, function, None):
            function = getattr(BuiltIn, function)
            arguments = []
            for param in args:
                arguments.append(self.visit(param))
            return function(*arguments)

        else:
            func = self.current_scope.get(node.identifier)
            if func:
                func_param_length = len(func.params)
                func_arg_length = len(node.args)
                if func_param_length != func_arg_length:
                    raise Exception("{} Expectes {} args, but found {} args".format(func.name, func_param_length, func_arg_length))

                for idx, param in enumerate(func.params):
                    if not param:
                        continue
                    # print("idx: {}, param: {}, args: {}".format(idx, param.value, node.args[idx].value))
                    self.visit(VarDeclaration(param.value, node.args[idx]))

                ret_node = self.visit(func.body)

                for idx, param in enumerate(func.params):
                    if not param:
                        continue
                    self.current_scope.remove(param.value)
            return ret_node
            

    def visit_VarDeclaration(self, node):
        name = node.left
        value = self.visit(node.right)
        self.current_scope.insert(name, value)
        return name


    def visit_FuncDeclaration(self, node):
        self.current_scope.insert(node.name, node)
        return node.name


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


    def visit_PostIncDecOp(self, node):
        value = self.current_scope.get(node.left.value)
        new_value = value + 1 if node.op.type == Tokens.PLUSPLUS else value - 1
        self.current_scope.insert(node.left.value, new_value)
        return value


    def visit_PreIncDecOp(self, node):
        value = self.current_scope.get(node.left.value)
        new_value = value + 1 if node.op.type == Tokens.PLUSPLUS else value - 1
        self.current_scope.insert(node.left.value, new_value)
        return new_value


    def visit_UnaryOp(self, node):
        if node.op.type == Tokens.PLUS:
            return +self.visit(node.expr)
        if node.op.type == Tokens.MINUS:
            return -self.visit(node.expr)

    # THIS IS FOR REASSIGNMENT
    def visit_Assignment(self, node):
        if self.current_scope.get(node.left):
            name = node.left
            value = self.visit(node.right)
            self.current_scope.insert(name, value)
            return name
        else:
            self.error(node.left)


    def visit_Identifier(self, node):
        value = self.current_scope.get(node.value)
        if value is None:
            self.error(node.value)
        return value
            

    def visit_String(self, node):
        return node.value
        
        
    def visit_Num(self, node):
        return int(node.value)
        
        
    def visit_NoOp(self, node):
        pass
        
        
    def interpret(self):
        self.visit(self.tree)


lexer = Lexer(example)
parser = Parser(lexer)
# THIS WILL SHOW YOU TOP LEVE OF TREE
# node_visiter = NodeVisiter()
# for node in parser.parse().body:
    # print(node)
    #node_visiter.visit(node.type)



tree = parser.parse()
interpreter = Interpreter(tree)
interpreter.interpret()
