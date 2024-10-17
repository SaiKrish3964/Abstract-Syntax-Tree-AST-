import json
import re
class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.node_type = node_type  # 'operator' or 'operand'
        self.left = left            # Reference to left Node
        self.right = right          # Reference to right Node
        self.value = value          # Optional value for operand nodes
def parse_expression(expression):
    tokens = re.findall(r'\w+|[<>!=]=|AND|OR|\(|\)', expression)
    
    def parse(tokens):
        stack = []
        current = []
        
        for token in tokens:
            if token == '(':
                stack.append(current)
                current = []
            elif token == ')':
                node = build_ast(current)
                current = stack.pop()
                current.append(node)
            else:
                current.append(token)
        
        return build_ast(current)
    
    def build_ast(parsed_tokens):
        if not parsed_tokens:
            return None
        if len(parsed_tokens) == 1:
            token = parsed_tokens[0]
            if re.match(r'\w+', token):
                return Node('operand', value=token)
            else:
                raise ValueError("Invalid token")
        for op in ('OR', 'AND'):
            if op in parsed_tokens:
                index = parsed_tokens.index(op)
                left = build_ast(parsed_tokens[:index])
                right = build_ast(parsed_tokens[index + 1:])
                return Node('operator', left=left, right=right, value=op)
        # Handle comparisons
        for comparison in ['>', '<', '=', '>=', '<=', '!=']:
            if comparison in parsed_tokens:
                index = parsed_tokens.index(comparison)
                left = parsed_tokens[index - 1]
                right = parsed_tokens[index + 1]
                return Node('operator', 
                            left=Node('operand', value=left), 
                            right=Node('operand', value=right), 
                            value=comparison)

        raise ValueError("Invalid expression")
    return parse(tokens)
def create_rule(rule_string):
    return parse_expression(rule_string)
def combine_ast_nodes(ast1, ast2):
    # Assuming ast1 and ast2 are both root nodes of their respective ASTs
    return Node('operator', left=ast1, right=ast2, value='OR')  # Combine with OR for simplicity
def combine_rules(rules):
    combined_ast = None
    for rule in rules:
        ast = create_rule(rule)
        if combined_ast is None:
            combined_ast = ast
        else:
            combined_ast = combine_ast_nodes(combined_ast, ast)
    return combined_ast

def evaluate_node(node, data):
    if node.node_type == 'operand':
        if isinstance(node.value, str):
            return data.get(node.value)
        else:
            return node.value
    elif node.node_type == 'operator':
        left_result = evaluate_node(node.left, data)
        right_result = evaluate_node(node.right, data)
        if node.value == 'AND':
            return left_result and right_result
        elif node.value == 'OR':
            return left_result or right_result
        elif node.value in ['>', '<', '=', '>=', '<=', '!=']:
            left_value = evaluate_node(node.left, data)
            right_value = evaluate_node(node.right, data)
            if node.value == '>':
                return left_value > right_value
            elif node.value == '<':
                return left_value < right_value
            elif node.value == '=':
                return left_value == right_value
            elif node.value == '>=':
                return left_value >= right_value
            elif node.value == '<=':
                return left_value <= right_value
            elif node.value == '!=':
                return left_value != right_value
def evaluate_rule(ast, data):
    return evaluate_node(ast, data)
# Test Cases
def test_create_rule():
    rule_string = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing'))"
    ast = create_rule(rule_string)
    assert ast is not None  # Further checks on the AST structure

def test_combine_rules():
    rules = [
        "((age > 30 AND department = 'Sales'))",
        "((age < 25 AND department = 'Marketing'))"
    ]
    combined_ast = combine_rules(rules)
    assert combined_ast is not None  # Further checks on the combined AST
def test_evaluate_rule():
    data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
    ast = create_rule("((age > 30 AND department = 'Sales'))")
    result = evaluate_rule(ast, data)
    assert result is True  # Check the expected output
# Run tests
test_create_rule()
test_combine_rules()
test_evaluate_rule()
print("All tests passed!")
