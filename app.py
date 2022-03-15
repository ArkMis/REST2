from flask import Flask, jsonify, abort, make_response
from flask import request
from models import discs

app = Flask(__name__)
app.config["SECRET_KEY"] = "minihifi"


@app.route("/api/v1/discs/", methods=["GET"])
def discs_list_api_v1():
    return jsonify(discs.all())

@app.route("/api/v1/discs/<int:disc_id>", methods=["GET"])
def get_disc(disc_id):
    disc = discs.get(disc_id)
    if not disc:
        abort(404)
    return jsonify({"disc": disc})

@app.route("/api/v1/discs/", methods=["POST"])
def create_disc():
    if not request.json or not 'title' in request.json:
        abort(400)
    disc = {
        'id': discs.all()[-1]['id'] + 1,
        'title': request.json['title'],
        'year': request.json.get('year', ""),
        'band': request.json['band']
    }
    discs.create(disc)
    return jsonify({'disc': disc}), 201

@app.route("/api/v1/discs/<int:disc_id>", methods=['DELETE'])
def delete_disc(disc_id):
    result = discs.delete(disc_id)
    if not result:
        abort(404)
    return jsonify({'result': result})

@app.route("/api/v1/discs/<int:disc_id>", methods=["PUT"])
def update_disc(disc_id):
    disc = discs.get(disc_id)
    if not disc:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    print('data=request.json')
    print(data)
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'year' in data and not isinstance(data.get('year'), str),
        'band' in data and not isinstance(data.get('band'), str)
    ]):
        abort(400)
    print('disc 1:')
    print(disc)
    disc = {
        'id': data.get('id', disc['id']),
        'title': data.get('title', disc['title']),
        'year': data.get('year', disc['year']),
        'band': data.get('band', disc['band'])
    }
    print('disc 2:')
    print(disc)
    discs.update(disc_id, disc)
    return jsonify({'disc': disc})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)

if __name__ == "__main__":
    app.run(debug=True)
