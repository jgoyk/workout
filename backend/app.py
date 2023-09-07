from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/workoutflask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Workouts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text())
    date = db.Column(db.DateTime, default = datetime.datetime.now)


    def __init__(self, title, body):
        self.title = title
        self.body = body

class WorkoutSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'body', 'date')

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)



@app.route('/get', methods = ['GET'])
def get_workouts():
    all_workouts = Workouts.query.all()
    results = workouts_schema.dump(all_workouts)
    return jsonify(results)


@app.route('/get/<id>/', methods = ['GET'])
def workout_details(id):
    workout = Workouts.query.get(id)
    return workout_schema.jsonify(workout)




@app.route('/add', methods = ['POST'])
def add_workout():
    title = request.json['title']
    body = request.json['body']

    workouts = Workouts(title, body)
    db.session.add(workouts)
    db.session.commit()
    return workout_schema.jsonify(workouts)


@app.route('/update/<id>/', methods = ['PUT'])
def update_workout(id):
    workout = Workouts.query.get(id)

    title = request.json['title']
    body = request.json['body']

    workout.title = title
    workout.body = body

    db.session.commit()

    return workout_schema.jsonify(workout)

@app.route('/delete/<id>/', methods = ['DELETE'])
def delete_workout(id):
    workout = Workouts.query.get(id)

    db.session.delete(workout)
    db.session.commit()

    return workout_schema.jsonify(workout)



if __name__ == "__main__":
    app.run(debug=True)