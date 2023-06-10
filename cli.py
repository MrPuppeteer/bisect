def create_func(exp):
    def f(x):
        # Using eval() safely in Python ref: https://lybniz2.sourceforge.net/safeeval.html
        safe_list = ['math', 'acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'degrees', 'e', 'exp', 'fabs', 'floor',
                     'fmod', 'fcexp', 'hypot', 'ldexp', 'log', 'log10', 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh']
        # use the list to filter the local namespace
        safe_dict = dict([(k, locals().get(k, k)) for k in safe_list])
        safe_dict['x'] = x
        return (eval(exp, {"__builtins__": None}, safe_dict))

    return f


def bisect(a, b, es, imax, f):
    i = 0
    c = b
    fa = f(a)
    fc = f(b)

    if (fa * fc > 0):
        print("Proses dihentikan, akar tidak ditemukan.")
        quit()

    while (True):
        # cold = c
        c = (a + b) / 2
        fc = f(c)
        i += 1

        if (c != 0):
            ea = abs(fc)

        test = fa * fc

        if (test < 0):
            b = c
        elif (test > 0):
            a = c
            fa = fc
        else:
            ea = 0

        if (ea < es or i >= imax):
            break

    return [c, ea, i]


def main():
    exp = input("Masukan fungsi: ")
    f = create_func(exp)

    print("Masukan nilai interval [a, b]:")
    a = float(input("a = "))
    b = float(input("b = "))
    while (b <= a):
        print("b tidak boleh kurang dari atau sama dengan a!")
        a = float(input("a = "))
        b = float(input("b = "))

    print("Masukan nilai toleransi error dan iterasi maksimum:")
    es = float(input("error = "))
    imax = int(input("imax  = "))
    while (imax < 1):
        print("Iterasi maksimum tidak boleh kurang dari 1!")
        imax = int(input("imax = "))

    res = bisect(a, b, es, imax, f)
    [c, ea, i] = res
    print("Dihasilkan Hampiran akar x = {:.6f}".format(c), end=' ')
    print("dengan error = {:.6f}".format(ea), end=' ')
    print("dan iterasi =", i)


if __name__ == "__main__":
    main()
