"""Flask app for Cupcakes"""
from flask import Flask,jsonify, flash, redirect, render_template, request
from models import db, connect_db, Cupcake
# from forms import FormName


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

db.create_all()

@app.get('/api/cupcakes')
def list_all_cupcakes():
    """return JSON {"cupcakes": [{id, flavor, size, rating, image}, ...]}"""
    cupcakes= Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]
    return jsonify(cupcakes=serialized)

@app.get('/api/cupcakes/<int:cupcake_id>')
def list_single_cupcake(cupcake_id):
    """return JSON {"cupcake": {id, flavor, size, rating, image}}"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()
    return jsonify(cupcake=serialized)