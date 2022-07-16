from string import ascii_lowercase, ascii_uppercase
from typing import Any, List, Union
from json import loads
from flask import Flask, render_template, request, jsonify, abort
from flask.wrappers import Response


app = Flask(__name__)


def decode_value(value: str, language: str, key: Union[None, int], mode: str) -> dict:
    symbols_en: List[str] = list(ascii_uppercase + ascii_lowercase)
    symbols_ko: List[str] = [chr(i) for i in range(44032, 55204)]
    symbols: List[str] = symbols_en if language == 'en' else symbols_ko
    
    translated: str = ""
  
    if language == "undefined":
       abort(400)
        
    if key == "None":
        abort(400)
  
    for symbol in value:
        if symbol in symbols:
            symbol_index: int = symbols.index(symbol)
            translated_index: int = 0
          
            if mode == 'encrypt':
                translated_index = symbol_index + key
            else:
                translated_index = symbol_index - key
          
            if translated_index >= (length := len(symbols)):
                translated_index %= length
            elif translated_index < 0:
                while translated_index < 0:
                    translated_index += length
                  
            translated += symbols[translated_index]
        else:
            translated += symbol
            
    return {'value': translated}


@app.route('/decode', methods=['GET', 'POST'])
def decode() -> Union[Response, str]:
    if request.method == "POST":
        data: Any = request.get_json(force=True)

        if type(data) != str:
            pass
        else:
            data = loads(data)

        value = data["value"]
        language = data["language"]
        key = data["key"]
        mode = data["mode"]

        return jsonify(decode_value(value, language, key, mode))

    elif request.method == 'GET':
        return render_template("decode.html")


@app.route('/baskin-robbins')
def baskin_robbins() -> Union[Response, str]:
    return render_template("baskin_robbins.html")


@app.route('/', methods=['GET'])
def index() -> str:
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
