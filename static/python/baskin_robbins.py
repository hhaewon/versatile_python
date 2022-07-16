from typing import Optional, Literal
from random import randrange
from js import document, alert, console
from pyodide import create_proxy


select = document.querySelector('#select')
count_area = document.querySelector('#floatingTextarea2')
input_area = document.querySelector('#input')

count = 0
player: Optional[Literal[1, 2]] = None


def trim_brackets_space_comma(string: str) -> list[int]:
    string = string.replace('[', '')
    string = string.replace(']', '')
    string = string.replace(' ', '')
    string = string.split(',')
    string = map(int, list(string))
    return list(string)


def player_turn(event):
    global count
    if event.target.value == '':
        alert('숫자를 입력하세요')
        return

    input_numbers: list[int] = trim_brackets_space_comma(event.target.value)
    print(input_numbers)
    print(input_numbers[0])

    if len(input_numbers) < 0 or 3 < len(input_numbers):
        alert('1~3개의 숫자를 입력하세요')
        return

    for number in input_numbers:
        if not isinstance(number, int):
            alert('숫자를 다시 입력하세요')
            return

    if input_numbers[0] != (count + 1):
        alert('AI 말한 숫자의 바로 다음 숫자부터 입력하세요')
        return

    former_number = None
    for number in input_numbers:
        console.log(former_number)
        console.log(number)
        if former_number is None:
            former_number = number
            continue
        if former_number + 1 != number:
            alert('1 간격으로 숫자를 입력하세요')
            return
        former_number = number

    for number in input_numbers:
        count_area.value += f"player : {number}\n"
    count += len(input_numbers)


def ai_turn():
    global count
    ai: int = 0

    if count % 4 == 3:
        ai = 3
    elif count % 4 == 0:
        ai = 2
    elif count % 4 == 1:
        ai = 1
    else:
        ai = randrange(1, 4)

    for number in range(1, ai + 1):
        count_area.value += f"AI : {count + number}\n"
    count += ai


@create_proxy
def input_key_press_handler(event):
    global count
    console.log(event.keyCode)
    console.log(event.target.value)
    if event.keyCode == 13:
        if select.value == '':
            alert('먼저 시작할 플레이어를 먼저 선택하세요')
        player_turn(event)
        ai_turn(event)





@create_proxy
def select_change_handler(event):
    global player
    player = int(event.target.value)
    select.setAttribute('readonly', '')
    if select.value == '2':
        ai_turn()


select.addEventListener('change', select_change_handler)
input_area.addEventListener('keypress', input_key_press_handler)
