import tkinter
from customtkinter import *
from tkinter import messagebox
from math import *


def f(x, exp):
    # Using eval() safely in Python ref: https://lybniz2.sourceforge.net/safeeval.html
    safe_list = ['math', 'acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'degrees', 'e', 'exp', 'fabs', 'floor',
                 'fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10', 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh']
    # use the list to filter the local namespace
    safe_dict = dict([(k, locals().get(k, k)) for k in safe_list])
    safe_dict['x'] = x
    return (eval(exp, {"__builtins__": None}, safe_dict))


def bisect(a, b, es, imax, f, exp):
    i = 0
    c = b
    fa = f(a, exp)
    fc = f(b, exp)
    res = [["iterasi", "a", "b", "c", "f(a)", "f(c)", "f(a).f(c)", "e"]]

    if (fa * fc > 0):
        return -1

    while (True):
        # cold = c
        c = (a + b) / 2
        fc = f(c, exp)
        i += 1

        if (c != 0):
            # ea = abs((c - cold) / c)
            ea = abs(fc)

        test = fa * fc

        res.append([
            "{}".format(i), "{:.6f}".format(a), "{:.6f}".format(b),
            "{:.6f}".format(c), "{:.6f}".format(fa), "{:.6f}".format(fc),
            "{:.6f}".format(test), "{:.6f}".format(ea)
        ])

        if (test < 0):
            b = c
        elif (test > 0):
            a = c
            fa = fc
        else:
            ea = 0

        if (ea < es or i >= imax):
            break

    return [res, c, ea, i]


class InputFrame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Expression Input
        self.exp_label = CTkLabel(
            self, text="Fungsi", fg_color="gray30", corner_radius=6)
        self.exp_label.grid(
            row=0, column=0, padx=10, pady=(10, 0), sticky="ew", columnspan=2)
        self.exp_entry = CTkEntry(self, corner_radius=6)
        self.exp_entry.grid(row=0, column=2, padx=10, pady=(
            10, 0), sticky="ew", columnspan=2)

        # Interval (a & b) Input
        self.a_label = CTkLabel(
            self, text="Batas Bawah", fg_color="gray30", corner_radius=6)
        self.a_label.grid(
            row=1, column=0, padx=10, pady=(10, 0), sticky="ew")
        self.a_entry = CTkEntry(self, corner_radius=6)
        self.a_entry.grid(
            row=1, column=1, padx=10, pady=(10, 0), sticky="ew")
        self.b_label = CTkLabel(
            self, text="Batas Atas", fg_color="gray30", corner_radius=6)
        self.b_label.grid(
            row=1, column=2, padx=10, pady=(10, 0), sticky="ew")
        self.b_entry = CTkEntry(self, corner_radius=6)
        self.b_entry.grid(
            row=1, column=3, padx=10, pady=(10, 0), sticky="ew")

        self.es_label = CTkLabel(
            self, text="Toleransi Error", fg_color="gray30", corner_radius=6)
        self.es_label.grid(
            row=2, column=0, padx=10, pady=10, sticky="ew")
        self.es_entry = CTkEntry(self, corner_radius=6)
        self.es_entry.grid(
            row=2, column=1, padx=10, pady=10, sticky="ew")
        self.imax_label = CTkLabel(
            self, text="Iterasi Maksimum", fg_color="gray30", corner_radius=6)
        self.imax_label.grid(
            row=2, column=2, padx=10, pady=10, sticky="ew")
        self.imax_entry = CTkEntry(self, corner_radius=6)
        self.imax_entry.grid(
            row=2, column=3, padx=10, pady=10, sticky="ew")

    def get_exp(self):
        return self.exp_entry.get()

    def get_a(self):
        return self.a_entry.get()

    def get_b(self):
        return self.b_entry.get()

    def get_es(self):
        return self.es_entry.get()

    def get_imax(self):
        return self.imax_entry.get()

    def reset(self):
        self.exp_entry.delete(0, END)
        self.a_entry.delete(0, END)
        self.b_entry.delete(0, END)
        self.es_entry.delete(0, END)
        self.imax_entry.delete(0, END)


class ButtonFrame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(1, weight=1)

        self.calc_button = CTkButton(
            self, text="Hitung", command=master.calculate)
        self.calc_button.grid(
            row=0, column=0, padx=10, pady=0, sticky="ew")
        self.reset_button = CTkButton(
            self, text="Reset", command=master.reset, state=DISABLED)
        self.reset_button.grid(
            row=0, column=1, padx=10, pady=0, sticky="ew")


class App(CTk):
    def __init__(self):
        super().__init__()

        self.title("Metode Biseksi")
        self.geometry("685x560")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.title_label = CTkLabel(
            self, text="Metode Biseksi", fg_color="transparent", corner_radius=6, font=CTkFont(size=20, weight='bold'))
        self.title_label.grid(row=0, column=0, padx=10,
                              pady=(10, 0), sticky="ew")

        self.input_frame = InputFrame(self)
        self.input_frame.grid(row=1, column=0, padx=10,
                              pady=(10, 0), sticky="")

        self.button_frame = ButtonFrame(self)
        self.button_frame.grid(row=2, column=0, padx=10,
                               pady=(10, 0), sticky="")
        self.button_frame.configure(fg_color="transparent")
        self.result_frame = None

    def calculate(self):
        exp = self.input_frame.get_exp()
        a = self.input_frame.get_a()
        b = self.input_frame.get_b()
        es = self.input_frame.get_es()
        imax = self.input_frame.get_imax()

        if (exp == "" or a == "" or b == "" or es == "" or imax == ""):
            messagebox.showerror(
                title="Error!",
                message="Input tidak boleh kosong!"
            )
            return

        exp = str(exp)
        a = float(a)
        b = float(b)
        es = float(es)
        imax = int(imax)

        if (b <= a):
            messagebox.showerror(
                title="Error!",
                message="Batas Atas tidak boleh kurang dari atau sama dengan Batas Bawah!"
            )
            return

        if (imax < 1):
            messagebox.showerror(
                title="Error!",
                message="Iterasi maksimum tidak boleh kurang dari 1!"
            )
            return

        result = bisect(a, b, es, imax, f, exp)
        if (result == -1):
            messagebox.showerror(
                title="Syarat tidak terpenuhi!",
                message="f(a).f(b) > 0\nAkar tidak ditemukan! Proses dihentikan."
            )
            return

        self.result_frame = CTkScrollableFrame(self)
        self.result_frame.grid(row=3, column=0, padx=10,
                               pady=10, sticky="nsew")

        [res, c, ea, i] = result
        for i in range(len(res)):
            for j in range(len(res[0])):
                entry = CTkEntry(self.result_frame,
                                 justify="center", corner_radius=0, width=80)
                entry.grid(row=i, column=j)
                entry.insert(0, res[i][j])
                entry.configure(state=DISABLED)

        self.button_frame.calc_button.configure(state=DISABLED)
        self.button_frame.reset_button.configure(state=NORMAL)
        messagebox.showinfo(
            title="Hasil",
            message="Dihasilkan hampiran akar = {:.6f}".format(c)
                    + " dengan error = {:.6f}".format(ea)
                    + " dan iterasi = {}".format(i)
        )

    def reset(self):
        self.result_frame.grid_forget()
        self.input_frame.reset()
        self.button_frame.reset_button.configure(state=DISABLED)
        self.button_frame.calc_button.configure(state=NORMAL)


def main():
    set_appearance_mode("dark")
    set_default_color_theme("blue")

    app = App()

    app.mainloop()


if __name__ == "__main__":
    main()
