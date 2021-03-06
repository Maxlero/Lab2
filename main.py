"""
    Автор: Орел Максим
    Группа: КБ-161
    Вариант: 11
    Дата создания: 25/02/2018
    Python Version: 3.6
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.misc import derivative

# Constants
accuracy = 0.00001
iterations = 0
a = -0.5
b = 0


def draw(function_f, x1, x2, y1, y2, x_left, x_right):
    x = np.arange(x_left, x_right, 0.01)

    plt.plot(x, function_f(x))
    plt.axis([x1, x2, y1, y2])
    plt.grid(True)
    plt.axhline(y=0, color='k')
    plt.axvline(x=0, color='k')
    plt.show()


def f(x):
    return x - np.log(x - 1 + ((x - 1) ** 2 + 1) ** 0.5)


def diff_f(point):
    return derivative(f, point, dx=1e-5)


def diff_2_f(point):
    return derivative(f, point, dx=1e-5, n=2)


def enter_values():
    while True:
        try:
            a = float(input("Введите левый промежуток: "))
            b = float(input("Введите правый промежуток: "))

            # Сделаем проверку, если ли корень на промежутке
            if f(a) * f(b) < 0:
                print("Кажется на промежутке [" + str(a) + ", " + str(b) + "] есть один или несколько корней.")
                break
            else:
                print("Кажется на введенном промежутке нет корня. Попробуйте еще раз..")

        except ValueError:
            print("Кажется с промежутком что-то не так. Попробуйте другой..")

    return a, b


def chords_method(left, right, motionless):
    global iterations
    global accuracy

    if motionless:
        b = right
        x0 = left
        if f(x0) != 0 and abs(f(x0)) > accuracy:
            iterations += 1
            a = x0 - f(x0) / (f(b) - f(x0)) * (b - x0)
            chords_method(a, b, 1)
        else:
            print("Корень: " + str("%.9f" % x0))
            print("Количество итераций: " + str(iterations))
            print("Проверка: f(x) = " + str("%.2e" % f(x0)) +
                  " <= " + str(accuracy))
    else:
        a = left
        x0 = right
        if f(x0) != 0 and abs(f(x0)) > accuracy:
            iterations += 1
            b = a - f(a) / (f(x0) - f(a)) * (x0 - a)
            chords_method(a, b, 0)
        else:
            print("Корень: " + str("%.9f" % x0))
            print("Количество итераций: " + str(iterations))
            print("Проверка: f(x) = " + str("%.2e" % f(x0)) +
                  " <= " + str(accuracy))


def max_diff(a, b):
    step = 0.01  # шаг
    max_value = 0  # максимальное значение
    array = np.arange(a, b + step, step)
    for i in array:
        if abs(diff_f(i)) > abs(max_value):
            max_value = diff_f(i)
    return max_value


def g(x, l):
    return x - l * f(x)


def aitken_method(x0, l):
    global iterations
    global accuracy

    if f(x0) != 0 and abs(f(x0)) > accuracy:
        iterations += 1
        x1 = g(x0, l)
        x2 = g(x1, l)
        x2s = (x0 * x2 - x1 ** 2) / (x2 - 2 * x1 + x0)
        x3 = g(x2s, l)
        if f(x3) != 0 and abs(f(x3)) > accuracy:
            aitken_method(x2s, l)
        else:
            print("Корень: " + str("%.9f" % x3))
            print("Количество итераций: " + str(iterations))
            print("Проверка: f(x) = " + str("%.2e" % f(x3)) +
                  " <= " + str(accuracy))
    else:
        print("Корень: " + str("%.9f" % x0))
        print("Количество итераций: " + str(iterations))
        print("Проверка: f(x) = " + str("%.2e" % f(x0)) +
              " <= " + str(accuracy))


def steffensen_method(x0):
    global iterations
    global accuracy

    if f(x0) != 0 and abs(f(x0)) > accuracy:
        iterations += 1
        x1 = x0 - ((f(x0)) ** 2) / (f(x0) - f(x0 - f(x0)))
        steffensen_method(x1)
    else:
        print("Корень: " + str("%.9f" % x0))
        print("Количество итераций: " + str(iterations))
        print("Проверка: f(x) = " + str("%.2e" % f(x0)) +
              " <= " + str(accuracy))


if __name__ == "__main__":
    # TODO rename files
    ####################################################################################################################
    print("___________________________________________________________________________________________________________")
    print("Подготовительные действия:")
    ####################################################################################################################

    # нарисуем функцию
    draw(f, -10, 10, -10, 10, -10, 10)

    # введем промежуток
    a, b = enter_values()
    # a, b = -0.5, 0

    # за начальное приближение возьмем середину отрезка
    x0 = (a + b) / 2

    ####################################################################################################################
    print("___________________________________________________________________________________________________________")
    print("Метод хорд:")
    ####################################################################################################################
    try:
        # нарисуем 2-ю производную на [a, b]
        draw(diff_2_f, a, b, f(a), f(b), a, b)

        iterations = 0
        if diff_2_f(x0) < 0:
            # точка а неподвижная
            chords_method(a, b, 0)
        else:
            # точка b неподвижная
            chords_method(a, b, 1)
    except:
        print("Что-то пошло не так.. Возможно, на промежутке несколько корней.")
    ####################################################################################################################
    print("___________________________________________________________________________________________________________")
    print("Метод Эйткена:")
    ####################################################################################################################
    try:
        # нарисуем 1-ю производную на [a, b]
        draw(diff_f, a, b, f(a), f(b), a, b)

        # найдем l = 1 / M = 1 / max|f'(x)| on [a, b]
        l = 1 / max_diff(a, b)

        iterations = 0
        aitken_method(x0, l)
    except:
        print("Что-то пошло не так.. Возможно, на промежутке несколько корней.")
    ####################################################################################################################
    print("___________________________________________________________________________________________________________")
    print("Метод Стеффенсона:")
    ####################################################################################################################
    try:
        # этот метод - комбинация 2-х предыдущих методов
        iterations = 0
        steffensen_method(x0)
    except:
        print("Что-то пошло не так.. Возможно, на промежутке несколько корней.")
