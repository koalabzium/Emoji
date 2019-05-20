import unittest
from lexer import lexer
from checkWithOriginal import lex


class TestLexer(unittest.TestCase):

    def test_comment(self):
        self.assertEqual(lexer("(☯‿├┬┴┬┴ Zignoruj mnie proszę"), [])

    def test_empty(self):
        self.assertEqual(lexer(""), [])

    def test_spaces(self):
        self.assertEqual(lexer("             \n\n     \n"), [])

    def test_plus(self):
        self.assertEqual(lexer("✿"), [{'toktype': 7, 'value': None}])

    def test_minus(self):
        self.assertEqual(lexer("❤"), [{'toktype': 8, 'value': None}])

    def test_star(self):
        self.assertEqual(lexer("✰"), [{'toktype': 9, 'value': None}])

    def test_slash(self):
        self.assertEqual(lexer("๑"), [{'toktype': 10, 'value': None}])

    def test_lparen(self):
        self.assertEqual(lexer("{"), [{'toktype': 11, 'value': None}])

    def test_rparen(self):
        self.assertEqual(lexer("}"), [{'toktype': 12, 'value': None}])

    def test_int(self):
        self.assertEqual(lexer("1"), [{'toktype': 3, 'value': 1}])
        self.assertEqual(lexer("145"), [{'toktype': 3, 'value': 145}])

    def test_float(self):
        self.assertEqual(lexer("0.192"), [{'toktype': 4, 'value': 0.192}])
        self.assertEqual(lexer("123.192"), [{'toktype': 4, 'value': 123.192}])
        self.assertEqual(lexer("2.0"), [{'toktype': 4, 'value': 2.0}])

    def test_equasion(self):
        self.assertEqual(lexer("12 ❤ {3.5 ✿ 4} ๑ 7 ✰ 3"), [{'toktype': 3, 'value': 12}, {'toktype': 8, 'value': None}, {'toktype': 11, 'value': None}, {'toktype': 4, 'value': 3.5}, {'toktype': 7, 'value': None}, {'toktype': 3, 'value': 4}, {'toktype': 12, 'value': None}, {'toktype': 10, 'value': None}, {'toktype': 3, 'value': 7}, {'toktype': 9, 'value': None}, {'toktype': 3, 'value': 3}])

    def test_while(self):
        self.assertEqual(lexer("<(_ _<(_ _<(_  a _)>_ _)>_ _)>"),[{'toktype': 14, 'value': None}, {'toktype': 1, 'value': 'a'}, {'toktype': 15, 'value': None}])
        self.assertEqual(lexer("<(_ _<(_ _<(_  a _)>_ _)>_ _)> ʢᵕᴗᵕʡ"),[{'toktype': 14, 'value': None}, {'toktype': 1, 'value': 'a'}, {'toktype': 15, 'value': None}, {'toktype': 16, 'value': None}])

    def test_equal(self):
        self.assertEqual(lexer("ʕ•ᴥ•ʔ"), [{'toktype': 19, 'value': None}])


    def test_less(self):
        self.assertEqual(lexer("ʕₒᴥₒʔ"), [{'toktype': 20, 'value': None}])

    def test_more(self):
        self.assertEqual(lexer("ʕ'ᴥ'ʔ"), [{'toktype': 21, 'value': None}])
        self.assertEqual(lexer("2 ʕ'ᴥ'ʔ 9"), [{'toktype': 3, 'value': 2}, {'toktype': 21, 'value': None}, {'toktype': 3, 'value': 9}])

    def test_variable_assignment(self):
        self.assertEqual(lexer("a (^._.^)ﾉ 7"), [{'toktype': 1, 'value': 'a'}, {'toktype': 6, 'value': None}, {'toktype': 3, 'value': 7}])

    def test_print(self):
        self.assertEqual(lexer("φ（．．）12"), [{'toktype': 0, 'value': None}, {'toktype': 3, 'value': 12}])

    def test_both(self):

        with open('demo.txt') as f:
            read_data = f.read()

        with open('demo2.txt') as f:
            read_data2 = f.read()
        self.assertEqual(lexer(read_data), lex(read_data2))


if __name__ == '__main__':
    unittest.main()
