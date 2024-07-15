"""Flask app for Cupcakes"""
from flask import Flask, render_template, jsonify, request
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

with app.app_context():
    db.drop_all()
    db.create_all()

@app.route('/')
def home_page():
    """Displays home page"""
    with app.app_context():
        return render_template('home.html')

@app.route('/api/cupcakes')
def get_cupcakes():
    """Gets data about all cupcakes."""
    with app.app_context():
        #gets all cupcakes from db, iterates through them, serializes them, and puts them into list
        cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
        return jsonify(cupcakes=cupcakes)


@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake_data(cupcake_id):
    """Gets data about a single cupcake."""
    with app.app_context(): 
        cupcake = Cupcake.query.get_or_404(cupcake_id)
        return jsonify(cupcake.serialize())

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Creates a cupcake with flavor, size, rating and image data from the body of the request."""
    with app.app_context(): 
        #gets data 
        data = request.json
        #makes cupcake
        cupcake = Cupcake(flavor=data['flavor'], rating=data['rating'], size=data['size'], image=data['image'])
        #adds cupcake to db
        db.session.add(cupcake)
        db.session.commit()

        return (jsonify(cupcake=cupcake.serialize()), 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    with app.app_context():
        """Updates a cupcake with the id passed in the URL and flavor, size, rating and image data from the body of the request."""
        #Gets cupcake
        cupcake = Cupcake.query.get_or_404(cupcake_id)
        #Gets data
        data = request.json
        #updates cupcake
        cupcake.flavor = data['flavor']
        cupcake.rating = data['rating']
        cupcake.size = data['size']
        cupcake.image = data['image']

        db.session.add(cupcake)
        db.session.commit()

        return jsonify(cupcake=cupcake.serialize())
    
@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """Delete cupcake with the id passed in the URL"""
    #gets cupcake
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    #deletes cupcake
    db.session.delete(cupcake)
    db.session.commit()
    
    return jsonify(message='Deleted')



