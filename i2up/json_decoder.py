#! /usr/bin/python3
import json
import re


class JsonDecoder:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def decode(self):
        token_type, token_value = self.tokens[self.pos]
        if token_type == 'LBRACE':
            return self._decode_object()
        elif token_type == 'LBRACKET':
            return self._decode_array()
        else:
            raise ValueError("Invalid JSON start")

    def _decode_object(self):
        obj = {}
        self.pos += 1  # Skip '{'

        while True:
            token_type, token_value = self.tokens[self.pos]

            if token_type == 'RBRACE':
                self.pos += 1  # Skip '}'
                return obj

            if token_type != 'STRING':
                raise ValueError("Expected string key in object")

            key = token_value
            self.pos += 1

            token_type, token_value = self.tokens[self.pos]
            if token_type != 'COLON':
                raise ValueError("Expected ':' after key in object")

            self.pos += 1  # Skip ':'
            obj[key] = self._decode_value()

            token_type, token_value = self.tokens[self.pos]
            if token_type == 'RBRACE':
                self.pos += 1  # Skip '}'
                return obj

            if token_type != 'COMMA':
                raise ValueError("Expected ',' or '}' in object")

            self.pos += 1  # Skip ','

    def _decode_array(self):
        arr = []
        self.pos += 1  # Skip '['

        while True:
            token_type, token_value = self.tokens[self.pos]

            if token_type == 'RBRACKET':
                self.pos += 1  # Skip ']'
                return arr

            arr.append(self._decode_value())

            token_type, token_value = self.tokens[self.pos]
            if token_type == 'RBRACKET':
                self.pos += 1  # Skip ']'
                return arr

            if token_type != 'COMMA':
                raise ValueError("Expected ',' or ']' in array")

            self.pos += 1  # Skip ','

    def _decode_value(self):
        token_type, token_value = self.tokens[self.pos]
        # self.pos += 1

        if token_type == 'LBRACE':
            return self._decode_object()
        elif token_type == 'LBRACKET':
            return self._decode_array()
        elif token_type in ('STRING', 'NUMBER', 'BOOLEAN', 'NULL'):
            self.pos += 1
            return token_value
        else:
            raise ValueError(f"Unexpected token: {token_type}")


# Example usage
json_text = '''
{
    "name": "John Doe",
    "age": 30,
    "is_employee": true,
    "address": {
        "street": "123 Main St",
        "city": "Anytown",
        "postal_code": "12345"
    },
    "phone_numbers": [
        {
            "type": "home",
            "number": "555-1234"
        },
        {
            "type": "work",
            "number": "555-5678"
        }
    ],
    "skills": [
        "Python",
        "Excel",
        "Data Analysis"
    ]
}
'''


def tokenize(text):
    # Regular expressions for tokenizing JSON
    token_specification = [
        ('NUMBER',   r'-?\d+(\.\d*)?([eE][+-]?\d+)?'),  # Integer or decimal number
        ('STRING',   r'"(\\.|[^"\\])*"'),               # String
        ('BOOLEAN',  r'\b(true|false)\b'),              # Boolean
        ('NULL',     r'\bnull\b'),                      # Null
        ('LBRACE',   r'\{'),                            # Left brace
        ('RBRACE',   r'\}'),                            # Right brace
        ('LBRACKET', r'\['),                            # Left bracket
        ('RBRACKET', r'\]'),                            # Right bracket
        ('COMMA',    r','),                             # Comma
        ('COLON',    r':'),                             # Colon
        ('WHITESPACE', r'[ \t\n]+'),                    # Whitespace (to be ignored)
    ]

    token_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    get_token = re.compile(token_regex).match
    line_no = 1
    line_start = 0
    mo = get_token(text)
    tokens = []

    while mo is not None:
        kind = mo.lastgroup
        value = mo.group(kind)
        if kind == 'WHITESPACE':
            pass
        elif kind == 'NUMBER':
            if '.' in value or 'e' in value or 'E' in value:
                value = float(value)
            else:
                value = int(value)
            tokens.append((kind, value))
        elif kind == 'STRING':
            tokens.append((kind, value[1:-1]))
        elif kind == 'BOOLEAN':
            value = (value == 'true')
            tokens.append((kind, value))
        elif kind == 'NULL':
            tokens.append((kind, None))
        else:
            tokens.append((kind, value))
        mo = get_token(text, mo.end())

    if mo is not None:
        raise RuntimeError(f'Unexpected character {text[mo.start()]} on line {line_no}')

    tokens.append(('EOF', None))  # End of file
    return tokens


def parse_json(text):
    tokens = tokenize(text)
    decoder = JsonDecoder(tokens)
    return decoder.decode()


def main():
    parsed_json = parse_json(json_text)
    print(json.dumps(parsed_json, indent=4))


if __name__ == "__main__":
    main()
