import ply.lex as lex


class Tokens:
    (
        NUMBER,
        SYMBOL,
        OPERATOR,
        OPAREN,
        CPAREN,
        OBRACE,
        CBRACE,
        OBRACKET,
        CBRACKET
    ) = (
        'NUMBER',
        'SYMBOL',
        'OPERATOR',
        'OPAREN',
        'CPAREN',
        'OBRACE',
        'CBRACE',
        'OBRACKET',
        'CBRACKET'
    )

    @staticmethod
    def is_operand(s):
        return s.type == Tokens.NUMBER or s.type == Tokens.SYMBOL

    @staticmethod
    def is_operator(s):
        return s.type == Tokens.OPERATOR

    @staticmethod
    def is_close_parent(s):
        return s.type == Tokens.CPAREN

    @staticmethod
    def is_close_brace(s):
        return s.type == Tokens.CBRACE

    @staticmethod
    def is_close_bracket(s):
        return s.type == Tokens.CBRACKET


tokens = (
    'NUMBER',
    'SYMBOL',
    'OPERATOR',
    'OPAREN',
    'CPAREN',
    'OBRACE',
    'CBRACE',
    'OBRACKET',
    'CBRACKET'
)


t_OPAREN = r'\('
t_CPAREN = r'\)'
t_OBRACE = r'\{'
t_CBRACE = r'\}'
t_OBRACKET = r'\['
t_CBRACKET = r'\]'
t_SYMBOL = r'[a-zA-Z]\w*'

# Unicode APL symbols
t_OPERATOR = r'⍴|←|\*|/|\+'


def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()


if __name__ == '__main__':
    data = '''
    foo ← {a + w} +/ a b cd34 23.4 (2 3⍴1 2 3 4 5 6)
    '''

    lexer.input(data)

    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

