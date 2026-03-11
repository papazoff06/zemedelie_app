import tkinter as tk
from tkinter import ttk
from crud_dokument import get_all_dokumenti
from crud_pravo import obshta_plosht_po_dogovor
from export_excel import export_renti_excel
from tkinter import filedialog
from datetime import date
from crud_dokument import create_dokument
from models import TipDokument
from ui_prava_kam_dogovor import open_prava_ui


def open_add_dogovor(refresh_callback):

    win = tk.Toplevel()
    win.title("Нов договор")
    win.geometry("350x350")

    tk.Label(win, text="№ договор").pack()
    e_nomer = tk.Entry(win)
    e_nomer.pack()

    tk.Label(win, text="Дата (YYYY-MM-DD)").pack()
    e_data = tk.Entry(win)
    e_data.insert(0, date.today().isoformat())
    e_data.pack()

    tk.Label(win, text="Тип договор").pack()

    cb_tip = ttk.Combobox(
        win,
        values=["naem", "arenda", "sobstvenost"],
        state="readonly",
        width=20
)

    cb_tip.pack()
    cb_tip.current(0)

    tk.Label(win, text="Наемодател").pack()
    e_naemodatel = tk.Entry(win)
    e_naemodatel.pack()

    tk.Label(win, text="ЕГН / Булстат").pack()
    e_egn = tk.Entry(win)
    e_egn.pack()

    def save():

        y, m, d = map(int, e_data.get().split("-"))

        create_dokument(
            nomer=e_nomer.get(),
            data=date(y, m, d),
            tip=TipDokument[cb_tip.get()],
            naemodatel=e_naemodatel.get(),
            egn_bulstat=e_egn.get(),
            filepath="",
            zabelezhka=None
        )

        refresh_callback()
        win.destroy()

    tk.Button(win, text="💾 Запази", command=save).pack(pady=10)


def open_dogovori_window():

    win = tk.Toplevel()
    win.title("Договори")
    win.geometry("900x450")

    # ─────────────
    # ТЪРСЕНЕ
    # ─────────────

    frame_search = tk.Frame(win)
    frame_search.pack(fill="x", padx=10, pady=5)

    tk.Label(frame_search, text="Име").pack(side="left")

    entry_name = tk.Entry(frame_search, width=20)
    entry_name.pack(side="left", padx=5)

    tk.Label(frame_search, text="ЕГН / Булстат").pack(side="left")

    entry_egn = tk.Entry(frame_search, width=15)
    entry_egn.pack(side="left", padx=5)

    # ─────────────
    # ТАБЛИЦА
    # ─────────────

    columns = ("nomer", "data", "tip", "plosht", "naemodatel", "egn")

    tree = ttk.Treeview(
        win,
        columns=columns,
        show="headings"
    )

    tree.heading("nomer", text="№ договор")
    tree.heading("data", text="Дата")
    tree.heading("tip", text="Тип")
    tree.heading("naemodatel", text="Наемодател")
    tree.heading("egn", text="ЕГН / Булстат")
    tree.heading("plosht", text="Обща площ (дка)")


    tree.column("nomer", width=100)
    tree.column("data", width=100)
    tree.column("tip", width=100)
    tree.column("naemodatel", width=250)
    tree.column("egn", width=150)
    tree.column("plosht", width=120)

    tree.pack(fill="both", expand=True, padx=10, pady=10)


    def open_prava(event):

        selected = tree.selection()

        if not selected:
            return

        dogovor_id = int(selected[0])
        open_prava_ui(dogovor_id)
       

    tree.bind("<Double-1>", open_prava)

    def export():

        file = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel file", "*.xlsx")],
            initialfile="rent_report.xlsx"
        )

        if not file:
            return

        export_renti_excel(file)


    tk.Button(win, text="➕ Нов договор", command=lambda: open_add_dogovor(refresh)).pack(pady=5)

    tk.Button(
        win,
        text="📊 Експорт в Excel",
        command=export
    ).pack(pady=10)


    # ─────────────
    # ПЪЛНЕНЕ НА ТАБЛИЦАТА
    # ─────────────

    def refresh():

        for row in tree.get_children():
            tree.delete(row)

        dokumenti = get_all_dokumenti()   # <-- тук

        name = entry_name.get().lower()
        egn = entry_egn.get()

        for d in dokumenti:

            if name and name not in (d.naemodatel or "").lower():
                continue

            if egn and egn not in (d.egn_bulstat or ""):
                continue

            plosht = obshta_plosht_po_dogovor(d.id)

            tree.insert(
                "",
                "end",
                iid=d.id,
                values=(
                    d.nomer,
                    d.data,
                    d.tip.value,
                    round(plosht, 2),
                    d.naemodatel or "",
                    d.egn_bulstat or ""
                )
            )

    tk.Button(
        frame_search,
        text="Търси",
        command=refresh
    ).pack(side="left", padx=10)

    refresh()