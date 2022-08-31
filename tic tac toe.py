import random


size = 10  # размер поля
count_lose = 5  # количество символов для поражения


def check_lose(smb, pc_available_step):
    """
    Проверяет кто является проигравшим

    :param smb: символ Х или О
    :param pc_available_step: список доступных ходов
    :return: сообщение о проигрыше, либо пустая строка
    """
    global count_lose
    for i in range(size):
        count = 0
        for j in range(size):
            count, lose_msg = check_counter(count, game_field[i][j], smb)
            if count == count_lose - 1:
                remove_cells(pc_available_step, i, j + 1)
                remove_cells(pc_available_step, i, j - count_lose - 1)
            if lose_msg:
                return lose_msg

    for i in range(size):
        count = 0
        for j in range(size):
            count, lose_msg = check_counter(count, game_field[j][i], smb)
            if count == count_lose - 1:
                remove_cells(pc_available_step, j + 1, i)
                remove_cells(pc_available_step, j - count_lose - 1, i)
            if lose_msg:
                return lose_msg

    for i in range(size):
        for j in range(size):
            count = 0
            a, b = i, j
            while a < size and b < size:
                count, lose_msg = check_counter(count, game_field[a][b], smb)
                if count == count_lose - 1:
                    remove_cells(pc_available_step, a + 1, b + 1)
                    remove_cells(pc_available_step, a - count_lose - 1, b - count_lose - 1)
                a += 1
                b += 1
                if lose_msg:
                    return lose_msg

    for i in range(size):
        for j in range(size):
            count = 0
            a, b = i, j
            while a < size and b >= 0:
                count, lose_msg = check_counter(count, game_field[a][b], smb)
                if count == count_lose - 1:
                    remove_cells(pc_available_step, a + 1, b - 1)
                    remove_cells(pc_available_step, a - count_lose - 1, b + count_lose - 1)
                a += 1
                b -= 1
                if lose_msg:
                    return lose_msg


def remove_cells(pc_available_step, i, j):
    """
    Удаляет координаты ячеек

    :param pc_available_step: список доступных ходов
    :param i: номер строки
    :param j: номер столбца
    """
    try:
        pc_available_step.remove((i, j))
    except ValueError:
        pass


def check_counter(count, cell, smb):
    """
    Считает количество подряд идущих одинаковых символов

    :param count: исходный счетчик
    :param cell: ячейка
    :param smb: символ Х или О
    :return: (счетчик, сообщение о проигрыше, либо пустая строка)
    """
    global count_lose
    if cell == smb:
        count += 1
    else:
        count = 0
    if count >= count_lose:
        return count_lose, 'Проиграл компьютер!' if smb == 'O ' else 'Ты проиграл!'
    return count, ''


def show_field(game_field):
    """
    Показывает поле игры
    :param game_field: игровое поле
    """
    for row in game_field:
        for cell in row:
            print(cell, end='')
        print()


# Главное тело функции, отвечает за ввод и раставление символов Х и О,  игроком и компьютером
pc_available_step = [(i, j) for j in range(size) for i in range(size)]
game_field = [['_ ' for j in range(size)] for i in range(size)]
flag = True  # флаг отсутствие проигравшего
while any(cell == '_ ' for row in game_field for cell in row) and flag:
    # ход игрока
    # проверяет правильность ввода координат
    while True:
        try:
            a_x, b_x = [int(i) for i in input(f'Введите координаты из 2 чисел (от 1 до {size}): \n').split()]
            if a_x > size or b_x > size or a_x < 1 or b_x < 1:
                raise ValueError
            if game_field[a_x - 1][b_x - 1] != '_ ':
                print('Эта клетка уже занята')
                continue
        except ValueError:
            print('Введено некорректное число')
        else:
            break
    game_field[a_x - 1][b_x - 1] = 'X '
    try:
        pc_available_step.remove((a_x - 1, b_x - 1))
    except ValueError:
        pass
    # определяет проигравшего
    if lose_msg_user := check_lose('X ', []):
        show_field(game_field)
        print(lose_msg_user)
        flag = False
        break
    # ход компьютера
    if not pc_available_step:
        show_field(game_field)
        flag = True
        break
    random.shuffle(pc_available_step)
    a_o, b_o = pc_available_step.pop()
    game_field[a_o][b_o] = 'O '
    show_field(game_field)
    # определяет проигравшего
    if lose_msg_pc := check_lose('O ', pc_available_step):
        print(lose_msg_pc)
        flag = False
        break
if flag:
    print('Победила дружба!!!')
