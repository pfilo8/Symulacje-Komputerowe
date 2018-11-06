import tkinter as tk
from tkinter import ttk
import matplotlib
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import numpy as np
from Zad2_Symulacje import paris_ruin

matplotlib.use("TkAgg")
LARGE_FONT = ("Verdana", 12)

def animate(i):
    global x, y

    if (i + 1) % len(holder[1]) == 0:
        y = [holder[1][0]]
        x = [0]
    else:
        y = holder[1][0:(i+1) % len(holder[2])]
        x = holder[2][0:(i+1) % len(holder[2])]

    wykres.set_data(x, y)
    a.set_ylim([min(holder[1])-1/10*min(holder[1]), max(holder[1])+1/10*max(holder[1])])
    a.set_xlim(-1, (len(holder[2])+1))


class Graphics(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame = StartPage(container, self)

        self.frames[StartPage] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Śliczna animacja", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()


if __name__ == '__main__':
    f = Figure(figsize=(5, 5), dpi=100)
    a = f.add_subplot(111)
    k_0 = 500000
    holder = paris_ruin(k=k_0, n=100, oc=120, m_oc=240, m=200, ac=120, m_ac=240, mi=30, s_oc=0, start_year=2000,
                       end_year=2009, text=False, strategy=True)

    x = [0 for i in range(len(holder[1]))]
    y = [k_0 for i in range(len(holder[2]))]

    wykres, = a.plot(x, y)

    app = Graphics()
    ani = animation.FuncAnimation(f, animate, interval=1)

    app.mainloop()
