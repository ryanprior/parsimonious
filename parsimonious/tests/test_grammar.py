from unittest import TestCase

from nose.tools import eq_

from parsimonious.nodes import Node
from parsimonious.grammar import peg_grammar


class PegGrammarTests(TestCase):
    """Tests for the expressions in the grammar that parses the grammar definition syntax"""

    def test_ws(self):
        text = ' \t\t'
        eq_(peg_grammar['ws'].parse(text), Node('ws', text, 0, 3))

    def test_quantifier(self):
        text = '*'
        eq_(peg_grammar['quantifier'].parse(text), Node('quantifier', text, 0, 1))
        text = '?'
        eq_(peg_grammar['quantifier'].parse(text), Node('quantifier', text, 0, 1))
        text = '+'
        eq_(peg_grammar['quantifier'].parse(text), Node('quantifier', text, 0, 1))

    def test_literal(self):
        text = '"anything but quotes#$*&^"'
        eq_(peg_grammar['literal'].parse(text), Node('literal', text, 0, len(text)))

    def test_regex(self):
        text = '~"[a-zA-Z_][a-zA-Z_0-9]*"LI'
        eq_(peg_grammar['regex'].parse(text),
            Node('regex', text, 0, len(text), children=[
                 Node('', text, 0, 1),
                 Node('literal', text, 1, 25),
                 Node('', text, 25, 27)]))

    def test_successes(self):
        """Make sure the PEG recognition grammar succeeds on various inputs."""
        assert peg_grammar['label'].parse('_')
        assert peg_grammar['label'].parse('jeff')
        assert peg_grammar['label'].parse('_THIS_THING')

        assert peg_grammar['atom'].parse('some_label')
        assert peg_grammar['atom'].parse('"some literal"')
        assert peg_grammar['atom'].parse('~"some regex"i')

        assert peg_grammar['quantified'].parse('~"some regex"i*')
        assert peg_grammar['quantified'].parse('thing+')
        assert peg_grammar['quantified'].parse('"hi"?')

        assert peg_grammar['term'].parse('this')
        assert peg_grammar['term'].parse('that+')

        assert peg_grammar['sequence'].parse('this that? other')

        assert peg_grammar['ored'].parse('this / that+ / "other"')

        assert peg_grammar['anded'].parse('this & that+ & "other"')

        assert peg_grammar['poly_term'].parse('this & that+ & "other"')
        assert peg_grammar['poly_term'].parse('this / that? / "other"+')
        assert peg_grammar['poly_term'].parse('this? that other*')

        assert peg_grammar['rhs'].parse('this')
        assert peg_grammar['rhs'].parse('this? that other*')

        assert peg_grammar['rule'].parse('this = that\r')
        assert peg_grammar['rule'].parse('this = the? that other* \t\r')
        assert peg_grammar['rule'].parse('the=~"hi*"\n')  # test $ as eol

        assert peg_grammar.parse('''
            this = the? that other*
            that = "thing"
            the=~"hi*"
            other = "ahoy hoy"
            ''')
