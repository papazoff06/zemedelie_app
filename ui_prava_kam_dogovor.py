import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from database import SessionLocal
from models import Imot, PravoImot, TipPravo


def load_imoti():
    session = SessionLocal()
    imoti = session.query(Imot).order_by(Imot.ecatte, Imot.imot_nomer).all()
    session.close()
    return imoti


def open_prava_ui(dokument_id):

    win = tk.Toplevel()
    win.title("Имотите по договора")
    win.geometry("750x450")

    # ───────── ИЗБОР НА ИМОТ ─────────

    tk.Label(win, text="Имот").pack()

    imoti = load_imoti()

    imot_map = {
        f"{i.ecatte} | {i.imot_nomer}": i.id
        for i in imoti
    }

    cb_imot = ttk.Combobox(
        win,
        values=list(imot_map.keys()),
        state="readonly",
        width=50
    )
    cb_imot.pack()

    # ───────── ТИП ПРАВО ─────────

    tk.Label(win, text="Тип право").pack()

    cb_tip = ttk.Combobox(
        win,
        values=[t.value for t in TipPravo],
        state="readonly"
    )
    cb_tip.pack()

    # ───────── ПЛОЩ ─────────

    tk.Label(win, text="Площ по право (дка)").pack()
    e_plosht = tk.Entry(win)
    e_plosht.pack()

    # ───────── ЦЕНА ─────────

    tk.Label(win, text="Цена на дка (€/дка или кг/дка)").pack()
    e_cena = tk.Entry(win)
    e_cena.pack()

    # ───────── ДАТИ ─────────

    tk.Label(win, text="Дата начало").pack()
    e_start = tk.Entry(win)
    e_start.insert(0, date.today().isoformat())
    e_start.pack()

    tk.Label(win, text="Дата край (празно = безсрочно)").pack()
    e_end = tk.Entry(win)
    e_end.pack()

    # ───────── ТАБЛИЦА ─────────

    cols = ("imot", "plosht", "cena", "suma", "nachalo", "krai")

    tree = ttk.Treeview(win, columns=cols, show="headings")

    tree.heading("imot", text="Имот")
    tree.heading("plosht", text="Площ")
    tree.heading("cena", text="Цена/дка")
    tree.heading("suma", text="Сума €")
    tree.heading("nachalo", text="Начало")
    tree.heading("krai", text="Край")

    tree.pack(fill="both", expand=True, padx=10, pady=10)
    total_label = tk.Label(win, text="", font=("Arial", 11, "bold"))
    total_label.pack(pady=5)
    
    # ───────── ЗАРЕЖДАНЕ НА ПРАВАТА ─────────

    def load_prava():

        for r in tree.get_children():
            tree.delete(r)

        session = SessionLocal()

        prava = (
            session.query(PravoImot)
            .filter_by(dokument_id=dokument_id)
            .all()
        )

        total = 0
        for p in prava:
            cena = p.cena_na_dka or 0
            suma = p.plosht_pravo * cena

            total += suma

            tree.insert(
                "",
                "end",
                values=(
                    f"{p.imot.ecatte} | {p.imot.imot_nomer}",
                    p.plosht_pravo,
                    cena,
                    round(suma, 2),
                    p.data_nachalo,
                    p.data_krai or ""
                )
            )
        total_label.config(text=f"Обща сума: {round(total,2)} €")
        session.close()

    # ───────── ЗАПИС ─────────

    def save_pravo():
        try:

            imot_id = imot_map[cb_imot.get()]
            tip_pravo = TipPravo(cb_tip.get())

            data_krai = (
                date.fromisoformat(e_end.get())
                if e_end.get().strip()
                else None
            )

            session = SessionLocal()

            cena = float(e_cena.get()) if e_cena.get() else 0
            pravo = PravoImot(
                imot_id=imot_id,
                dokument_id=dokument_id,
                tip_pravo=tip_pravo,
                plosht_pravo=float(e_plosht.get()),
                cena_na_dka=cena,
                data_nachalo=date.fromisoformat(e_start.get()),
                data_krai=data_krai,
            )

            session.add(pravo)
            session.commit()
            session.close()

            

            messagebox.showinfo("OK", "Имотът е добавен към договора")

            load_prava()

        except Exception as e:
            messagebox.showerror("Грешка", str(e))

    tk.Button(win, text="➕ Запази", command=save_pravo).pack(pady=10)

    load_prava()