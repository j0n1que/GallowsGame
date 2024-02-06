import tkinter.font
from tkinter import *
from pymorphy3 import *


""" Игра виселица."""
solved = 0


def RootGen():
    global root
    root = Tk()
    root.geometry("1280x1000")
    root.title('Виселица')
    root.resizable(width=False, height=False)


def FontParams() -> tkinter.font:
    starting_text_font = tkinter.font.Font(family='Segoe Script', size=28)
    additional_text_font = tkinter.font.Font(family='Segoe Script', size=18)
    extra_text_font = tkinter.font.Font(family='Segoe Script', size=21)
    return [starting_text_font, additional_text_font, extra_text_font]


def StartingButton():
    canvas.create_window(639, 500, anchor='center', window=starting_btn)


def RemoveStartingButton():
    starting_btn.destroy()


def StartingText():
    global starting_text, starting_ps
    starting_text = canvas.create_text(640, 0, text="Готовы сыграть?", anchor='n', font=FontParams()[0])
    starting_ps = canvas.create_text(640, 40, text='p.s. В эту игру надо играть вдвоем!', anchor='n',
                                     font=FontParams()[1])


def RemoveStartingText():
    canvas.delete(starting_text)
    canvas.delete(starting_ps)


def Solved():
    global solved, text_solved
    if solved == 1:
        text_solved = canvas.create_text(640, 80, text=f'Успешно спасен {solved} человек!', anchor='n',
                                         font=FontParams()[1])
    elif 2 <= solved <= 4:
        text_solved = canvas.create_text(640, 80, text=f'Успешно спасено {solved} человека!', anchor='n',
                                         font=FontParams()[1])
    else:
        text_solved = canvas.create_text(640, 80, text=f'Успешно спасено {solved} человек!', anchor='n',
                                         font=FontParams()[1])


def FuncOfStartingButton():
    RemoveStartingButton()
    RemoveStartingText()
    RemoveSolved()
    Alphabet()
    UserRequest()
    root.bind('<Key>', FirstKeyPress)


def Alphabet():
    global alphabet, alph_text
    alphabet = ' А Б В Г Д Е Ё Ж З И Й К Л М Н\nО П Р С Т У Ф Х Ц Ч Ш Щ Ъ Ы\nЬ Э Ю Я '
    alph_text = canvas.create_text(640, 800, text=alphabet, anchor='center', justify='center', font=FontParams()[0])


def UserRequest():
    global riddle_request, enter_hint
    riddle_request = canvas.create_text(640, 0, text="Введи слово, которое хочешь загадать",
                                        anchor='n', font=FontParams()[0])
    enter_hint = canvas.create_text(640, 40, text='(После ввода нажми Enter)', anchor='n', font=FontParams()[1])


def FirstKeyPress(event):
    global riddle, riddle_text, inputing_text, first_input
    if first_input:
        if event.keysym != 'Return':
            if event.keysym == 'BackSpace':
                try:
                    inputing_text = inputing_text[:len(inputing_text) - 1]
                    canvas.delete(riddle_text)
                    riddle_text = canvas.create_text(640, 360, text=inputing_text, anchor='center',
                                                     font=FontParams()[0])
                except NameError:
                    pass
            else:
                inputing_text += event.char
                try:
                    canvas.delete(riddle_text)
                    riddle_text = canvas.create_text(640, 360, text=inputing_text, anchor='center',
                                                     font=FontParams()[0])
                except NameError:
                    riddle_text = canvas.create_text(640, 360, text=inputing_text, anchor='center',
                                                     font=FontParams()[0])
        else:
            if len(inputing_text) > 0 and WordCheck() and ' ' not in inputing_text:
                riddle = inputing_text.upper()
                HintRequest()
                inputing_text = ''
                first_input = False
            else:
                InputError()
                inputing_text = ''


def WordCheck() -> bool:
    threshold = 0.6
    morph = MorphAnalyzer()
    p = morph.parse(inputing_text)
    score = p[0].score
    if score >= threshold:
        return True
    else:
        return False


def InputError():
    RemoveRiddle()
    RemoveSolved()
    try:
        ErrorRemove()
    except NameError:
        pass
    NoRecognition()
    RemoveRequest()


def NoRecognition():
    global error_msg
    no_rec = f'Не могу распознать слово {inputing_text}, возможно оно выдумано!\n Пожалуйста, придумай другое!'
    error_msg = canvas.create_text(640, 0, justify='center', text=no_rec, anchor='n', font=FontParams()[1])


def ErrorRemove():
    canvas.delete(error_msg)


def HintRequest():
    RemoveRiddle()
    RemoveRequest()
    try:
        ErrorRemove()
    except NameError:
        pass
    YourWord()
    AskingForHint()
    root.unbind('<Key>')
    root.bind('<Key>', SecondKeyPress)


def RemoveRiddle():
    canvas.delete(riddle_text)


def RemoveSolved():
    canvas.delete(text_solved)


def RemoveRequest():
    canvas.delete(riddle_request)
    canvas.delete(enter_hint)


def YourWord():
    global your_word
    your_word = canvas.create_text(640, 0, text=f'Твое слово - {inputing_text}!', anchor='n', font=FontParams()[0])


def AskingForHint():
    global ask
    msg = 'Теперь введи одно слово - подсказку для отгадывающего'
    ask = canvas.create_text(640, 40, text=f'{msg}', anchor='n', font=FontParams()[0])


def SecondKeyPress(event):
    global hint, second_input, hint_text, inputing_text
    if second_input:
        if event.keysym != 'Return':
            if event.keysym == 'BackSpace':
                try:
                    inputing_text = inputing_text[:len(inputing_text) - 1]
                    canvas.delete(hint_text)
                    hint_text = canvas.create_text(640, 360, text=inputing_text, anchor='center', font=FontParams()[0])
                except NameError:
                    pass
            else:
                inputing_text += event.char
                try:
                    canvas.delete(hint_text)
                    hint_text = canvas.create_text(640, 360, text=inputing_text, anchor='center', font=FontParams()[0])
                except NameError:
                    hint_text = canvas.create_text(640, 360, text=inputing_text, anchor='center', font=FontParams()[0])
        else:
            if len(inputing_text) > 0 and WordCheck() and ' ' not in inputing_text:
                hint = inputing_text
                SecondPart()
                inputing_text = ''
                second_input = False
            else:
                HintInputError()
                inputing_text = ''


def HintInputError():
    RemoveHint()
    RemoveWord()
    RemoveAsk()
    try:
        ErrorRemove()
    except NameError:
        pass
    NoRecognition()


def RemoveHint():
    canvas.delete(hint_text)


def RemoveWord():
    canvas.delete(your_word)


def RemoveAsk():
    canvas.delete(ask)


def SecondPart():
    RemoveHint()
    try:
        RemoveAsk()
    except NameError:
        pass
    try:
        ErrorRemove()
    except NameError:
        pass
    try:
        RemoveWord()
    except NameError:
        pass
    InspiringMessage()
    ShowHint()
    ShowUnderscores()
    root.unbind('<Key>')
    root.bind('<Key>', ThirdKeyPress)


def ShowHint():
    global show_hint_text
    show_hint_text = canvas.create_text(640, 40, text=f'Подсказка - {hint}', anchor='n', font=FontParams()[0])


def ShowUnderscores():
    global underscores
    underscores = canvas.create_text(640, 200, text=' _ ' * len(riddle), anchor='center', font=FontParams()[0])


def InspiringMessage():
    global inspiration
    msg = 'Отгадай слово за 6 попыток, чтобы спасти самоубийцу!'
    inspiration = canvas.create_text(640, 0, text=msg, anchor='n', font=FontParams()[0])


def ThirdKeyPress(event):
    global inputing_char, word, mistakes_counter, pressed, solved, game_run
    inputing_char = event.char
    local_alphabet = 'абвгдеёжзийклмнопрстуфхцчшщьыъэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    if event.keysym in ['BackSpace', 'Return'] or inputing_char not in local_alphabet or inputing_char in pressed:
        pass
    else:
        pressed.append(inputing_char)
        if inputing_char.upper() in riddle:
            word += riddle.count(inputing_char.upper()) * inputing_char
            RemoveAlph()
            PlaceAlph()
            PlaceChar()
            if len(word) == len(riddle):
                solved += 1
                GameWin()
        else:
            RemoveAlph()
            PlaceAlph()
            mistakes_counter += 1
            if mistakes_counter == 1:
                DrawGallowsBase()
            elif mistakes_counter == 2:
                DrawHeadBody()
            elif mistakes_counter == 3:
                DrawLeftHand()
            elif mistakes_counter == 4:
                DrawRightHand()
            elif mistakes_counter == 5:
                DrawLeftLeg()
            else:
                DrawRightLeg()
                GameLose()


def RemoveAlph():
    try:
        canvas.delete(alph_text)
    except NameError:
        pass
    try:
        canvas.delete(input_alph_text)
    except NameError:
        pass


def PlaceAlph():
    global input_alph_text, alph_flag, local_alphabet
    if alph_flag:
        local_alphabet = alphabet
        alph_flag = False
        char_index = local_alphabet.index(inputing_char.upper())
        local_alphabet = local_alphabet[:char_index] + ' ' + local_alphabet[char_index + 1:]
        input_alph_text = canvas.create_text(640, 800, text=local_alphabet, anchor='center', justify='center',
                                             font=FontParams()[0])
    else:
        char_index = local_alphabet.index(inputing_char.upper())
        local_alphabet = local_alphabet[:char_index] + ' ' + local_alphabet[char_index + 1:]
        input_alph_text = canvas.create_text(640, 800, text=local_alphabet, anchor='center', justify='center',
                                             font=FontParams()[0])


def PlaceChar():
    global showing_word_text, showing_word_flag, showing_word
    try:
        canvas.delete(showing_word_text)
    except NameError:
        pass
    if showing_word_flag:
        showing_word = '   ' * len(riddle)
        showing_word_flag = False
        for i in range(len(riddle)):
            if riddle[i] == inputing_char.upper():
                showing_word = showing_word[:i * 3 + 1] + riddle[i] + showing_word[i * 3 + 2:]
        showing_word_text = canvas.create_text(640, 200, text=showing_word, anchor='center', justify='center',
                                               font=FontParams()[2])
    else:
        for i in range(len(riddle)):
            if riddle[i] == inputing_char.upper():
                showing_word = showing_word[:i * 3 + 1] + riddle[i] + showing_word[i * 3 + 2:]
        showing_word_text = canvas.create_text(640, 200, text=showing_word, anchor='center', justify='center',
                                               font=FontParams()[2])


def DrawGallowsBase():
    global b1, b2, b3, b4
    b1 = canvas.create_line(540, 700, 740, 700, width=3)
    b2 = canvas.create_line(640, 700, 640, 260, width=3)
    b3 = canvas.create_line(640, 260, 450, 260, width=3)
    b4 = canvas.create_line(450, 260, 450, 350, width=1)


def DrawHeadBody():
    canvas.create_oval(420, 350, 480, 410, width=3)
    canvas.create_oval(435, 367, 440, 372, fill='Black', width=3)
    canvas.create_oval(460, 367, 465, 372, fill='Black', width=3)
    canvas.create_line(435, 390, 465, 390, width=2)
    canvas.create_line(450, 410, 450, 540, width=3)


def DrawLeftHand():
    canvas.create_line(450, 430, 410, 470, width=3)


def DrawRightHand():
    canvas.create_line(450, 430, 490, 470, width=3)


def DrawLeftLeg():
    canvas.create_line(450, 540, 410, 580, width=3)


def DrawRightLeg():
    canvas.create_line(450, 540, 490, 580, width=3)


def GameWin():
    root.unbind('<Key>')
    RemoveAlph()
    RemoveInspiration()
    RemoveUnderscores()
    RemoveShowingWord()
    RemoveShowHint()
    DrawHeadBody()
    DrawLeftHand()
    DrawRightHand()
    DrawLeftLeg()
    DrawRightLeg()
    try:
        RemoveGallows()
    except NameError:
        pass
    DrawHouse()
    Congratulations()
    IWant()
    IDontWant()


def RemoveGallows():
    canvas.delete(b1)
    canvas.delete(b2)
    canvas.delete(b3)
    canvas.delete(b4)


def RemoveInspiration():
    canvas.delete(inspiration)


def RemoveUnderscores():
    canvas.delete(underscores)


def RemoveShowingWord():
    canvas.delete(showing_word_text)


def RemoveShowHint():
    canvas.delete(show_hint_text)


def Congratulations():
    canvas.create_text(640, 0, text='Тебе удалось спасти его!', anchor='n', font=FontParams()[0])
    canvas.create_text(640, 40, text='Хотите сыграть еще раз?', anchor='n', font=FontParams()[0])


def DrawHouse():
    canvas.create_rectangle(700, 580, 1100, 300, width=5)
    canvas.create_rectangle(750, 580, 850, 340, width=5)
    canvas.create_line(700, 300, 900, 120, width=5)
    canvas.create_line(1100, 300, 900, 120, width=5)
    canvas.create_rectangle(920, 480, 1020, 380, width=5)
    canvas.create_line(920, 430, 1020, 430, width=5)
    canvas.create_line(970, 480, 970, 380, width=5)


def IWant():
    canvas.create_window(650, 120, window=i_want_btn)


def IDontWant():
    canvas.create_window(639, 760, window=i_dont_want_btn)


def IWantBtn():
    root.destroy()
    GameWindow()


def IDontWantBtn():
    root.destroy()


def GameLose():
    root.unbind('<Key>')
    RemoveShowHint()
    try:
        RemoveShowingWord()
    except NameError:
        pass
    RemoveUnderscores()
    RemoveInspiration()
    RemoveAlph()
    LoseMessage()
    IWant()
    IDontWant()


def LoseMessage():
    canvas.create_text(640, 0, text='Ты не смог спасти его!', anchor='n', font=FontParams()[0])
    canvas.create_text(640, 40, text='Хотите сыграть еще раз?', anchor='n', font=FontParams()[0])


def GameWindow():
    global canvas, starting_btn, i_want_btn, i_dont_want_btn, first_input, second_input, alph_flag, showing_word_flag
    global inputing_text, hint, riddle, word, mistakes_counter, pressed
    first_input = second_input = alph_flag = showing_word_flag = True
    inputing_text = hint = riddle = word = ''
    mistakes_counter = 0
    pressed = []
    RootGen()
    icon = PhotoImage(file='GallowsGame.png')
    root.iconphoto(False, icon)
    canvas = Canvas(root, width=1280, height=1000)
    canvas.pack()
    background = PhotoImage(file='background.png')
    canvas.create_image(0, 0, anchor="nw", image=background)
    StartingText()
    starting_image = PhotoImage(file="starting_button.png")
    starting_btn = Button(image=starting_image, command=FuncOfStartingButton)
    i_want_image = PhotoImage(file='i_want.png')
    i_want_btn = Button(image=i_want_image, command=IWantBtn)
    i_dont_want_image = PhotoImage(file='i_dont_want.png')
    i_dont_want_btn = Button(image=i_dont_want_image, command=IDontWantBtn)
    StartingButton()
    Solved()
    root.mainloop()


GameWindow()
