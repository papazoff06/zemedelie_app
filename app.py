import tkinter as tk
from tkinter import messagebox
from crud_imot import get_imot_by_nomer, create_imot
from crud_dogovor import create_dogovor
from tkinter import filedialog
import shutil
import os
from models import VidImot, NTP, Imot, Naem, Dogovor
from datetime import date
import sys
import subprocess
from crud_naem import dogovori_za_imot
from database import SessionLocal

def tarsi():
    nomer = entry_search.get().strip()
    imot = get_imot_by_nomer(nomer)

    if imot:
        result.set(
            f"Имот № {imot.imot_nomer}\n"
            f"ЕКАТТЕ: {imot.ecatte}\n"
            f"Обща площ: {imot.obshta_plosht} дка\n"
            f"Собствена площ: {imot.plosht_sobstvena or 0} дка\n"
            f"Наета площ: {imot.plosht_naeta or 0} дка\n"
            f"Вид: {imot.vid.value}\n"
            f"НТП: {imot.ntp.value}\n"
            f"Категория: {imot.kategoriya or '-'}\n"
            f"Местност: {imot.mestnost or '-'}"
        )
    else:
        result.set("❌ Няма такъв имот")

    global current_imot
    current_imot = imot


def open_add_imot():
    win = tk.Toplevel(root)
    win.title("Добави имот")
    win.geometry("360x520")

    entries = {}

    def field(label):
        tk.Label(win, text=label).pack()
        e = tk.Entry(win)
        e.pack()
        return e

    entries["ecatte"] = field("ЕКАТТЕ")
    entries["imot_nomer"] = field("Номер на имот")
    entries["obshta_plosht"] = field("Обща площ (дка)")
    entries["plosht_sobstvena"] = field("Собствена площ (дка)")
    entries["plosht_naeta"] = field("Наета площ (дка)")
    entries["mestnost"] = field("Местност")
    entries["kategoriya"] = field("Категория")
    entries["zabelezhka"] = field("Забележка")

    tk.Label(win, text="Вид имот").pack()
    vid_var = tk.StringVar(value="sobstven")
    tk.OptionMenu(win, vid_var, *[v.name for v in VidImot]).pack()

    tk.Label(win, text="НТП").pack()
    ntp_var = tk.StringVar(value="niva")
    tk.OptionMenu(win, ntp_var, *[n.name for n in NTP]).pack()

    def save():
        try:
            create_imot(
                ecatte=entries["ecatte"].get().strip(),
                imot_nomer=entries["imot_nomer"].get().strip(),
                obshta_plosht=float(entries["obshta_plosht"].get()),
                plosht_sobstvena=float(entries["plosht_sobstvena"].get() or 0),
                plosht_naeta=float(entries["plosht_naeta"].get() or 0),
                vid=VidImot[vid_var.get()],
                ntp=NTP[ntp_var.get()],
                mestnost=entries["mestnost"].get().strip(),
                kategoriya=entries["kategoriya"].get().strip(),
                zabelezhka=entries["zabelezhka"].get().strip() or None
            )
            messagebox.showinfo("OK", "Имотът е добавен успешно")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Грешка", str(e))

    tk.Button(win, text="💾 Запази", command=save).pack(pady=10)


def izberi_dogovor_pdf():
    filepath = filedialog.askopenfilename(
        title="Избери сканиран договор",
        filetypes=[("PDF файлове", "*.pdf")]
    )

    if not filepath:
        return None

    os.makedirs("data/dogovori", exist_ok=True)

    filename = os.path.basename(filepath)
    new_path = os.path.join("data/dogovori", filename)

    shutil.copy(filepath, new_path)

    return new_path


def open_add_dogovor():
    win = tk.Toplevel(root)
    win.title("Добави договор")
    win.geometry("360x360")

    tk.Label(win, text="Номер на договор").pack()
    e_nomer = tk.Entry(win)
    e_nomer.pack()

    tk.Label(win, text="Дата (YYYY-MM-DD)").pack()
    e_data = tk.Entry(win)
    e_data.insert(0, "2024-10-01")
    e_data.pack()

    tk.Label(win, text="Тип договор (наем / аренда)").pack()
    e_tip = tk.Entry(win)
    e_tip.pack()

    tk.Label(win, text="Забележка").pack()
    e_zab = tk.Entry(win)
    e_zab.pack()

    pdf_path_var = tk.StringVar(value="(няма избран файл)")

    def choose_pdf():
        path = izberi_dogovor_pdf()
        if path:
            pdf_path_var.set(path)

    tk.Button(win, text="📄 Избери PDF", command=choose_pdf).pack(pady=5)
    tk.Label(win, textvariable=pdf_path_var, wraplength=320).pack()

    def save():
        try:
            if pdf_path_var.get().startswith("("):
                raise Exception("Не е избран PDF файл")

            y, m, d = map(int, e_data.get().split("-"))

            create_dogovor(
                nomer=e_nomer.get().strip(),
                data=date(y, m, d),
                tip=e_tip.get().strip(),
                filepath=pdf_path_var.get(),
                zabelezhka=e_zab.get().strip() or None
            )

            messagebox.showinfo("OK", "Договорът е добавен успешно")
            win.destroy()

        except Exception as e:
            messagebox.showerror("Грешка", str(e))

    tk.Button(win, text="💾 Запази", command=save).pack(pady=10)


def open_file(filepath):
    if sys.platform.startswith("win"):
        os.startfile(filepath)
    elif sys.platform == "darwin":
        subprocess.call(["open", filepath])
    else:
        subprocess.call(["xdg-open", filepath])


def open_dogovori_for_imot(imot):
    dogovori = dogovori_za_imot(imot.id)

    if not dogovori:
        messagebox.showinfo("Инфо", "Няма договори за този имот")
        return

    win = tk.Toplevel(root)
    win.title(f"Договори за имот {imot.imot_nomer}")
    win.geometry("400x300")

    listbox = tk.Listbox(win)
    listbox.pack(fill="both", expand=True, padx=10, pady=10)

    for d in dogovori:
        listbox.insert(tk.END, f"{d.nomer} | {d.tip} | {d.data}")

    def show_selected():
        idx = listbox.curselection()
        if not idx:
            return

        dogovor = dogovori[idx[0]]

        # 1️⃣ отвори PDF
        open_file(dogovor.filepath)

        # 2️⃣ покажи имотите в договора
        show_imoti_in_dogovor(dogovor)

    tk.Button(win, text="📄 Отвори договор", command=show_selected).pack(pady=5)


def show_imoti_in_dogovor(dogovor):
    win = tk.Toplevel(root)
    win.title(f"Имоти в договор {dogovor.nomer}")
    win.geometry("450x300")

    session = SessionLocal()

    naemi = (
        session.query(Naem)
        .filter(Naem.dogovor_id == dogovor.id)
        .all()
    )

    for n in naemi:
        imot = session.get(Imot, n.imot_id)
        text = (
            f"Имот № {imot.imot_nomer} | "
            f"Площ: {n.plosht_dka} дка | "
            f"Цена: {n.cena_na_dka} лв/дка"
        )
        tk.Label(win, text=text, anchor="w").pack(fill="x", padx=10)

    session.close()

# ───── MAIN WINDOW ─────

root = tk.Tk()
root.title("Земеделски имоти")
root.geometry("320x260")

tk.Label(root, text="Номер на имот").pack()
entry_search = tk.Entry(root)
entry_search.pack()

tk.Button(root, text="Търси", command=tarsi).pack(pady=5)
tk.Button(root, text="➕ Добави имот", command=open_add_imot).pack(pady=5)
tk.Button(root, text="📄 Добави договор", command=open_add_dogovor).pack(pady=5)
tk.Button(root, text="📄 Покажи договори", command=lambda: open_dogovori_for_imot(current_imot)).pack(pady=5)

result = tk.StringVar()
tk.Label(root, textvariable=result, justify="left").pack(pady=5)


root.mainloop()


