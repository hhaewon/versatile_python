from string import ascii_lowercase, ascii_uppercase
from typing import Any, List, Literal, Union
import json
from flask import Flask, render_template, request, jsonify, abort
from flask.wrappers import Response

app = Flask(__name__)


def decode_value(value: str, language: str, key: Union[None, int], mode: str):
    SYMBOLS_EN: List[str] = list(ascii_uppercase + ascii_lowercase)
    SYMBOLS_KO: List[str] = [chr(i) for i in range(44032, 55204)]
    SYMBOLS: List[str] = SYMBOLS_EN if language == 'en' else SYMBOLS_KO
    
    translated: str = ""
  
    if language == "undefined":
       abort(400)
        
    if key == "None":
        abort(400)
  
    for symbol in value:
        if symbol in SYMBOLS:
            symbol_index: int = SYMBOLS.index(symbol)
            translated_index: int = 0
          
            if mode == 'encrypt':
                translated_index = symbol_index + key
            else:
                translated_index = symbol_index - key
          
            if translated_index >= (length := len(SYMBOLS)):
                translated_index %= length
            elif translated_index < 0:
                while translated_index < 0:
                    translated_index += length
                  
            translated += SYMBOLS[translated_index]
        else:
            translated += symbol
            
    return {'value': translated}


@app.route('/decode', methods=['GET', 'POST'])
def decode():
    if request.method == "POST":
        data: Any = request.get_json(force=True)

        if type(data) != str:
            pass
        else:
            data = json.loads(data)

        value = data["value"]
        language = data["language"]
        key = data["key"]
        mode = data["mode"]

        return jsonify(decode_value(value, language, key, mode))

    elif request.method == 'GET':
        return render_template("decode.html")


@app.route('/', methods=['GET'])
def index() -> str:
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
