import unittest
from models import create_rule, evaluate_rule, combine_rules

class TestRuleEngine(unittest.TestCase):

    def setUp(self):
        self.data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}

    def test_create_rule(self):
        ast = create_rule("((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)")
        self.assertIsNotNone(ast)

    def test_evaluate_rule(self):
        ast = create_rule("((age > 30 AND department = 'Sales'))")
        result = evaluate_rule(ast, self.data)
        self.assertTrue(result)

    def test_combine_rules(self):
        combined_ast = combine_rules(["((age > 30 AND department = 'Sales'))", "((age < 25 AND department = 'Marketing'))"])
        self.assertIsNotNone(combined_ast)

if __name__ == '__main__':
    unittest.main()
