from typing import Dict, Union
import json
from pyodide import create_proxy
from pyodide.http import pyfetch
import asyncio
from js import document, alert, console

select = document.querySelector("select");
input_key = document.querySelector("#input");
button_encrypt = document.querySelector('#encrypt');
button_decrypt = document.querySelector("#decrypt");
first_text = document.querySelector(".inputTextarea");
second_text = document.querySelector(".result");

key: Union[None, int, str] = None


def get_body(mode: str):
    global key
    key = key if key is not None else "None"
    return json.dumps({"value": first_text.value,
                       "language": select.value,
                       "mode": mode,
                       "key": key})


async def make_request(url: str, method: str, mode: str, headers: Union[None, Dict[str, str]]=None):
    if not headers:
        headers = {"Content-Type": "application/json"}

    response = await pyfetch(
        url=url,
        method=method,
        headers=headers,
        body=get_body(mode=mode)
    )
    if response.ok:
        return await response.json()

    if response.status == 400:
        alert("언어와 키를 선택해 주세요.")


@create_proxy
async def encrypt_handler(event):
    data = await make_request(url='http://127.0.0.1:5000/decode', method='POST', mode='encrypt')
    if data is None:
        return
    second_text.value = data['value']


@create_proxy
async def decrypt_handler(event):
    data = await make_request(url='http://127.0.0.1:5000/decode', method='POST', mode='decrypt')
    if data is None:
        return
    second_text.value = data['value']


@create_proxy
def input_handler(_):
    global key
    if input_key.value == '':
        key = None
    else:
        key = int(input_key.value)


button_encrypt.addEventListener('click', encrypt_handler)
button_decrypt.addEventListener('click', decrypt_handler)
input_key.addEventListener('input', input_handler)
