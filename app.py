import tkinter as tk
from tkinter import messagebox

from crud_imot import create_imot, get_imot_by_nomer
from models import NTP

# ─────────────────────────────
# ТЪРСЕНЕ НА ИМОТ
# ─────────────────────────────

def tarsi():
    ecatte = entry_ecatte.get().strip()
    nomer = entry_imot.get().strip()

    if not ecatte or not nomer:
        messagebox.showwarning("Грешка", "Въведи ЕКАТТЕ и номер")
        return

    imot = get_imot_by_nomer(ecatte, nomer)

    if not imot:
        result.set("❌ Няма такъв имот")
        return

    text = (
        f"Имот № {imot.imot_nomer}\n"
        f"ЕКАТТЕ: {imot.ecatte}\n"
        f"Площ: {imot.plosht_kadastr} дка\n"
        f"НТП: {imot.ntp.value}\n"
        f"Категория: {imot.kategoriya or '-'}\n"
        f"Местност: {imot.mestnost or '-'}"
    )

    result.set(text)


# ─────────────────────────────
# ДОБАВЯНЕ НА ИМОТ
# ─────────────────────────────

def open_add_imot():

    win = tk.Toplevel(root)
    win.title("Добави имот")
    win.geometry("350x450")

    def field(label):
        tk.Label(win, text=label).pack()
        e = tk.Entry(win)
        e.pack()
        return e

    e_ecatte = field("ЕКАТТЕ")
    e_nomer = field("Номер на имот")
    e_plosht = field("Площ по кадастър (дка)")
    e_kategoriya = field("Категория")
    e_mestnost = field("Местност")
    e_zab = field("Забележка")

    tk.Label(win, text="НТП").pack()

    ntp_var = tk.StringVar(value="niva")

    tk.OptionMenu(
        win,
        ntp_var,
        *[n.name for n in NTP]
    ).pack()

    def save():

        try:

            create_imot(
                ecatte=e_ecatte.get().strip(),
                imot_nomer=e_nomer.get().strip(),
                plosht_kadastr=float(e_plosht.get()),
                ntp=NTP[ntp_var.get()],
                kategoriya=e_kategoriya.get().strip(),
                mestnost=e_mestnost.get().strip(),
                zabelezhka=e_zab.get().strip()
            )

            messagebox.showinfo("OK", "Имотът е добавен")
            win.destroy()

        except Exception as e:
            messagebox.showerror("Грешка", str(e))

    tk.Button(win, text="💾 Запази", command=save).pack(pady=10)


# ─────────────────────────────
# ДОГОВОРИ
# ─────────────────────────────

def open_dogovori():

    import ui_dogovori

    ui_dogovori.open_dogovori_window()


# ─────────────────────────────
# MAIN WINDOW
# ─────────────────────────────

root = tk.Tk()
root.title("Земеделски имоти")
root.geometry("320x320")

tk.Label(root, text="ЕКАТТЕ").pack()
entry_ecatte = tk.Entry(root)
entry_ecatte.pack()

tk.Label(root, text="Номер на имот").pack()
entry_imot = tk.Entry(root)
entry_imot.pack()

tk.Button(root, text="🔎 Търси", command=tarsi).pack(pady=5)

tk.Button(root, text="🌾 Добави имот", command=open_add_imot).pack(pady=5)

tk.Button(root, text="📄 Договори", command=open_dogovori).pack(pady=5)

result = tk.StringVar()

tk.Label(
    root,
    textvariable=result,
    justify="left"
).pack(pady=10)

root.mainloop()