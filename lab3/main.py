import time
import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use("TkAgg")


def draw_pixel(graph, x, y, color):
    graph.fill([x, x, x + 1, x + 1], [y, y + 1, y + 1, y], color=color)

def draw_coordinate_axes(graph, x_max, y_max):
    graph.plot([0, 0], [0, y_max], color='black')  # y-axis
    graph.plot([0, x_max], [0, 0], color='black')  # x-axis
    graph.text(-0.5, y_max + 5, 'y', fontsize=10, ha='center')
    graph.text(x_max + 5, -0.5, 'x', fontsize=10, ha='center')


def dda_algorithm(graph, x1, y1, x2, y2, color):
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))

    if dx == 0 and dy == 0:
        draw_pixel(graph, x1, y1, color)
        return

    x_increment = dx / steps
    y_increment = dy / steps

    x = x1
    y = y1

    for _ in range(steps):
        draw_pixel(graph, round(x), round(y), color)
        x += x_increment
        y += y_increment


def bresenham_algorithm(graph, x1, y1, x2, y2, color):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = -1 if x1 > x2 else 1
    sy = -1 if y1 > y2 else 1

    if dx > dy:
        err = dx / 2.0
        while x1 < x2 - 1:
            draw_pixel(graph, x1, y1, color)
            err -= dy
            if err < 0:
                y1 += sy
                err += dx
            x1 += sx
    else:
        err = dy / 2.0
        while y1 < y2 - 1:
            draw_pixel(graph, x1, y1, color)
            err -= dx
            if err < 0:
                x1 += sx
                err += dy
            y1 += sy


def castle_pitway_algorithm(graph, x1, y1, x2, y2, color):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    steep = dy > dx

    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    error = dx // 2
    ystep = 1 if y1 < y2 else -1
    y = y1

    for x in range(x1, x2):
        if steep:
            draw_pixel(graph, y, x, color)
        else:
            draw_pixel(graph, x, y, color)

        error -= dy
        if error < 0:
            y += ystep
            error += dx


def interpolate_color(color1, color2, factor):
    r1, g1, b1 = color1
    r2, g2, b2 = color2

    r = int(r1 + (r2 - r1) * factor)
    g = int(g1 + (g2 - g1) * factor)
    b = int(b1 + (b2 - b1) * factor)

    return r, g, b


if __name__ == "__main__":
    x1dda, y1dda, x2dda, y2dda = map(int, input("Введите x1, y1, x2, y2 для алгоритма DDA\n").strip().split())
    x1br, y1br, x2br, y2br = map(int, input("Введите x1, y1, x2, y2 для алгоритма Брезенхема\n").strip().split())
    x1kp, y1kp, x2kp, y2kp = map(int, input("Введите x1, y1, x2, y2 для алгоритма Кастла-Питвея\n").strip().split())

    # Создаем графический интерфейс с использованием библиотеки Tkinter
    root = tk.Tk()
    fig = plt.figure()
    graph = fig.add_subplot(111)
    x_max = max(x1dda, x2dda, x1kp, x2kp, x1br, x2br) * 1.05
    y_max = max(y1dda, y2dda, y1kp, y2kp, y1br, y2br) * 1.05
    plt.ylim(0, y_max)
    plt.xlim(0, x_max)
    graph.grid()
    draw_coordinate_axes(graph, x_max, y_max)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()
    canvas.draw()


    start_time = time.time()
    # Здесь вызывается алгоритм DDA
    dda_algorithm(graph, x1dda, y1dda, x2dda, y2dda, "red")
    end_time = time.time()
    execution_time_dda = end_time - start_time

    start_time = time.time()
    # Здесь вызывается алгоритм Брезенхема
    bresenham_algorithm(graph, x1br, y1br, x2br, y2br, "blue")
    end_time = time.time()
    execution_time_bresenham = end_time - start_time

    start_time = time.time()
    # Здесь вызывается алгоритм Кастла-Питвея
    castle_pitway_algorithm(graph, x1kp, y1kp, x2kp, y2kp, "green")
    end_time = time.time()
    execution_time_castle_pitway = end_time - start_time

    graph.plot([], [], color='red', label='DDA Algorithm')
    graph.plot([], [], color='blue', label='Bresenham Algorithm')
    graph.plot([], [], color='green', label='Castle-Pitway Algorithm')

    graph.legend(loc='upper right')  # Display the legend

    plt.title('Line Drawing Algorithms')

    print("Execution time of DDA algorithm:", execution_time_dda, "seconds")
    print("Execution time of Bresenham algorithm:", execution_time_bresenham, "seconds")
    print("Execution time of Castle-Pitway algorithm:", execution_time_castle_pitway, "seconds")

    tk.mainloop()
