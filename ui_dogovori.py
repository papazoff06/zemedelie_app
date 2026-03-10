import tkinter as tk
from tkinter import ttk
from crud_dokument import get_all_dokumenti
from crud_pravo import obshta_plosht_po_dogovor
from export_excel import export_renti_excel
from tkinter import filedialog

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
    def export():

        file = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel file", "*.xlsx")],
            initialfile="rent_report.xlsx"
        )

        if not file:
            return

        export_renti_excel(file)


    tk.Button(
        win,
        text="📊 Експорт в Excel",
        command=export
    ).pack(pady=10)

    dokumenti = get_all_dokumenti()

    # ─────────────
    # ПЪЛНЕНЕ НА ТАБЛИЦАТА
    # ─────────────

    def refresh():

        for row in tree.get_children():
            tree.delete(row)

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