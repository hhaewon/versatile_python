import string
import typing
from pyodide import create_proxy
import js

select = document.querySelector("select");
buttonEncrypt = document.getElementById('encrypt');
buttonDecrypt = document.querySelector("#decrypt");
input = document.querySelector("#input");
firstText = document.querySelector(".inputTextarea");
secondText = document.querySelector(".result");


selectvalue = None
key = None
SYMBOLS = ""
SYMBOLS_EN: typing.List[str] = list(string.ascii_uppercase + string.ascii_lowercase)
SYMBOLS_KO: typing.List[str] = [chr(i) for i in range(44032, 55204)]

@create_proxy
def changeHandler(event, mode: str):
    translated = ""
  
    if (select.value == '어떤 언어를 암호화 할지 선택하세요.'):                                  
        js.alert('암호화·복호화할 언어를 선택해주세요.')
        return
  
    if (key == None):
        js.alert('키 값을 입력해주세요.')
        return
  
    for symbol in firstText.value:
        if symbol in SYMBOLS:
            symbol_index = SYMBOLS.index(symbol)
            translated_index = 0
          
            if (mode == 'encrypt'):
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
            
    secondText.value = translated
            
   
@create_proxy           
def encryptHandler(event):
    changeHandler(event, "encrypt")
    
@create_proxy
def decryptHandler(event):
    changeHandler(event, "decrypt")   
    
buttonEncrypt.addEventListener('click', encryptHandler)
buttonDecrypt.addEventListener('click', decryptHandler)

@create_proxy
def selectHandler(event):
    global SYMBOLS
    select_value = tuple(event.target.options)[event.target.options.selectedIndex].value
    
    if select_value == 'en':
        SYMBOLS = SYMBOLS_EN
    elif select_value == 'ko':
        SYMBOLS = SYMBOLS_KO

select.addEventListener('change', selectHandler)

@create_proxy
def inputHandler(event):
    global key
    if input.value == '':
        key = None
    else:
        key = int(input.value)

input.addEventListener('input', inputHandler)