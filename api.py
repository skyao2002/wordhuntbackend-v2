from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import cv2
import numpy
import pytesseract
import re
from solver import loadDict
from solver import solveWordHunt

app = Flask(__name__)
cors = CORS(app)
# cors = CORS(app, resources={r"/*": {"origins" : }})
# app.config['CORS_HEADERS'] = 'Content-Type'
trie = loadDict()
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


@app.route('/')
def hello():
    return "Welcome to the wordhunt solver's api"

@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json(force=True)
    solution = solveWordHunt(data["letters"], data["size"], trie)

    response = jsonify({"answer": solution.ansNoDuplicates})

    # Enable Access-Control-Allow-Origin
    # response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/solveimg', methods=['POST'])
def solveimg():
    fileParam = request.files['file']
    img = cv2.imdecode(numpy.fromstring(fileParam.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)

    # convert img to rgb since opencv is normally in bcr
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.threshold(img, 60, 255, cv2.THRESH_BINARY)[1]

    letters = pytesseract.image_to_string(img, config="-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    letters = re.sub(r'\W+', '', letters)

    print(letters)
    if len(letters) < 16:
        letters += "A" * (16 - len(letters))

    solution = solveWordHunt(letters, 4, trie)

    response = jsonify({"letters": letters, "answer": solution.ansNoDuplicates})
    
    # Enable Access-Control-Allow-Origin
    # response.headers.add("Access-Control-Allow-Origin", "*")
    return response

