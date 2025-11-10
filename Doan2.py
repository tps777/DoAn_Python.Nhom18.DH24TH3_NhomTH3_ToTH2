import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector

# ====== Kết nối MySQL ======
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",        # thay bằng user MySQL của bạn
        password="111111",        # thay bằng mật khẩu của bạn
        database="qlbaihat" # database vừa tạo ở trên
    )

# ====== Hàm canh giữa cửa sổ ======
def center_window(win, w=700, h=500):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')

# ====== Cửa sổ chính ======
root = tk.Tk()
root.title("Quản lý bài hát 🎵")
center_window(root, 700, 500)
root.resizable(False, False)

# ====== Tiêu đề ======
lbl_title = tk.Label(root, text="QUẢN LÝ BÀI HÁT", font=("Arial", 18, "bold"))
lbl_title.pack(pady=10)

# ====== Frame nhập thông tin ======
frame_info = tk.Frame(root)
frame_info.pack(pady=5, padx=10, fill="x")

tk.Label(frame_info, text="Mã BH").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_mabh = tk.Entry(frame_info, width=10)
entry_mabh.grid(row=0, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Thể loại").grid(row=0, column=2, padx=5, pady=5, sticky="w")
cbb_theloai = ttk.Combobox(frame_info, values=[
    "Pop", "Ballad", "Rock", "R&B", "Rap", "Indie"
], width=20)
cbb_theloai.grid(row=0, column=3, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Tên bài hát").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_tenbh = tk.Entry(frame_info, width=25)
entry_tenbh.grid(row=1, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Ca sĩ").grid(row=1, column=2, padx=5, pady=5, sticky="w")
entry_casi = tk.Entry(frame_info, width=20)
entry_casi.grid(row=1, column=3, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Yêu thích").grid(row=2, column=0, padx=5, pady=5, sticky="w")
like_var = tk.StringVar(value="Không")
tk.Radiobutton(frame_info, text="Có", variable=like_var, value="Có").grid(row=2, column=1, padx=5, sticky="w")
tk.Radiobutton(frame_info, text="Không", variable=like_var, value="Không").grid(row=2, column=1, padx=60, sticky="w")

tk.Label(frame_info, text="Ngày phát hành").grid(row=2, column=2, padx=5, pady=5, sticky="w")
date_entry = DateEntry(frame_info, width=12, background="darkblue", foreground="white", date_pattern="yyyy-mm-dd")
date_entry.grid(row=2, column=3, padx=5, pady=5, sticky="w")

# ====== Bảng danh sách ======
lbl_ds = tk.Label(root, text="Danh sách bài hát", font=("Arial", 10, "bold"))
lbl_ds.pack(pady=5, anchor="w", padx=10)

columns = ("mabh", "tenbh", "casi", "theloai", "ngayphathanh", "yeuthich")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col.capitalize())
tree.column("mabh", width=60, anchor="center")
tree.column("tenbh", width=150)
tree.column("casi", width=100)
tree.column("theloai", width=100)
tree.column("ngayphathanh", width=100, anchor="center")
tree.column("yeuthich", width=80, anchor="center")
tree.pack(padx=10, pady=5, fill="both")

# ====== CRUD ======
def clear_input():
    entry_mabh.delete(0, tk.END)
    entry_tenbh.delete(0, tk.END)
    entry_casi.delete(0, tk.END)
    like_var.set("Không")
    date_entry.set_date("2000-01-01")
    cbb_theloai.set("")

def load_data():
    for i in tree.get_children():
        tree.delete(i)
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM baihat")
    for row in cur.fetchall():
        tree.insert("", tk.END, values=row)
    conn.close()

def them_bh():
    mabh = entry_mabh.get()
    tenbh = entry_tenbh.get()
    casi = entry_casi.get()
    theloai = cbb_theloai.get()
    ngay = date_entry.get()
    yeuthich = like_var.get()
    if mabh == "" or tenbh == "" or casi == "":
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin!")
        return
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO baihat VALUES (%s,%s,%s,%s,%s,%s)",
                    (mabh, tenbh, casi, theloai, ngay, yeuthich))
        conn.commit()
        load_data()
        clear_input()
        messagebox.showinfo("Thành công", "Đã thêm bài hát!")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
    conn.close()

def xoa_bh():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Hãy chọn bài hát để xóa!")
        return
    mabh = tree.item(selected)["values"][0]
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM baihat WHERE mabh=%s", (mabh,))
    conn.commit()
    conn.close()
    load_data()

def sua_bh():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Hãy chọn bài hát để sửa!")
        return
    values = tree.item(selected)["values"]
    entry_mabh.delete(0, tk.END)
    entry_mabh.insert(0, values[0])
    entry_tenbh.delete(0, tk.END)
    entry_tenbh.insert(0, values[1])
    entry_casi.delete(0, tk.END)
    entry_casi.insert(0, values[2])
    cbb_theloai.set(values[3])
    date_entry.set_date(values[4])
    like_var.set(values[5])

def luu_bh():
    mabh = entry_mabh.get()
    tenbh = entry_tenbh.get()
    casi = entry_casi.get()
    theloai = cbb_theloai.get()
    ngay = date_entry.get()
    yeuthich = like_var.get()
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE baihat
        SET tenbh=%s, casi=%s, theloai=%s, ngayphathanh=%s, yeuthich=%s
        WHERE mabh=%s
    """, (tenbh, casi, theloai, ngay, yeuthich, mabh))
    conn.commit()
    conn.close()
    load_data()
    clear_input()

# ====== Frame nút ======
frame_btn = tk.Frame(root)
frame_btn.pack(pady=5)
tk.Button(frame_btn, text="Thêm", width=8, command=them_bh).grid(row=0, column=0, padx=5)
tk.Button(frame_btn, text="Lưu", width=8, command=luu_bh).grid(row=0, column=1, padx=5)
tk.Button(frame_btn, text="Sửa", width=8, command=sua_bh).grid(row=0, column=2, padx=5)
tk.Button(frame_btn, text="Hủy", width=8, command=clear_input).grid(row=0, column=3, padx=5)
tk.Button(frame_btn, text="Xóa", width=8, command=xoa_bh).grid(row=0, column=4, padx=5)
tk.Button(frame_btn, text="Thoát", width=8, command=root.quit).grid(row=0, column=5, padx=5)

# ====== Load dữ liệu ban đầu ======
load_data()
root.mainloop()
