from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Float, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favorite = relationship('Favorite', back_populates='user', lazy=True)

    def __repr__(self):
        return f"<User {self.user_name}>"

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "first_name": self.first_name,
            "last_name": self.last_name,            
            "email": self.email,
            "is_active": self.is_active,
           
            # do not serialize the password, its a security breach
        }
    def serialize_with_favorites(self):
        return {
            **self.serialize(),
             "favorites": [fav.serialize() for fav in self.favorite]
        }

class People(db.Model):
    __tablename__ = 'people'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    gender: Mapped[str] = mapped_column(String(60), nullable=False)
    skin_color: Mapped[str] = mapped_column(String(60), nullable=False)
    hair_color: Mapped[str] = mapped_column(String(60), nullable=False)
    height: Mapped[Float] = mapped_column(Float, nullable=False)    
    eye_color: Mapped[str] = mapped_column(String(60), nullable=False)
    mass: Mapped[Float] = mapped_column(Float, nullable=False)
    birth_year: Mapped[str] = mapped_column(String(60), nullable=False)
    favorite = relationship('Favorite', back_populates='people', lazy=True)

    # Representacion para saber como se va amostrar el objeto en consola
    def __repr__(self):
        return f"<People {self.name}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "skin_color": self.skin_color,
            "hair_color": self.hair_color,
            "height": self.height,
            "eye_color": self.eye_color,
            "mass": self.mass,
            "birth_year": self.birth_year,
        }

class Planet(db.Model):   
    __tablename__ = 'planets'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    climate: Mapped[str] = mapped_column(String(60), nullable=False)
    surface_water: Mapped[Float] = mapped_column(Float, nullable=False)
    diameter: Mapped[int] = mapped_column(Integer, nullable=False)
    rotation_period: Mapped[int] = mapped_column(Integer, nullable=False)
    terrain: Mapped[str] = mapped_column(String(60), nullable=False)
    gravity: Mapped[str] = mapped_column(String(60), nullable=False)
    orbital_period: Mapped[int] = mapped_column(Integer, nullable=False)
    population: Mapped[int] = mapped_column(Integer, nullable=False)   
    favorite = relationship('Favorite', back_populates='planet', lazy=True)
    
    def __repr__(self):
        return f"<Planet {self.name}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "surface_water": self.surface_water,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "terrain": self.terrain,
            "gravity": self.gravity,
            "orbital_period": self.orbital_period,
            "population": self.population,
        }

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    people_id: Mapped[int] = mapped_column(ForeignKey('people.id'), nullable=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planets.id'), nullable=True)
    user = relationship('User')   
    people = relationship('People')
    planet = relationship('Planet')

    def __repr__(self):
        return f"<Favorite {self.user_id} - {self.people_id} - {self.planet_id}>"

    def serialize(self):
        if not self.people:
            return {            
            "planet": self.planet.serialize() if self.planet else None
        }
        if not self.planet:
            return {            
            "people": self.people.serialize() if self.people else None
        }
