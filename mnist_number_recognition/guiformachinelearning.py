import tkinter as tk
import json
import math

def out(inputs):

    def pool2(tensor):
        newTensor = []
        for y in range(0,27,2):

            lst = []

            for x in range(0,27,2):
                lst.append((tensor[y][x] + tensor[y+1][x+1] + tensor[y+1][x] + tensor[y][x+1])/4)

            newTensor.extend(lst)

        return newTensor
    
    def ReLU(x):
        return [max(0, val) for val in x]

    def dot_product(matrix, column_vector):
        return [sum(column_vector[i] * matrix[j][i] for i in range(len(column_vector))) for j in range(len(matrix))]
    
    def softmax(array):
        sum_of_exponentation = sum([math.exp(i) for i in array])
        return [math.exp(i)/sum_of_exponentation for i in array]

    output = softmax(dot_product(w3, ReLU(dot_product(w2, ReLU(dot_product(w1, pool2(inputs)))))))

    return output.index(max(output)), output[output.index(max(output))] * 100

def read_data(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)
    
def draw_on_canvas(event):
    x = event.x // 20
    y = event.y // 20

    canvas.create_rectangle(x * 20, y * 20, (x + 1) * 20, (y + 1) * 20, fill="white")

    try:
        pixel_colors[y][x] = "white"

    except:
        pass

def on_press(event):
    global left_button_pressed
    left_button_pressed = True

def on_release(event):
    global left_button_pressed
    left_button_pressed = False

def submit_button_clicked():
    pixels = []

    for y in range(canvas.winfo_height() // 20):
        row = []

        for x in range(canvas.winfo_width() // 20):

            color = pixel_colors[y][x]
            brightness = 255 if color == "white" else 0
            row.append(brightness)

        pixels.append(row)

    num, chance = out(pixels)

    status_label.config(text=f"I am {round(chance)}% sure that your number is a {num}")

def clear():
    global pixel_colors
    canvas.delete("all")
    pixel_colors = [["black" for _ in range(28)] for _ in range(28)]

w1 = read_data('weights1.json')
w2 = read_data('weights2.json')
w3 = read_data('weights3.json')

window = tk.Tk()
window.geometry('560x600')

canvas = tk.Canvas(window, bg="black", width=560, height=560)
canvas.pack()

submit_button = tk.Button(window, text="Submit", command=submit_button_clicked)

clear_button = tk.Button(window, text="CLEAR", command=clear)

submit_button.pack(side=tk.LEFT)
clear_button.pack(side=tk.RIGHT)

status_label = tk.Label(window, text="waiting for submission")
status_label.pack()

canvas.bind("<Button-1>", on_press)
canvas.bind("<ButtonRelease-1>", on_release)
canvas.bind("<B1-Motion>", draw_on_canvas)

pixel_colors = [["black" for _ in range(28)] for _ in range(28)]

window.mainloop()
