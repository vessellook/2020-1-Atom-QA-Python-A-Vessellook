from flask import Flask, jsonify, request

app = Flask(__name__)

vk_ids = {}
responses = {}


@app.route('/vk_id/<username>', methods=['GET'])
def vk_id_username(username):
    if username in responses:  # special response
        obj = responses[username]
        if 'json' in obj:
            return jsonify(obj['json']), obj['code']
        elif 'data' in obj:
            return obj['data'], obj['code']
    elif username in vk_ids:
        return jsonify({'vk_id': vk_ids[username]}), 200  # success
    else:
        return jsonify({}), 404  # error


@app.route('/mock/set_vk_id/<username>', methods=['PUT'])
def set_vk_id(username):
    global vk_ids
    if request.content_type == 'application/json':
        obj = request.get_json()
        if 'vk_id' in obj:
            vk_id = obj['vk_id']
            vk_ids[username] = vk_id
    return jsonify({'success': True}), 200


@app.route('/mock/unset_vk_id/<username>', methods=['DELETE'])
def unset_vk_id(username):
    global vk_ids
    try:
        vk_ids.pop(username)
    except KeyError:
        pass
    return jsonify({'success': True}), 200


@app.route('/mock/set_response/<username>', methods=['PUT'])
def set_response(username):
    global responses
    if request.content_type == 'application/json':
        obj = request.get_json()
        if 'code' in obj and ('json' in obj or 'data' in obj):
            responses[username] = obj
    return jsonify({'success': True}), 200


@app.route('/mock/unset_response/<username>', methods=['DELETE'])
def unset_response(username):
    global responses
    try:
        responses.pop(username)
    except KeyError:
        pass
    return jsonify({'success': True}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
