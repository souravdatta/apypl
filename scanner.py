from lexer import lex
from lexer import Tokens


def scan_tokens_r2l(s):
    lex.input(s)
    tokens = []
    
    while True:
        tok = lex.token()

        if not tok:
            break

        tokens.append(tok)

    tokens.reverse() 
    return tokens


def extract_tokens(tokens, start_index, for_token, match_token_str):
    start_index += 1
    match_count = 1
    extracted_tokens = []

    for ti in range(start_index, len(tokens)):
        tok = tokens[ti]

        if match_count == 0:
            extracted_tokens = extracted_tokens[1:]
            extracted_tokens.reverse()
            return extracted_tokens, tokens[ti:]

        if tok.type == for_token.type and tok.value == for_token.value:
            match_count += 1
        elif tok.value == match_token_str:
            match_count -= 1

        extracted_tokens.insert(0, tok)

    raise ValueError('Unmatched token!!')


def eval_tree(tokens):
    def peek(stk):
        if len(stk) == 0:
            return None

        return stk[0]


    def push_to_list(x, y):
        if len(y) == 0 or (x is None):
            y.insert(0, [])
        if x:
            head = y[0]
            head.insert(0, x)

    op_stack = []
    val_stack = []

    token_i = 0

    while True:
        if token_i >= len(tokens):
            break

        cur_token = tokens[token_i]

        if Tokens.is_operand(cur_token):
            push_to_list(cur_token.value, val_stack)
            token_i += 1
        elif Tokens.is_operator(cur_token):
            prev_op = peek(op_stack)

            if prev_op:
                op_stack = op_stack[1:]
                args = [a for a in val_stack]
                val_stack = []
                push_to_list(apply_op(prev_op, args), val_stack)

            push_to_list(cur_token.value, op_stack)
            push_to_list(None, val_stack)
            token_i += 1
        elif Tokens.is_close_parent(cur_token):
            extracted_tokens, rest_tokens = extract_tokens(tokens, token_i, cur_token, '(')
            push_to_list(eval_tree(extracted_tokens), val_stack)
            tokens = rest_tokens
            token_i = 0
        elif Tokens.is_close_brace(cur_token):
            extracted_tokens, rest_tokens = extract_tokens(tokens, token_i, cur_token, '{')
            push_to_list(eval_tree(extracted_tokens), val_stack)
            tokens = rest_tokens
            token_i = 0
        elif Tokens.is_close_bracket(cur_token):
            extracted_tokens, rest_tokens = extract_tokens(tokens, token_i, cur_token, '[')
            push_to_list(eval_tree(extracted_tokens), val_stack)
            tokens = rest_tokens
            token_i = 0
        else:
            token_i += 1
    
    last_op = peek(op_stack)
    if last_op:
        return apply_op(last_op, val_stack)
    else:
        return val_stack


def apply_op(op, args):
    return (op[0], args)


if __name__ == '__main__':
    data = '''
    foo ← {a + w} +/ a b cd34 23.4 (2 3⍴1 2 3 [4 * 5] 6)
    '''
    print(eval_tree(scan_tokens_r2l(data)))
