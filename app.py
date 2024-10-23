from flask import Flask, request, jsonify, render_template
from config import Config, db, Rule # Import db and Rule from config
from module import create_rules, evaluate_rule, combine_rules
import json

app = Flask(__name__)
app.config.from_object(Config)

# Initialize db with the app
db.init_app(app)


#---------------------------------------------------------------------------------------------------------------------------------

# New endpoint to fetch all rule names
@app.route('/get_rule_names', methods=['GET'])
def get_rule_names():
    rules = Rule.query.all()
    rule_names = [rule.name for rule in rules]
    return jsonify(rule_names)

@app.route('/get_rule_data', methods=['GET'])
def get_rule_data():
    rules = Rule.query.all()
    rule_data = [{"name": rule.name, "rule_string": rule.rule_string} for rule in rules]
    return jsonify(rule_data)

# Route to add a new rule
@app.route('/add_rule', methods=['POST'])
def create_rule():
    data = request.json
    rule_string = data.get('rule')
    
    if not rule_string:
        return jsonify({'error': 'Rule string is required'}), 400

    rule_name = f"Rule_{Rule.query.order_by(Rule.id.desc()).first().id + 1 if Rule.query.first() else 1}"
    try:
        ast_node = create_rules(rule_string)
        ast_representation = ast_node[1]  
        new_rule = Rule(name=rule_name, rule_string=ast_node[0],rule_tree=ast_node[1])
        db.session.add(new_rule)
        db.session.commit()
    except Exception as e:
        return jsonify({'error': f'Error creating AST: {str(e)}'}), 500

    return jsonify({
        'message': 'Rule added successfully',
        'rule': {
            'name': rule_name,
            'rule_string': rule_string,
            'ast': ast_representation
        }
    })

# Modify the evaluate endpoint to accept either rule string or rule name
@app.route('/evaluate_rule', methods=['POST'])
def evaluate():
    data = request.json
    rule_string = data.get('rule')
    rule_name = data.get('rule_name')
    eval_data = data.get('data')

    if rule_name:
        rule = Rule.query.filter_by(name=rule_name).first()
        if rule:
            rule_string = rule.rule_string
        else:
            return jsonify({'error': 'Rule name not found'}), 404

    if not rule_string or not eval_data:
        return jsonify({'error': 'Rule string/name and data are required'}), 400

    try:
        # Ensure eval_data is a valid dictionary
        if not isinstance(eval_data, dict):
            return jsonify({'error': 'Invalid data format, expected JSON object'}), 400

        ast = json.loads(create_rules(rule_string)[1])
        print(type(ast),ast)
        result = evaluate_rule(ast, eval_data)
    except Exception as e:
        return jsonify({'error': f'Error Evaluating rule: {str(e)}'}), 500
    
    return jsonify({'result': result})

# Modify rule endpoint to accept either rule string or rule name
@app.route('/modify_rule', methods=['PATCH'])
def modify_rule():
    data = request.json
    rule_string = data.get('rule')
    rule_name = data.get('rule_name')
    print(rule_name,rule_string)

    if rule_name:
        rule = Rule.query.filter_by(name=rule_name).first()
        if rule:
            if rule_string == rule.rule_string:
                return jsonify({'warning':'Change the rule string to modify','status':'NOT UPDATED'}), 404
            else:
                ast_tree = create_rules(rule_string)[1]
                print(ast_tree)
                Rule.query.filter(Rule.name == rule.name).update({"rule_string": rule_string,"rule_tree":ast_tree}, synchronize_session=False)
                db.session.commit()
                rule = Rule.query.filter_by(name=rule_name).first()
                result=rule.rule_string
        else:
            return jsonify({'error': 'Rule name not found'}), 404

    
    return jsonify({'result': result,'status':'UPDATED'})


#Delete a rule endpoint to delete the selected rules
@app.route('/delete_rule', methods=['DELETE'])
def delete():
    data = request.json
    rule_names = data.get('rules')
    print(rule_names)
    deleted_entries=[]

    if rule_names:
        for name in rule_names:
            rule = Rule.query.filter_by(name=name).first()
            if rule:
                deleted_entries.append(rule.name)
                Rule.query.filter(Rule.name == rule.name).delete(synchronize_session=False)
            else:
                return jsonify({'error': f'Rule name {name} not found'}), 404
        db.session.commit()
    result = deleted_entries
    
    return jsonify({'result': result,'status':"DELETED"})

@app.route('/combine_rule', methods=['POST'])
def combine_rule():
    data = request.json
    rule_strings = data.get('rules', [])
    rule_names = data.get('rule_names', [])

    combined_rule_strings = []

    if rule_strings and rule_strings[0] != '':
        combined_rule_strings = rule_strings

    if rule_names:
        for name in rule_names:
            rule = Rule.query.filter_by(name=name).first()
            if rule:
                combined_rule_strings.append(rule.rule_string)
            else:
                return jsonify({'error': f'Rule name {name} not found'}), 404

    if not combined_rule_strings:
        return jsonify({'error': 'No valid rules or rule names provided'}), 400

    try:
        # Assuming combine_rules is a function that processes the rules
        combined_ast = combine_rules(combined_rule_strings)
        
        rule_name = f"Rule_{len(Rule.query.all()) + 1}"  
        rule_string = combined_ast[0]
        ast_representation = combined_ast[1]  # Get string representation of the AST node
        new_rule = Rule(name=rule_name, rule_string=rule_string, rule_tree=ast_representation)
        db.session.add(new_rule)
        db.session.commit()
        
    except Exception as e:
        print(f'Error combining rules: {str(e)}')  # Debugging
        return jsonify({'error': f'Error combining rules: {str(e)}'}), 500

    return jsonify({
        'message': 'Rules combined successfully',
        'rule': {
            'name': rule_name,
            'rule_string': rule_string,
            'ast': ast_representation
        }
    })

    
@app.route('/get_rule_string', methods=['GET'])
def get_rule_string():
    rule_name = request.args.get('name')
    rule = Rule.query.filter_by(name=rule_name).first()
    if rule:
        return jsonify({'rule_string': rule.rule_string})
    return jsonify({'error': 'Rule not found'}), 404

# Route to serve index.html
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    app.run(debug=True)
