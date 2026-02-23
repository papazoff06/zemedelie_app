import tkinter as tk
from tkinter import messagebox
from crud_imot import get_imot_by_nomer, create_imot
from tkinter import filedialog
import shutil
import os
from models import VidImot, NTP

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


