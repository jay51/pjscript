import pytest
from pjscript import *
from io import StringIO
import sys


example1 = """
    var x = 2;
    log("x: ", x);

    var y = x++ * 2;
    log("y: ", y);
    log("x: ", x);

    var x = 2;
    log("x: ", x);

    var y = ++x * 2;
    log("y: ", y);
    log("x: ", x);
"""

example2 = """
    var x = 0 + add(2, 3);
    var x = x + add(2, 3);
    var x = (x * 2) / 2;
    log(x); /* should log 10*/
"""

example3 = """
    var x = 2;
    var y = x >= 2;
    log("y: ", y);
    log("x: ", x);
"""


example4 = """
    function printme(st1, st2, st3){
        log(st1);
        log(st2);
        log(st3);
        return 1;
    };
    var result = printme(1, 2, 3);
    log(result);
"""

example5 = """
    function loop(){
        var i = 0;
        for(; i < 5; i++){
            log(i);
        };
        return null;
    };
    log(loop());
"""

example6 = """
    var i = 0;
    if(i == 1){
        log("if");
    } else if (i == 0) {
        log("else if");
    } else {
        log("else");
    };

    var y = 0;
    if (y == 0){
        log("y is:", y);
    };
"""

example7 = """
    var numbers = [1, 2, 3];
    log(numbers[1]);
"""


class TestLexer:
    def test_expression(self):
        self.math_operators()
        self.post_pre_inc_dec()
        self.comparison_operators()

    def post_pre_inc_dec(self):

        # fmt: off
        expected_result = [
            "var", "IDENTIFIER", "=", "NUMBER", ";", "IDENTIFIER", "(", "STRING", ",", "IDENTIFIER", ")",
            ";", "var", "IDENTIFIER", "=", "IDENTIFIER", "++", "*", "NUMBER", ";", "IDENTIFIER", "(", "STRING",
            ",", "IDENTIFIER", ")", ";", "IDENTIFIER", "(", "STRING", ",", "IDENTIFIER", ")", ";", "var", "IDENTIFIER",
            "=", "NUMBER", ";", "IDENTIFIER", "(", "STRING", ",", "IDENTIFIER", ")", ";", "var", "IDENTIFIER", "=", "++",
            "IDENTIFIER", "*", "NUMBER", ";", "IDENTIFIER", "(", "STRING", ",", "IDENTIFIER", ")", ";", "IDENTIFIER", "(", "STRING", ",", "IDENTIFIER", ")", ";", "EOF"
        ]
        # fmt: on

        lexer = Lexer(example1)
        for idx, tok in enumerate(lexer):
            assert tok.type == expected_result[idx]

    def math_operators(self):

        # fmt: off
        expected_result = [
            "var", "IDENTIFIER", "=", "NUMBER", "+",
            "IDENTIFIER", "(", "NUMBER", ",", "NUMBER", ")", ";",
            "var", "IDENTIFIER", "=", "IDENTIFIER", "+", "IDENTIFIER",
            "(", "NUMBER", ",", "NUMBER", ")", ";", "var", "IDENTIFIER",
            "=", "(", "IDENTIFIER", "*", "NUMBER", ")", "/", "NUMBER", ";",
            "IDENTIFIER", "(", "IDENTIFIER", ")", ";", "EOF"
        ]
        # fmt: on

        lexer = Lexer(example2)
        for idx, tok in enumerate(lexer):
            assert tok.type == expected_result[idx]

    def comparison_operators(self):
        # fmt: off
        expected_result = [
            "var", "IDENTIFIER", "=", "NUMBER", ";", "var", "IDENTIFIER", "=", "IDENTIFIER", ">=",
            "NUMBER", ";", "IDENTIFIER", "(", "STRING", ",", "IDENTIFIER", ")", ";", "IDENTIFIER", "(",
            "STRING", ",", "IDENTIFIER", ")", ";", "EOF"
        ]
        # fmt: on

        lexer = Lexer(example3)
        for idx, tok in enumerate(lexer):
            assert tok.type == expected_result[idx]

    def test_function(self):
        # fmt: off
        expected_result = [
            "function", "IDENTIFIER", "(", "IDENTIFIER", ",", "IDENTIFIER", ",", "IDENTIFIER", ")",
            "{", "IDENTIFIER", "(", "IDENTIFIER", ")", ";", "IDENTIFIER", "(", "IDENTIFIER", ")", ";",
            "IDENTIFIER", "(", "IDENTIFIER", ")", ";", "return", "NUMBER", ";", "}", ";", "var", "IDENTIFIER",
            "=", "IDENTIFIER", "(", "NUMBER", ",", "NUMBER", ",", "NUMBER", ")", ";", "IDENTIFIER", "(", "IDENTIFIER", ")", ";", "EOF"
        ]
        # fmt: on

        lexer = Lexer(example4)
        for idx, tok in enumerate(lexer):
            assert tok.type == expected_result[idx]

    def test_forloop(self):
        # fmt: off
        expected_result = [
            "function", "IDENTIFIER", "(", ")", "{", "var", "IDENTIFIER", "=", "NUMBER", ";", "for", "(", ";", "IDENTIFIER", "<", "NUMBER",
            ";", "IDENTIFIER", "++", ")", "{", "IDENTIFIER", "(", "IDENTIFIER", ")", ";", "}", ";", "return", "null", ";", "}", ";",
            "IDENTIFIER", "(", "IDENTIFIER", "(",")", ")", ";", "EOF"
        ]
        # fmt: on

        lexer = Lexer(example5)
        for idx, tok in enumerate(lexer):
            assert tok.type == expected_result[idx]

    def test_if_else(self):
        # fmt: off
        expected_result = [
            "var", "IDENTIFIER", "=", "NUMBER", ";", "if", "(", "IDENTIFIER", "==", "NUMBER", ")", "{", "IDENTIFIER",
            "(", "STRING", ")", ";", "}", "else", "if", "(", "IDENTIFIER", "==", "NUMBER", ")", "{", "IDENTIFIER", "(",
            "STRING", ")", ";", "}", "else", "{", "IDENTIFIER", "(", "STRING", ")", ";", "}", ";", "var", "IDENTIFIER", "=",
            "NUMBER", ";", "if", "(", "IDENTIFIER", "==", "NUMBER", ")", "{", "IDENTIFIER", "(", "STRING", ",", "IDENTIFIER", ")", ";", "}", ";", "EOF"
            ]
        # fmt: on

        lexer = Lexer(example6)
        for idx, tok in enumerate(lexer):
            assert tok.type == expected_result[idx]

    def test_array(self):
        # fmt: off
        expected_result = [
            "var", "IDENTIFIER", "=", "[", "NUMBER", ",", "NUMBER", ",", "NUMBER", "]", ";",
            "IDENTIFIER", "(", "IDENTIFIER", "[", "NUMBER", "]", ")", ";", "EOF"
        ]
        # fmt: on

        lexer = Lexer(example7)
        for idx, tok in enumerate(lexer):
            assert tok.type == expected_result[idx]


class TestParser:
    def test_expression(self):

        self.post_pre_inc_dec()
        self.math_operators()
        self.comparison_operators()
        self.comparison_operators()

    def post_pre_inc_dec(self):
        expected_result = [
            VarDeclaration,
            CallExpression,
            VarDeclaration,
            CallExpression,
            CallExpression,
            VarDeclaration,
            CallExpression,
            VarDeclaration,
            CallExpression,
            CallExpression,
            NoOp,
        ]

        lexer = Lexer(example1)
        parser = Parser(lexer)

        result = []
        for node in parser.parse().body:
            result.append(node)

        for idx, node in enumerate(result):
            assert isinstance(node, expected_result[idx])

    def math_operators(self):
        expected_result = [
            VarDeclaration,
            VarDeclaration,
            VarDeclaration,
            CallExpression,
            NoOp,
        ]

        lexer = Lexer(example2)
        parser = Parser(lexer)

        result = []
        for node in parser.parse().body:
            result.append(node)

        for idx, node in enumerate(result):
            assert isinstance(node, expected_result[idx])

    def comparison_operators(self):
        expected_result = [
            VarDeclaration,
            VarDeclaration,
            CallExpression,
            CallExpression,
            NoOp,
        ]

        lexer = Lexer(example3)
        parser = Parser(lexer)

        result = []
        for node in parser.parse().body:
            result.append(node)

        for idx, node in enumerate(result):
            assert isinstance(node, expected_result[idx])

    def test_function(self):
        expected_result = [FuncDeclaration, VarDeclaration, CallExpression, NoOp]

        lexer = Lexer(example4)
        parser = Parser(lexer)

        result = []
        for node in parser.parse().body:
            result.append(node)

        for idx, node in enumerate(result):
            assert isinstance(node, expected_result[idx])

    def test_forloop(self):
        expected_result = [FuncDeclaration, CallExpression, NoOp]

        lexer = Lexer(example5)
        parser = Parser(lexer)

        result = []
        for node in parser.parse().body:
            result.append(node)

        for idx, node in enumerate(result):
            assert isinstance(node, expected_result[idx])

    def test_if_else(self):
        expected_result = [VarDeclaration, IfStmt, VarDeclaration, IfStmt, NoOp]

        lexer = Lexer(example6)
        parser = Parser(lexer)

        result = []
        for node in parser.parse().body:
            result.append(node)

        for idx, node in enumerate(result):
            assert isinstance(node, expected_result[idx])

    def test_array(self):
        expected_result = [VarDeclaration, CallExpression]

        lexer = Lexer(example7)
        parser = Parser(lexer)

        result = []
        for node in parser.parse().body:
            result.append(node)

        for idx, node in enumerate(result):
            assert isinstance(node, expected_result[idx])


class TestInterpreter:
    def test_expression(self):
        self.post_pre_inc_dec()
        self.math_operators()
        self.comparison_operators()

    def post_pre_inc_dec(self):
        expected_result = StringIO()
        print("x:  2", file=expected_result, end=" \n")
        print("y:  4", file=expected_result, end=" \n")
        print("x:  3", file=expected_result, end=" \n")
        print("x:  2", file=expected_result, end=" \n")
        print("y:  6", file=expected_result, end=" \n")
        print("x:  3", file=expected_result, end=" \n")

        tmp_stdout = StringIO()
        sys.stdout = tmp_stdout
        lexer = Lexer(example1)
        tree = Parser(lexer).parse()
        interpreter = Interpreter(tree)
        interpreter.interpret()
        sys.stdout = sys.__stdout__
        assert tmp_stdout.getvalue() == expected_result.getvalue()

    def math_operators(self):
        expected_result = StringIO()
        print("10", file=expected_result, end=" \n")

        tmp_stdout = StringIO()
        sys.stdout = tmp_stdout
        lexer = Lexer(example2)
        tree = Parser(lexer).parse()
        interpreter = Interpreter(tree)
        interpreter.interpret()
        sys.stdout = sys.__stdout__
        assert tmp_stdout.getvalue() == expected_result.getvalue()

    def comparison_operators(self):
        expected_result = StringIO()
        print("y:  True", file=expected_result, end=" \n")
        print("x:  2", file=expected_result, end=" \n")

        tmp_stdout = StringIO()
        sys.stdout = tmp_stdout
        lexer = Lexer(example3)
        tree = Parser(lexer).parse()
        interpreter = Interpreter(tree)
        interpreter.interpret()
        sys.stdout = sys.__stdout__
        assert tmp_stdout.getvalue() == expected_result.getvalue()

    def test_function(self):
        expected_result = StringIO()
        print("1", file=expected_result, end=" \n")
        print("2", file=expected_result, end=" \n")
        print("3", file=expected_result, end=" \n")
        print("1", file=expected_result, end=" \n")

        tmp_stdout = StringIO()
        sys.stdout = tmp_stdout
        lexer = Lexer(example4)
        tree = Parser(lexer).parse()
        interpreter = Interpreter(tree)
        interpreter.interpret()
        sys.stdout = sys.__stdout__
        assert tmp_stdout.getvalue() == expected_result.getvalue()

    def test_forloop(self):
        expected_result = StringIO()
        print("0", file=expected_result, end=" \n")
        print("1", file=expected_result, end=" \n")
        print("2", file=expected_result, end=" \n")
        print("3", file=expected_result, end=" \n")
        print("4", file=expected_result, end=" \n")
        print("null", file=expected_result, end=" \n")

        tmp_stdout = StringIO()
        sys.stdout = tmp_stdout
        lexer = Lexer(example5)
        tree = Parser(lexer).parse()
        interpreter = Interpreter(tree)
        interpreter.interpret()
        sys.stdout = sys.__stdout__
        assert tmp_stdout.getvalue() == expected_result.getvalue()

    def test_if_else(self):
        expected_result = StringIO()
        print("else if", file=expected_result, end=" \n")
        print("y is: 0", file=expected_result, end=" \n")

        tmp_stdout = StringIO()
        sys.stdout = tmp_stdout
        lexer = Lexer(example6)
        tree = Parser(lexer).parse()
        interpreter = Interpreter(tree)
        interpreter.interpret()
        sys.stdout = sys.__stdout__
        assert tmp_stdout.getvalue() == expected_result.getvalue()

    def test_operators_order(self):
        example = """
            if( 1 == 6 || 3 == 3 ){
                log("yes");
            };

            if( 1 + 6 > 3 + 3 ){
                log("yes");
            };

            if( 1 + 6 > 3 + 3 && 1 == 1 ){
                log("yes");
            };

            if(!(1 != 1)) {
                log("yes");
            };
        """
        expected_result = StringIO()
        print("yes", file=expected_result, end=" \n")
        print("yes", file=expected_result, end=" \n")
        print("yes", file=expected_result, end=" \n")
        print("yes", file=expected_result, end=" \n")

        tmp_stdout = StringIO()
        sys.stdout = tmp_stdout
        lexer = Lexer(example)
        tree = Parser(lexer).parse()
        interpreter = Interpreter(tree)
        interpreter.interpret()
        sys.stdout = sys.__stdout__
        assert tmp_stdout.getvalue() == expected_result.getvalue()

    def test_array(self):
        expected_result = StringIO()
        print("2", file=expected_result, end=" \n")

        tmp_stdout = StringIO()
        sys.stdout = tmp_stdout
        lexer = Lexer(example7)
        tree = Parser(lexer).parse()
        interpreter = Interpreter(tree)
        interpreter.interpret()
        sys.stdout = sys.__stdout__
        assert tmp_stdout.getvalue() == expected_result.getvalue()

    def test_array_indexing(self):
        example = """
            var list = [0, [1, 2], [3, [4] ], 5 ];
            list[0] = 10;
            list[1][0] = 10;
            list[2][1][0] = 10;
            log(list);
            log(list[2][1][0]);
);
        """
        expected_result = StringIO()
        print("[10, [10, 2], [3, [10]], 5]", file=expected_result, end=" \n")
        print("10", file=expected_result, end=" \n")

        tmp_stdout = StringIO()
        sys.stdout = tmp_stdout
        lexer = Lexer(example)
        tree = Parser(lexer).parse()
        interpreter = Interpreter(tree)
        interpreter.interpret()
        sys.stdout = sys.__stdout__
        assert tmp_stdout.getvalue() == expected_result.getvalue()

    def test_anonymous_function(self):
        example = """
            var print = function(){
                log("working");
            };
            print();

            print = function(){
                log("yes");
            };
            print();
        """
        expected_result = StringIO()
        print("working", file=expected_result, end=" \n")
        print("yes", file=expected_result, end=" \n")

        tmp_stdout = StringIO()
        sys.stdout = tmp_stdout
        lexer = Lexer(example)
        tree = Parser(lexer).parse()
        interpreter = Interpreter(tree)
        interpreter.interpret()
        sys.stdout = sys.__stdout__
        assert tmp_stdout.getvalue() == expected_result.getvalue()

    def test_methods(self):
        example = """
            var person = {
                age: { born: 23, died: 28 },
                features: {
                    hair: { curly: [1, 2, 3], notcurly: 0 }
                },

                printname: function(){
                    log("printname inside object person");
                    return 1;
                }
            };

            log(person.features.hair.curly[1]);
            log(person.printname());
        """
        expected_result = StringIO()
        print("2", file=expected_result, end=" \n")
        print("printname inside object person", file=expected_result, end=" \n")
        print("1", file=expected_result, end=" \n")  # return value of printname

        tmp_stdout = StringIO()
        sys.stdout = tmp_stdout
        lexer = Lexer(example)
        tree = Parser(lexer).parse()
        interpreter = Interpreter(tree)
        interpreter.interpret()
        sys.stdout = sys.__stdout__
        assert tmp_stdout.getvalue() == expected_result.getvalue()
