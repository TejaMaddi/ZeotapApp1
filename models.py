import sqlite3

class Node:
    def __init__(self, type, left=None, right=None, value=None):
        self.type = type
        self.left = left
        self.right = right
        self.value = value

    def to_dict(self):
        return {
            "type": self.type,
            "value": self.value,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None,
        }


def init_db():
    conn = sqlite3.connect('rules.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule_string TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def create_rule(rule_string):
    root = Node("operator", "AND")
    left = Node("operator", "OR", 
                Node("operator", "AND", 
                     Node("operand", "age > 30"), 
                     Node("operand", "department = 'Sales'")),
                Node("operator", "AND", 
                     Node("operand", "age < 25"), 
                     Node("operand", "department = 'Marketing'"))
    )
    root.left = left
    root.right = Node("operator", "OR", 
                      Node("operand", "salary > 50000"), 
                      Node("operand", "experience > 5"))
    return root

def combine_rules(rules):
    # Combine rules logic (this is just a simple example)
    nodes = [create_rule(rule) for rule in rules]  # Assume create_rule returns a Node
    # Implement logic to combine the nodes efficiently
    # For example, using an AND operator for all rules
    if not nodes:
        return None
    combined_node = Node("operator", left=nodes[0], right=None)  # Initial node
    current = combined_node
    for node in nodes[1:]:
        current.right = node  # Link next nodes
        current = node
    return combined_node


def evaluate_rule(ast, data):
    if ast['type'] == "operand":
        if ">" in ast['value']:
            attribute, value = ast['value'].split(" > ")
            return data[attribute] > int(value)
        elif "=" in ast['value']:
            attribute, value = ast['value'].split(" = ")
            return data[attribute] == value.strip("'")
    elif ast['type'] == "operator":
        if ast['value'] == "AND":
            return evaluate_rule(ast['left'], data) and evaluate_rule(ast['right'], data)
        elif ast['value'] == "OR":
            return evaluate_rule(ast['left'], data) or evaluate_rule(ast['right'], data)

    return False

