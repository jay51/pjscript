example = """
/* comment

var age = 2;
var name = "jack";

var newage = age;
name = "jack and me";

log(1, "it's working fuck yea", name);

var x = add(age, add(2,3));
log(x);
*/


function sayHi(){

    log(x);
};

sayHi();

"""

class Tokens():
    PLUS        = "+"
    MINUS       = "-"
    MUL         = "*"
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
    var         = "var"
    function    = "function"
    
    
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
        while(self.curr_char != "*" and self.peek() != "/"):
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

        if hasattr(Tokens, id):
            token_type = getattr(Tokens, id) # RESERVED_KEYWORDS (var, log)
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

            if self.curr_char == Tokens.PLUS:
                self.advance()
                return Token(Tokens.PLUS, Tokens.PLUS)
            if self.curr_char == Tokens.MINUS:
                self.advance()
                return Token(Tokens.MINUS, Tokens.MINUS)
            if self.curr_char == Tokens.MUL:
                self.advance()
                return Token(Tokens.MUL, Tokens.MUL)
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
# lexer = Lexer(example)
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


CallExpression
    callee: id
    args: []


VarDeclaration, # var name = "jack";
    type: var
    left: id
    right: expression



Var_assigne, # var name = "jack";
    left: id
    right: expression


expression: String
            | Num
            | id


id: CallExpression
    | Var_assigne
    | identifier


identifier: [a-zA-Z][a-zA-Z0-9_]

"""


class Program():
    def __init__(self, body):
        self.body = body
        
        
        
class Num():
    def __init__(self, token):
        self.token = token
        self.value = token.value
        
        
class String():
    def __init__(self, token):
        self.token = token
        self.value = token.value


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
        return "VarDeclaration<{} : {}  -> {}>".format(self.left, self.right.__class__.__name__, self.right.value)

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
            
            
    def program(self):
        body = []
        body.append(self.statement())
        while(self.curr_token.type == Tokens.SEMI):
            self.consume(Tokens.SEMI)
            body.append(self.statement())
        return Program(body)
        
        
        
    def statement(self):
        if self.curr_token.type == Tokens.var:
            node = self.var_declaration()
        elif self.curr_token.type == Tokens.IDENTIFIER:
            node = self.id()
        elif self.curr_token.type == Tokens.function:
            node = self.func_declaration()

        elif self.curr_token.type == Tokens.EOF:
            return NoOp()
        return node
        
        
    def var_declaration(self):
        self.consume(Tokens.var)
        left = self.curr_token.value
        self.consume(Tokens.IDENTIFIER)
        self.consume(Tokens.ASSIGN)
        right = self.expression()
        return VarDeclaration(left, right)

        
    def func_declaration(self):
        self.consume(Tokens.function)
        name  = self.curr_token.value
        self.consume(Tokens.IDENTIFIER)
        self.consume(Tokens.LPAREN)
        params = [self.expression()]
        while(self.curr_token.type == Tokens.COMMA):
            self.consume(Tokens.COMMA)
            params.append(self.expression())

        self.consume(Tokens.RPAREN)
        self.consume(Tokens.LCURLY)
        body = [self.statement()]
        while(self.curr_token.type == Tokens.SEMI):
            self.consume(Tokens.SEMI)
            body.append(self.statement)

        self.consume(Tokens.RCURLY)
        return FuncDeclaration(name, params, body)



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
        
        
    def expression(self):
        if self.curr_token.type == Tokens.STRING:
            return self.parse_string()
        elif self.curr_token.type == Tokens.NUMBER:
            return self.parse_number()
        elif self.curr_token.type == Tokens.IDENTIFIER:
            return self.id()
        # print("not considerd", self.curr_token.type)
        return NoOp()
        
        
    def parse_string(self):
        token = self.curr_token
        self.consume(Tokens.STRING)
        return String(token)
        
    def parse_number(self):
        token = self.curr_token
        self.consume(Tokens.NUMBER)
        return Num(token)
        
    def parse(self):
        program = self.program()
        return program
        
        
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
        self.symbol_table = dict()
        self.tree = tree
        
    def error(self, val):
        raise Exception("var {} not defined".format(val))
        
    def visit_CallExpression(self, node):
        args = node.args
        function = node.identifier
        # we support only the log function right now
        if getattr(BuiltIn, function, None):
            function = getattr(BuiltIn, function)
            arguments = []
            for param in args:
                arguments.append(self.visit(param))
            return function(*arguments)
        else:
            return NoOp()
            

    def visit_VarDeclaration(self, node):
        name = node.left
        value = self.visit(node.right)
        self.symbol_table[name] = value
        return name


    def visit_FuncDeclaration(self, node):
        self.symbol_table[node.name] = node
        return node.name


    # THIS IS FOR REASSIGNMENT
    def visit_Assignment(self, node):
        if self.symbol_table.get(node.left):
            name = node.left
            value = self.visit(node.right)
            self.symbol_table[name] = value
            return name
        else:
            self.error(node.left)


    def visit_Identifier(self, node):
        value = self.symbol_table.get(node.value)
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
        body = self.tree.body
        for node in body:
            self.visit(node)
            
            
            
lexer = Lexer(example)
parser = Parser(lexer)
# THIS WILL SHOW YOU TOP LEVE OF TREE
#node_visiter = NodeVisiter()
# for node in parser.parse().body:
    # print(node)
    #node_visiter.visit(node.type)
    
    
tree = parser.parse()
interpreter = Interpreter(tree)
interpreter.interpret()
