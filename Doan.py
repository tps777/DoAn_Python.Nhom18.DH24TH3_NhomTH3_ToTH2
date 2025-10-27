import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
def center_window(win,w=700,h=500):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws//2)-(w//2)
    y = (hs//2)-(h//2)
    win.geometry(f'{w}x{h}+{x}+{y}')
# ====== KẾT NỐI DATABASE ======
def connect_db():
    conn = sqlite3.connect("songs.db")
    return conn

# ====== TẠO BẢNG ======
def create_table():
    conn = connect_db()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ten TEXT NOT NULL,
            ca_si TEXT,
            the_loai TEXT
        )
    """)
    conn.commit()
    conn.close()

# ====== HÀM HIỂN THỊ ======
def hien_thi(ket_qua=None):
    for row in tree.get_children():
        tree.delete(row)
    conn = connect_db()
    c = conn.cursor()
    if ket_qua:
        for row in ket_qua:
            tree.insert("", "end", values=row)
    else:
        c.execute("SELECT * FROM songs")
        for row in c.fetchall():
            tree.insert("", "end", values=row)
    conn.close()

# ====== HÀM THÊM ======
def them_bai_hat():
    ten = entry_ten.get().strip()
    ca_si = entry_casi.get().strip()
    the_loai = entry_theloai.get().strip()
    if ten == "":
        messagebox.showwarning("Lỗi", "Tên bài hát không được để trống!")
        return
    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO songs (ten, ca_si, the_loai) VALUES (?, ?, ?)", (ten, ca_si, the_loai))
    conn.commit()
    conn.close()
    hien_thi()
    entry_ten.delete(0, tk.END)
    entry_casi.delete(0, tk.END)
    entry_theloai.delete(0, tk.END)
    messagebox.showinfo("Thành công", "Đã thêm bài hát!")

# ====== HÀM XÓA ======
def xoa_bai_hat():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Lỗi", "Hãy chọn bài hát để xóa!")
        return
    item = tree.item(selected[0])
    song_id = item["values"][0]
    conn = connect_db()
    c = conn.cursor()
    c.execute("DELETE FROM songs WHERE id = ?", (song_id,))
    conn.commit()
    conn.close()
    hien_thi()
    messagebox.showinfo("Thành công", "Đã xóa bài hát!")

# ====== HÀM CHỌN BÀI ======
def chon_bai_hat(event):
    selected = tree.selection()
    if not selected:
        return
    item = tree.item(selected[0])
    entry_ten.delete(0, tk.END)
    entry_casi.delete(0, tk.END)
    entry_theloai.delete(0, tk.END)
    entry_ten.insert(0, item["values"][1])
    entry_casi.insert(0, item["values"][2])
    entry_theloai.insert(0, item["values"][3])

# ====== HÀM CẬP NHẬT ======
def cap_nhat():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Lỗi", "Hãy chọn bài hát để cập nhật!")
        return
    item = tree.item(selected[0])
    song_id = item["values"][0]
    ten = entry_ten.get().strip()
    ca_si = entry_casi.get().strip()
    the_loai = entry_theloai.get().strip()
    conn = connect_db()
    c = conn.cursor()
    c.execute("UPDATE songs SET ten=?, ca_si=?, the_loai=? WHERE id=?",
              (ten, ca_si, the_loai, song_id))
    conn.commit()
    conn.close()
    hien_thi()
    messagebox.showinfo("Thành công", "Đã cập nhật bài hát!")

# ====== HÀM TÌM KIẾM ======
def tim_kiem():
    tu_khoa = entry_tim.get().strip()
    if tu_khoa == "":
        hien_thi()
        return
    conn = connect_db()
    c = conn.cursor()
    c.execute("""
        SELECT * FROM songs
        WHERE ten LIKE ? OR ca_si LIKE ?
    """, (f"%{tu_khoa}%", f"%{tu_khoa}%"))
    ket_qua = c.fetchall()
    conn.close()
    if not ket_qua:
        messagebox.showinfo("Kết quả", "Không tìm thấy bài hát phù hợp!")
    hien_thi(ket_qua)

# ====== HÀM GIỚI THIỆU ======
def gioi_thieu():
    messagebox.showinfo(
        "Giới thiệu",
        "🎵 Ứng dụng Quản lý bài hát\n\n"
        "Phiên bản: 1.0\nTác giả: ChatGPT & Bạn\nNgôn ngữ: Python, Tkinter, SQLite"
    )

# ====== HÀM THOÁT ======
def thoat():
    if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn thoát không?"):
        root.destroy()

# ====== GIAO DIỆN TKINTER ======
root = tk.Tk()
root.title("🎶 Quản lý bài hát (Tkinter + SQLite + Menu)")
root.geometry("700x520")

create_table()

# === MENU BAR ===
menubar = tk.Menu(root)

# Menu File
menu_file = tk.Menu(menubar, tearoff=0)
menu_file.add_command(label="Thoát", command=thoat)
menubar.add_cascade(label="File", menu=menu_file)

# Menu Bài hát
menu_song = tk.Menu(menubar, tearoff=0)
menu_song.add_command(label="Thêm", command=them_bai_hat)
menu_song.add_command(label="Cập nhật", command=cap_nhat)
menu_song.add_command(label="Xóa", command=xoa_bai_hat)
menu_song.add_separator()
menu_song.add_command(label="Hiển thị tất cả", command=hien_thi)
menubar.add_cascade(label="Bài hát", menu=menu_song)

# Menu Tìm kiếm
menu_search = tk.Menu(menubar, tearoff=0)
menu_search.add_command(label="Tìm kiếm bài hát", command=lambda: entry_tim.focus_set())
menubar.add_cascade(label="Tìm kiếm", menu=menu_search)

# Menu Trợ giúp
menu_help = tk.Menu(menubar, tearoff=0)
menu_help.add_command(label="Giới thiệu", command=gioi_thieu)
menubar.add_cascade(label="Trợ giúp", menu=menu_help)

root.config(menu=menubar)

# === KHUNG NHẬP LIỆU ===
frame_input = tk.LabelFrame(root, text="Thông tin bài hát", padx=10, pady=10)
frame_input.pack(pady=10, fill="x")

tk.Label(frame_input, text="Tên bài hát:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_ten = tk.Entry(frame_input, width=40)
entry_ten.grid(row=0, column=1, padx=5)

tk.Label(frame_input, text="Ca sĩ:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_casi = tk.Entry(frame_input, width=40)
entry_casi.grid(row=1, column=1, padx=5)

tk.Label(frame_input, text="Thể loại:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_theloai = tk.Entry(frame_input, width=40)
entry_theloai.grid(row=2, column=1, padx=5)

# === KHUNG NÚT ===
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=5)

tk.Button(frame_buttons, text="Thêm", command=them_bai_hat, width=10).grid(row=0, column=0, padx=5)
tk.Button(frame_buttons, text="Cập nhật", command=cap_nhat, width=10).grid(row=0, column=1, padx=5)
tk.Button(frame_buttons, text="Xóa", command=xoa_bai_hat, width=10).grid(row=0, column=2, padx=5)
tk.Button(frame_buttons, text="Hiển thị", command=hien_thi, width=10).grid(row=0, column=3, padx=5)

# === KHUNG TÌM KIẾM ===
frame_search = tk.LabelFrame(root, text="Tìm kiếm bài hát", padx=10, pady=10)
frame_search.pack(pady=5, fill="x")

tk.Label(frame_search, text="Nhập từ khóa:").grid(row=0, column=0, padx=5)
entry_tim = tk.Entry(frame_search, width=30)
entry_tim.grid(row=0, column=1, padx=5)
tk.Button(frame_search, text="Tìm", command=tim_kiem, width=10).grid(row=0, column=2, padx=5)
tk.Button(frame_search, text="Hiển thị tất cả", command=hien_thi, width=12).grid(row=0, column=3, padx=5)

# === BẢNG DANH SÁCH ===
cols = ("ID", "Tên bài hát", "Ca sĩ", "Thể loại")
tree = ttk.Treeview(root, columns=cols, show="headings")
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=150)
tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
tree.bind("<<TreeviewSelect>>", chon_bai_hat)

# Hiển thị ban đầu
hien_thi()

root.mainloop()