import re
def is_number(s):
    pattern = r'^-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?$'
    return re.match(pattern, s) is not None

test_strings = ["123", "-123", "123.45", "-123.45", "1.23e10", "abc", "-.123", ".123", "nan", "inf"]

for s in test_strings:
    print(f"'{s}' is a number: {is_number(s)}")