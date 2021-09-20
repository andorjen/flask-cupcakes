"""Flask app for Cupcakes"""
from flask import Flask, jsonify, flash, redirect, render_template, request
from models import db, connect_db, Cupcake
# from forms import FormName

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

db.create_all()


@app.get('/')
def show_home_page():
    """return html of home page with form and cupcake list space"""
    return render_template("cupcakes.html")


#############################################################################
# API ROUTES
@app.get('/api/cupcakes')
def list_all_cupcakes():
    """return JSON {"cupcakes": [{id, flavor, size, rating, image}, ...]}"""

    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]
    return jsonify(cupcakes=serialized)


@app.get('/api/cupcakes/<int:cupcake_id>')
def list_single_cupcake(cupcake_id):
    """return JSON {"cupcake": {id, flavor, size, rating, image}}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()
    return jsonify(cupcake=serialized)


@app.post('/api/cupcakes')
def create_a_cupcake():
    """add cupcake and return JSON {"cupcake": {id, flavor, size, rating, image}}"""

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"] or None

    # data = {k: (v if v else None) for k, v in request.json.items()}
    # loop through ["flavor", "size", "rating", "image"] -- safer approach
    Cupcake(**request.json)

    cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(cupcake)
    db.session.commit()

    serialized = cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)


@app.patch('/api/cupcakes/<int:cupcake_id>')
def update_cupcake_data(cupcake_id):
    """edit cupcake details and return JSON {"cupcake": {id, flavor, size, rating, image}}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    # is there a more efficient way with loops to do?
    # setattr(cupcake, "flavor", request.json['flavor'])

    if 'flavor' in request.json:
        cupcake.flavor = request.json['flavor']
    if 'size' in request.json:
        cupcake.size = request.json['size']
    if 'rating' in request.json:
        cupcake.rating = request.json['rating']
    if 'image' in request.json:
        cupcake.image = request.json['image']

    serialized = cupcake.serialize()

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=serialized)


@app.delete('/api/cupcakes/<int:cupcake_id>')
def delete_cupcake(cupcake_id):
    """delete a cupcake with given id, return {deleted: cupcake_id} """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return {"deleted": cupcake_id}
