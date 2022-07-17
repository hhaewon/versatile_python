from typing import Optional, Literal
from random import randrange
from js import document, alert, console
from pyodide import create_proxy


select = document.querySelector('#select')
count_area = document.querySelector('#floatingTextarea2')
input_area = document.querySelector('#input')
count_element = document.querySelector('#count')
restart_button = document.querySelector('#restart')

count = 0
player: Optional[Literal[1, 2]] = None


def change_count(who: str):
    global count
    won_player: str = 'AI' if who == 'player' else 'player'
    if count > 30:
        count_element.innerText = 31
        alert(f'{won_player}가 이겼습니다.')
        input_area.removeEventListener('keypress', input_key_press_handler)
        return "end"
    else:
        count_element.innerText = count


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
        raise ValueError('숫자를 입력하세요')

    input_numbers: list[int] = trim_brackets_space_comma(event.target.value)

    if len(input_numbers) < 0 or 3 < len(input_numbers):
        raise ValueError('1~3개의 숫자를 입력하세요')

    for number in input_numbers:
        if not isinstance(number, int):
            raise ValueError('숫자를 다시 입력하세요')

    if input_numbers[0] != (count + 1):
        raise ValueError(f'{count + 1}부터 입력하세요')

    former_number = None
    for number in input_numbers:
        console.log(former_number)
        console.log(number)
        if former_number is None:
            former_number = number
            continue
        if former_number + 1 != number:
            raise ValueError('1 간격으로 숫자를 입력하세요')
        former_number = number

    for number in input_numbers:
        count_area.value += f"player : {number}\n"
    count += len(input_numbers)
    state = change_count('player')
    input_area.value = ''
    if state is not None:
        return state


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
    change_count('AI')


@create_proxy
def input_key_press_handler(event):
    global count
    if event.keyCode == 13:
        if select.value == 'undefined':
            alert('먼저 시작할 플레이어를 먼저 선택하세요')
            return
        try:
            state = player_turn(event)
            if state is not None:
                return
            ai_turn()
            auto_resize_textarea()
        except ValueError as e:
            message: str = str(e).replace('ValueError', '').replace('(', '').replace(')', '')
            if message == "invalid literal for int with base 10: ''":
                alert('쉼표를 하나씩 입력해주세요')
                return
            alert(message)


@create_proxy
def select_change_handler(event):
    global player
    player = int(event.target.value)
    for option in event.target.options:
        option.setAttribute('disabled', '')
    if select.value == '2':
        ai_turn()
        auto_resize_textarea()


def auto_resize_textarea():
    if count_area is not None:
        console.log("Hello")
        count_area.style.height = 'auto'
        height = count_area.scrollHeight
        count_area.style.height = f'{height + 8}px'


@create_proxy
def button_click_handler():
    global count
    count_area.value = ''
    for index, option in enumerate(select.options):
        if index == 0:
            pass
        else:
            option.removeAttribute('disabled')
    select.options.selectedIndex = 0
    count = 0
    count_element.innerText = count
    auto_resize_textarea()


select.addEventListener('change', select_change_handler)
input_area.addEventListener('keypress', input_key_press_handler)
restart_button.addEventListener('click', button_click_handler)
