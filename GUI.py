import tkinter as tk
from tkinter import ttk
from LTI_Solver import *

HEIGHT = 600
WIDTH = 800
LABEL_FONT = ("TkDefaultFont", 12)
ENTRY_FONT = ("TkDefaultFont", 12)


def main():

    def select_output_order(event):
        nonlocal output_order
        output_order = combo_box1.get()
        combo_box2["state"] = "readonly"
        combo_box2["values"] = [i for i in range(0, int(output_order) + 1)]
        combo_box3["state"] = "readonly"

    def select_input_order(event):
        nonlocal input_order
        input_order = combo_box2.get()

    def select_input_signal(event):
        nonlocal input_signal
        input_signal = combo_box3.get()
        if input_signal == "unit step" or input_signal == "unit impulse":
            radiobutton3["state"] = "normal"
            radiobutton4["state"] = "normal"

        else:
            radiobutton3["state"] = "disable"
            radiobutton4["state"] = "disable"
            entry3["state"] = "disable"

    def time_interval():
        if check_time.get():
            entry1["state"] = "normal"
            entry2["state"] = "normal"

        else:
            entry1["state"] = "disable"
            entry2["state"] = "disable"

    def check_custom():
        if check_time_change.get():
            entry3["state"] = "normal"

        else:
            entry3["state"] = "disable"

    def start():
        # validate start and end time
        start_time, end_time = 0, 0
        if check_time.get():
            try:
                start_time, end_time = round(float(entry1.get()), 3), round(float(entry2.get()), 3)
                if start_time >= end_time:
                    label12["text"] = "Invalid Time Interval"
                    return
            except ValueError:
                label12["text"] = "Invalid Time Interval"
                return
        else:
            start_time = -1
            end_time = 10

        # validate output order
        out_order = 0
        in_signal = None
        if output_order is None:
            label12["text"] = "Invalid Output Order"
            return
        else:
            out_order = int(output_order)

        # validate input order
        in_order = 0
        if input_order is None:
            label12["text"] = "Invalid Input Order"
            return
        else:
            in_order = int(input_order)

        if in_order > out_order:
            label12["text"] = "Error: output order is lower than input order"
            return

        # initialize time interval
        Ns = int((end_time - start_time) * Fs)
        t = np.linspace(start_time, end_time - Ts, Ns)

        # validate input signal and step time
        step_time = 0
        idx = 0
        if input_signal == "unit step" or input_signal == "unit impulse":
            if check_time_change.get():
                try:
                    step_time = float(entry3.get())
                except ValueError:
                    label12["text"] = "Invalid Step/Impulse Time"
                    return
            else:
                step_time = 0

            if not start_time <= step_time <= end_time:
                label12["text"] = "Step/Impulse Time Out of Range"
                return

            # compute input signal
            in_signal = np.zeros(Ns)
            idx = round((step_time - start_time) * Fs + out_order)

            if input_signal == "unit step":
                for i in range(idx, Ns):
                    in_signal[i] = 1
            else:
                in_signal[idx] = 1 / Ts

        elif input_signal is None:
            label12["text"] = "Invalid Input Signal"
            return

        else:
            in_signal = eval("np.{}".format(input_signal))

        # validate output coefficients
        try:
            a = list(map(float, entry4.get().strip("[ ]").split()))
            a.reverse()
        except ValueError:
            label12["text"] = "Invalid Output Coefficients"
            return
        if len(a) != out_order + 1:
            label12["text"] = "Some of Output Coefficients are missing"
            return

        # validate input coefficients
        try:
            b = list(map(float, entry5.get().strip("[ ]").split()))
            b.reverse()
        except ValueError:
            label12["text"] = "Invalid Input Coefficients"
            return
        if len(b) != in_order + 1:
            label12["text"] = "Some of Input Coefficients are missing"
            return

        label12["text"] = simulate(Ns, t, in_signal, idx, out_order, in_order, a, b)
        plt.show()

    app = tk.Tk()
    app.title("ODE Solver")

    canvas = tk.Canvas(app, height=HEIGHT, width=WIDTH)
    canvas.pack()

    input_frame = tk.Frame(app, bd=4)
    input_frame.place(relheight=0.5, relwidth=1)

    output_frame = tk.Frame(app, bd=4)
    output_frame.place(relx=0, rely=0.5, relheight=0.5, relwidth=1)

    label1 = tk.Label(input_frame, anchor="nw", bd=10, font=("Times", "22", "bold italic"))
    label1["text"] = "This Program Solves ODE in the form of:"
    label1.place(relheight=0.2, relwidth=0.65)

    image1 = tk.PhotoImage(file='./equation.png')
    label2 = tk.Label(input_frame, image=image1)
    label2.place(relx=0.66, rely=0, relwidth=0.33, relheight=0.25)

    label3 = tk.Label(input_frame, text="Output Order(n):", anchor="nw", bd=4, font=LABEL_FONT)
    label3.place(relx=0, rely=0.4, relheight=0.1, relwidth=0.19)
    out_orders = [i for i in range(1, 11)]
    combo_box1 = ttk.Combobox(input_frame, values=out_orders, justify="center", font=ENTRY_FONT, state="readonly")
    combo_box1.bind("<<ComboboxSelected>>", select_output_order)
    combo_box1.place(relx=0.19, rely=0.4, relwidth=0.08, relheight=0.1)

    output_order = None

    label4 = tk.Label(input_frame, text="Input Order(n):", anchor="nw", bd=4, font=LABEL_FONT)
    label4.place(relx=0.3, rely=0.4, relheight=0.1, relwidth=0.17)
    combo_box2 = ttk.Combobox(input_frame, values=[None], justify="center", font=ENTRY_FONT, state="disable")
    combo_box2.bind("<<ComboboxSelected>>", select_input_order)
    combo_box2.place(relx=0.47, rely=0.4, relwidth=0.08, relheight=0.1)

    input_order = None

    label5 = tk.Label(input_frame, text="Input Signal(u):", anchor="nw", bd=4, font=LABEL_FONT)
    label5.place(relx=0, rely=0.55, relheight=0.1, relwidth=0.18)
    input_signals = ["unit step", "unit impulse", "sin(t)", "cos(t)", "exp(t)"]
    combo_box3 = ttk.Combobox(input_frame, values=input_signals, justify="center", font=ENTRY_FONT, state="disable")
    combo_box3.bind("<<ComboboxSelected>>", select_input_signal)
    combo_box3.place(relx=0.18, rely=0.55, relwidth=0.17, relheight=0.1)

    input_signal = None

    check_time = tk.BooleanVar()
    check_time.set("False")

    label6 = tk.Label(input_frame, text="Time Interval:", anchor="nw", bd=4, font=LABEL_FONT)
    label6.place(relx=0, rely=0.25, relheight=0.1, relwidth=0.16)
    radiobutton1 = tk.Radiobutton(input_frame, text="Default from -1s to 10s", variable=check_time,
                                  value=False, command=time_interval, font=LABEL_FONT)
    radiobutton1.place(relx=0.17, rely=0.25, relheight=0.1, relwidth=0.26)

    radiobutton2 = tk.Radiobutton(input_frame, text="Custom from", variable=check_time, value=True,
                                  command=time_interval, font=LABEL_FONT)
    radiobutton2.place(relx=0.48, rely=0.25, relheight=0.1, relwidth=0.18)

    entry1 = tk.Entry(input_frame, borderwidth=4, justify="center", font=10, state="disable")
    entry1.place(relx=0.66, rely=0.25, relheight=0.1, relwidth=0.07)

    label7 = tk.Label(input_frame, text="s to", anchor="nw", bd=4, font=LABEL_FONT)
    label7.place(relx=0.73, rely=0.25, relheight=0.1)

    entry2 = tk.Entry(input_frame, borderwidth=4, justify="center", font=10, state="disable")
    entry2.place(relx=0.775, rely=0.25, relheight=0.1, relwidth=0.07)

    label13 = tk.Label(input_frame, text="s", anchor="nw", bd=4, font=LABEL_FONT)
    label13.place(relx=0.845, rely=0.25, relheight=0.1, relwidth=0.03)

    check_time_change = tk.BooleanVar()
    check_time_change.set("False")

    label8 = tk.Label(input_frame, text="Step/Impulse Time:", anchor="nw", bd=4, font=LABEL_FONT)
    label8.place(relx=0.38, rely=0.55, relheight=0.1, relwidth=0.18)
    radiobutton3 = tk.Radiobutton(input_frame, text="Default (at 0s)", variable=check_time_change,
                                  value=False, command=check_custom, font=LABEL_FONT, state="disable")
    radiobutton3.place(relx=0.56, rely=0.55, relheight=0.1, relwidth=0.15)

    radiobutton4 = tk.Radiobutton(input_frame, text="Custom at", variable=check_time_change, value=True,
                                  command=check_custom, font=LABEL_FONT, state="disable")
    radiobutton4.place(relx=0.74, rely=0.55, relheight=0.1, relwidth=0.13)

    entry3 = tk.Entry(input_frame, borderwidth=4, justify="center", font=10, state="disable")
    entry3.place(relx=0.87, rely=0.55, relheight=0.1, relwidth=0.07)

    label9 = tk.Label(input_frame, text="s", anchor="nw", bd=4, font=LABEL_FONT)
    label9.place(relx=0.94, rely=0.55, relheight=0.1, relwidth=0.03)

    label10 = tk.Label(input_frame, text="Enter output coefficients in form [an an-1 an-2 .... a1 a0] below:",
                       anchor="nw", bd=4)
    label10.place(relx=0, rely=0.72, relheight=0.08, relwidth=0.45)
    entry4 = tk.Entry(input_frame, borderwidth=4, justify="center")
    entry4.place(relx=0, rely=0.8, relheight=0.1, relwidth=0.45)

    label11 = tk.Label(input_frame, text="Enter input coefficients in form [bn bn-1 bn-2 .... b1 b0] below:",
                       anchor="nw", bd=4)
    label11.place(relx=0.55, rely=0.72, relheight=0.08, relwidth=0.45)
    entry5 = tk.Entry(input_frame, borderwidth=4, justify="center")
    entry5.place(relx=0.55, rely=0.8, relheight=0.1, relwidth=0.45)

    label12 = tk.Label(output_frame, bg="white", anchor="center", bd=10, relief=tk.RIDGE,
                       font=("Courier", "14"), justify='left')
    label12.place(relx=0, rely=0, relheight=0.8, relwidth=1)

    button1 = tk.Button(output_frame, text="Solve", command=start, bd=8, font=("Times", "20", "bold italic"))
    button1.place(relx=0.5, rely=0.82, relheight=0.15, relwidth=0.2)

    button1 = tk.Button(output_frame, text="Cancel", command=app.destroy, bd=8, font=("Times", "20", "bold italic"))
    button1.place(relx=0.75, rely=0.82, relheight=0.15, relwidth=0.2)

    app.mainloop()


if __name__ == "__main__":
    main()
