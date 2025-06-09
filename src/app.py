"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


# Get all People documentation
@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    if people is None:
        return jsonify('error People not found'), 404

    return jsonify([person.serialize() for person in people]), 200

# Get People by id

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_id(people_id):
    people = People.query.get(people_id)
    print(people)
    if people is None:
        return jsonify({"error": "People not found"}), 404
    return jsonify((people.serialize())), 200


# Get all Planets documentation
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    if planets is None:
        return jsonify('error Planets not found'), 404

    return jsonify([planet.serialize() for planet in planets]), 200

# Get Planet by id


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_id(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify((planet.serialize()), 200)


# Get All User
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    if users is None:
        return jsonify({"error": "Users not found"}), 404
    return jsonify([user.serialize() for user in users]), 200

# Get all Favorites

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_user_favorite(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify(user.serialize_with_favorites()), 200


# Post Favorite Planet by id

@app.route('/favorite/user/<int:user_id>/planet/<int:planet_id>', methods=['POST'])
def create_favorite_planet(user_id, planet_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    favorite = Favorite(user_id=user.id, planet_id=planet.id)
   

    db.session.add(favorite)
    db.session.commit()

    return jsonify({"message": "Favorite Planet created successfully"}), 200

# Post Favorite People by id
@app.route('/favorite/user/<int:user_id>/people/<int:people_id>', methods=['POST'])
def create_favorite_people(user_id, people_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    people = People.query.get(people_id)
    if people is None:
        return jsonify({"error": "People not found"}), 404
    favorite = Favorite(user_id=user.id, people_id=people.id)

    db.session.add(favorite)
    db.session.commit()

    return jsonify({"message": "Favorite People created successfully"}), 200
     

# Delete Planet Favorites by id
@app.route('/favorite/user/<int:user_id>/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet_favorite_id(user_id, planet_id):
    favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite is None:
        return jsonify({"error": "Favorite not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite deleted successfully"}), 200


 # Delete People Favorites by id
@app.route('/favorite/user/<int:user_id>/people/<int:people_id>', methods=['DELETE'])
def delete_people_favorite_id(user_id, people_id):
    favorite = Favorite.query.filter_by(user_id=user_id, people_id=people_id).first()
    if favorite is None:
        return jsonify({"error": "Favorite not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite People deleted successfully"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
