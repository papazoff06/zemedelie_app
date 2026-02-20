import tkinter as tk
from tkinter import messagebox
from crud import get_imot_by_nomer, create_imot


def tarsi():
    nomer = entry_search.get().strip()
    imot = get_imot_by_nomer(nomer)

    if imot:
        result.set(
            f"Имот № {imot.imot_nomer}\n"
            f"Площ: {imot.plosht} дка\n"
            f"Вид: {imot.vid}\n"
            f"Процент: {imot.procent}%"
        )
    else:
        result.set("❌ Няма такъв имот")


def open_add_imot():
    win = tk.Toplevel(root)
    win.title("Добави имот")
    win.geometry("300x250")

    tk.Label(win, text="Номер на имот").pack()
    e_nomer = tk.Entry(win)
    e_nomer.pack()

    tk.Label(win, text="Площ (дка)").pack()
    e_plosht = tk.Entry(win)
    e_plosht.pack()

    tk.Label(win, text="Вид (sobstven / naet / sasobshtven)").pack()
    e_vid = tk.Entry(win)
    e_vid.pack()

    tk.Label(win, text="Процент").pack()
    e_procent = tk.Entry(win)
    e_procent.pack()

    def save():
        try:
            create_imot(
                imot_nomer=e_nomer.get().strip(),
                plosht=float(e_plosht.get()),
                vid=e_vid.get().strip(),
                procent=float(e_procent.get())
            )
            messagebox.showinfo("OK", "Имотът е добавен")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Грешка", str(e))

    tk.Button(win, text="Запази", command=save).pack(pady=10)


# ───── MAIN WINDOW ─────

root = tk.Tk()
root.title("Земеделски имоти")
root.geometry("320x260")

tk.Label(root, text="Номер на имот").pack()
entry_search = tk.Entry(root)
entry_search.pack()

tk.Button(root, text="Търси", command=tarsi).pack(pady=5)
tk.Button(root, text="➕ Добави имот", command=open_add_imot).pack(pady=5)

result = tk.StringVar()
tk.Label(root, textvariable=result, justify="left").pack(pady=5)

root.mainloop()
