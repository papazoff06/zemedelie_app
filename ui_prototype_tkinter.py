import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# --- Main window ---
root = tk.Tk()
root.title("Земеделски имоти")
root.geometry("1000x600")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# ================= TAB 1: ИМОТИ =================
frame_imoti = ttk.Frame(notebook)
notebook.add(frame_imoti, text="Имоти")

columns_imoti = ("ЕКАТТЕ", "Имот №", "НТП", "Площ 1", "Площ 2", "Площ 3")

tree_imoti = ttk.Treeview(frame_imoti, columns=columns_imoti, show="headings")
for col in columns_imoti:
    tree_imoti.heading(col, text=col)
    tree_imoti.column(col, width=120)

tree_imoti.pack(fill="both", expand=True, padx=10, pady=10)

btn_frame_imoti = ttk.Frame(frame_imoti)
btn_frame_imoti.pack(pady=5)

ttk.Button(btn_frame_imoti, text="➕ Нов имот").pack(side="left", padx=5)
ttk.Button(btn_frame_imoti, text="✏️ Редакция").pack(side="left", padx=5)
ttk.Button(btn_frame_imoti, text="📎 Документи").pack(side="left", padx=5)

# ================= TAB 2: ДОГОВОРИ =================
frame_dogovori = ttk.Frame(notebook)
notebook.add(frame_dogovori, text="Договори + имоти")

# --- Top: Dogovor data ---
frame_top = ttk.LabelFrame(frame_dogovori, text="Данни за договор")
frame_top.pack(fill="x", padx=10, pady=10)

# Row 1

ttk.Label(frame_top, text="Номер:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_nomer = ttk.Entry(frame_top, width=20)
entry_nomer.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_top, text="Дата:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
entry_date = ttk.Entry(frame_top, width=15)
entry_date.grid(row=0, column=3, padx=5, pady=5)

# Row 2

ttk.Label(frame_top, text="Тип договор:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
combo_tip = ttk.Combobox(frame_top, values=["наем", "аренда", "собственост"], width=18)
combo_tip.grid(row=1, column=1, padx=5, pady=5)

# Price type
price_type = tk.StringVar(value="eur")

ttk.Radiobutton(frame_top, text="€/дка", variable=price_type, value="eur").grid(row=1, column=2)
ttk.Radiobutton(frame_top, text="кг/дка (пшеница)", variable=price_type, value="kg").grid(row=1, column=3)

# Row 3

ttk.Label(frame_top, text="Стойност:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_price = ttk.Entry(frame_top, width=20)
entry_price.grid(row=2, column=1, padx=5, pady=5)

# File attach

def attach_pdf():
    filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])


ttk.Button(frame_top, text="📎 Прикачи договор", command=attach_pdf).grid(row=2, column=2, padx=5, pady=5)

# Notes

ttk.Label(frame_top, text="Забележка:").grid(row=3, column=0, padx=5, pady=5, sticky="ne")
text_note = tk.Text(frame_top, height=2, width=60)
text_note.grid(row=3, column=1, columnspan=3, padx=5, pady=5)

# Action buttons
btn_frame_top = ttk.Frame(frame_top)
btn_frame_top.grid(row=0, column=4, rowspan=4, padx=10)

ttk.Button(btn_frame_top, text="💾 Запази").pack(pady=3)
ttk.Button(btn_frame_top, text="🆕 Нов").pack(pady=3)
ttk.Button(btn_frame_top, text="🗑 Изтрий").pack(pady=3)

# --- Bottom: Imoti in dogovor ---
frame_bottom = ttk.LabelFrame(frame_dogovori, text="Имоти в договора")
frame_bottom.pack(fill="both", expand=True, padx=10, pady=10)

columns_dogovor_imoti = ("Имот №", "ЕКАТТЕ", "НТП", "Площ 1", "Площ 2", "Площ 3", "Рента")

tree_dogovor_imoti = ttk.Treeview(frame_bottom, columns=columns_dogovor_imoti, show="headings")
for col in columns_dogovor_imoti:
    tree_dogovor_imoti.heading(col, text=col)
    tree_dogovor_imoti.column(col, width=110)

tree_dogovor_imoti.pack(fill="both", expand=True, padx=5, pady=5)

btn_frame_bottom = ttk.Frame(frame_bottom)
btn_frame_bottom.pack(pady=5)

ttk.Button(btn_frame_bottom, text="➕ Добави имот").pack(side="left", padx=5)
ttk.Button(btn_frame_bottom, text="➖ Премахни имот").pack(side="left", padx=5)
ttk.Button(btn_frame_bottom, text="🔍 Избери имот").pack(side="left", padx=5)

# ================= TAB 3: ПЛАЩАНИЯ =================
frame_plashtania = ttk.Frame(notebook)
notebook.add(frame_plashtania, text="Ренти / Плащания")

ttk.Label(frame_plashtania, text="(тук ще е справката за ренти)").pack(pady=50)

# ================= TAB 4: ДЕКЛАРАЦИИ =================
frame_deklaracii = ttk.Frame(notebook)
notebook.add(frame_deklaracii, text="Декларации 69 / 70")

ttk.Label(frame_deklaracii, text="(генериране на декларации)").pack(pady=50)

# ================= TAB 5: ДОКУМЕНТИ =================
frame_docs = ttk.Frame(notebook)
notebook.add(frame_docs, text="Документи")

ttk.Label(frame_docs, text="(всички прикачени PDF файлове)").pack(pady=50)

root.mainloop()
