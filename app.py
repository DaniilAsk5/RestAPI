from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

@app.before_first_request
def create_tables_base():
    db.create_all()

@app.route('/')
def index():
    return "Welcome to the Items API! Use /items to get or create items."

@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([item.serialize() for item in items])

@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    print(data)  # Отладочная информация
       
    if data is None:
        return jsonify({'error': 'No input data provided'}), 400

    name = data.get('name')
    description = data.get('description')

    if not name or not description:
        return jsonify({'error': 'Name and description are required'}), 400

    new_item = Item(name=name, description=description)
    db.session.add(new_item)
    db.session.commit()

    return jsonify(new_item.serialize()), 201

@app.route('/items_page')
def items_page():
    return render_template('Site.html')

if __name__ == '__main__':
    app.run(debug=True)