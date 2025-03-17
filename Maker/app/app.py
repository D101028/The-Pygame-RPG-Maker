import json
import os

from flask import Flask, render_template, send_from_directory, send_file, request, jsonify
from PIL import Image
from urllib.parse import unquote

TILES_SETS_PATH = "tiles_sets\\tiles_sets.json"
TEMP_DIR = "temp"

app = Flask(__name__)

@app.route('/')
def test():
    return render_template('index.html')

@app.route('/js/<filename>')
def js(filename):
    return send_from_directory("js", filename)

@app.route('/css/<filename>')
def css(filename):
    return send_from_directory("css", filename)


@app.route('/get-image', methods=['GET'])
def get_image():
    image_path = request.args.get('image_path')
    image_path = unquote(image_path)
    if os.path.isfile(image_path):
        return send_file(image_path, mimetype='image/png')
    else:
        return "Image not found", 404

@app.route('/get-image-shape', methods=['GET'])
def get_image_shap():
    image_path = request.args.get('image_path')
    image_path = unquote(image_path)
    if os.path.isfile(image_path):
        img = Image.open(image_path)
        return jsonify({"width": img.width, "height": img.height})
    else:
        return "Image not found", 404

@app.route('/tiles/<filename>')
def tiles(filename):
    return send_from_directory("tiles", filename)

@app.route('/get-tiles-sets', methods=['GET'])
def load_tiles_sets():
    with open(TILES_SETS_PATH) as json_file:
        tiles_sets = json.load(json_file)

    return jsonify(tiles_sets)

if __name__ == "__main__":
    app.run(debug=True)
