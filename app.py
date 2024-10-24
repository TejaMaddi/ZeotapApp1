from flask import Flask, request, jsonify
from models import create_rule, combine_rules, evaluate_rule, init_db

app = Flask(__name__)

# Initialize the database
init_db()

@app.route('/create_rule', methods=['POST'])
def api_create_rule():
    rule_string = request.json.get('rule_string')
    ast = create_rule(rule_string)
    return jsonify(ast.to_dict()), 200


@app.route('/combine_rules', methods=['POST'])
def api_combine_rules():
    rules = request.json.get('rules')
    combined_ast = combine_rules(rules)  # Assuming combine_rules returns a Node
    return jsonify(combined_ast.to_dict()), 200  # Convert to dict


@app.route('/evaluate_rule', methods=['POST'])
def api_evaluate_rule():
    ast = request.json.get('ast')
    data = request.json.get('data')
    result = evaluate_rule(ast, data)
    return jsonify({"result": result}), 200


if __name__ == '__main__':
    app.run(debug=True)
