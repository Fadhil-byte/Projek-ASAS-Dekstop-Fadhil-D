import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

def connect_db():
    return sqlite3.connect("users.db")

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            email TEXT,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_data():
    nama = entry_nama.get()
    email = entry_email.get()
    password = entry_password.get()
    
    if not email.endswith('@gmail.com'):
        messagebox.showwarning("Email Error", "Email harus berakhiran @gmail.com!")
        return
    if nama and email and password:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (nama, email, password) VALUES (?, ?, ?)", (nama, email, password))
        conn.commit()
        conn.close()
        treeview.insert('', 'end', values=(nama, email, password))
        clear_inputs()
        messagebox.showinfo("Success", "Data berhasil ditambahkan!")
    else:
        messagebox.showwarning("Input Error", "Semua field harus diisi!")

def update_data():
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Pilih data yang ingin diubah.")
        return
    
    selected_item = selected_item[0]
    new_nama = entry_nama.get()
    new_email = entry_email.get()
    new_password = entry_password.get()
    
    if not new_email.endswith('@gmail.com'):
        messagebox.showwarning("Email Error", "Email harus berakhiran @gmail.com!")
        return
    
    if new_nama and new_email and new_password:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET nama = ?, email = ?, password = ? WHERE nama = ? AND email = ? AND password = ?",
                       (new_nama, new_email, new_password, 
                        treeview.item(selected_item, 'values')[0], 
                        treeview.item(selected_item, 'values')[1], 
                        treeview.item(selected_item, 'values')[2]))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Data berhasil diubah!")
        load_data()
        clear_inputs()
        toggle_buttons("reset")
    else:
        messagebox.showwarning("Input Error", "Semua field harus diisi!")

def delete_data():
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Pilih data yang ingin dihapus.")
        return
    
    selected_item = selected_item[0]
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE nama = ? AND email = ? AND password = ?",
                   (treeview.item(selected_item, 'values')[0], 
                    treeview.item(selected_item, 'values')[1], 
                    treeview.item(selected_item, 'values')[2]))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Data berhasil dihapus!")
    load_data()
    clear_inputs()
    toggle_buttons("reset")

def search_data():
    query = entry_search.get()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE nama LIKE ?", ('%' + query + '%',))
    rows = cursor.fetchall()
    conn.close()
    
    for row in treeview.get_children():
        treeview.delete(row)
    
    for row in rows:
        treeview.insert('', 'end', values=(row[1], row[2], row[3]))

def load_data():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.close()
    
    for row in treeview.get_children():
        treeview.delete(row)
    
    for row in rows:
        treeview.insert('', 'end', values=(row[1], row[2], row[3]))

def clear_inputs():
    entry_nama.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_password.delete(0, tk.END)

def toggle_buttons(state):
    if state == "reset":
        btn_add.config(state=tk.NORMAL)
        btn_update.config(state=tk.DISABLED)
        btn_delete.config(state=tk.DISABLED)
    elif state == "update":
        btn_add.config(state=tk.DISABLED)
        btn_update.config(state=tk.NORMAL)
        btn_delete.config(state=tk.NORMAL)

def on_select(event):
    selected_item = treeview.selection()
    if selected_item:
        selected_data = treeview.item(selected_item[0])['values']
        entry_nama.delete(0, tk.END)
        entry_nama.insert(0, selected_data[0])
        entry_email.delete(0, tk.END)
        entry_email.insert(0, selected_data[1])
        entry_password.delete(0, tk.END)
        entry_password.insert(0, selected_data[2])
        toggle_buttons("update")
    else:
        toggle_buttons("reset")

def validate_login():
    email = entry_login_email.get()
    password = entry_login_password.get()

    valid_email = "fadhil@gmail.com"
    valid_password = "admin123"

    if email == valid_email and password == valid_password:
        messagebox.showinfo("Login Success", "Login berhasil!")
        login_window.destroy()
        open_data_window(email) 
    else:
        messagebox.showerror("Login Failed", "Email atau Password salah!")

def open_data_window(user_email):
    global entry_nama, entry_email, entry_password, treeview, entry_search, btn_add, btn_update, btn_delete
    
    root = tk.Tk()
    root.title("Pengelolaan Data Pengguna")
    root.geometry("900x700")
    root.configure(bg='#87CEFA')

    input_frame = tk.Frame(root, bg='#87CEFA')
    input_frame.pack(pady=20)

    label_nama = tk.Label(input_frame, text="Nama", font=("Arial", 12), bg='#87CEFA')
    label_nama.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    entry_nama = tk.Entry(input_frame, font=("Arial", 14), width=30)
    entry_nama.grid(row=0, column=1, padx=10, pady=10)

    label_email = tk.Label(input_frame, text="Email", font=("Arial", 12), bg='#87CEFA')
    label_email.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    entry_email = tk.Entry(input_frame, font=("Arial", 14), width=30)
    entry_email.grid(row=1, column=1, padx=10, pady=10)

    label_password = tk.Label(input_frame, text="Password", font=("Arial", 12), bg='#87CEFA')
    label_password.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    entry_password = tk.Entry(input_frame, font=("Arial", 14), show="*", width=30)
    entry_password.grid(row=2, column=1, padx=10, pady=10)

    button_frame = tk.Frame(root, bg='#87CEFA')
    button_frame.pack(pady=10)

    btn_add = tk.Button(button_frame, text="Tambah Data", command=add_data, font=("Arial", 14), width=15, bg='#4CAF50', fg='white')
    btn_add.pack(side=tk.LEFT, padx=5)

    btn_update = tk.Button(button_frame, text="Ubah Data", command=update_data, font=("Arial", 14), width=15, bg='#2196F3', fg='white', state=tk.DISABLED)
    btn_update.pack(side=tk.LEFT, padx=5)

    btn_delete = tk.Button(button_frame, text="Hapus Data", command=delete_data, font=("Arial", 14), width=15, bg='#F44336', fg='white', state=tk.DISABLED)
    btn_delete.pack(side=tk.LEFT, padx=5)

    search_frame = tk.Frame(root, bg='#e0f7fa')
    search_frame.pack(pady=10)

    label_search = tk.Label(search_frame, text="Cari Nama", font=("Arial", 12), bg='#e0f7fa')
    label_search.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    entry_search = tk.Entry(search_frame, font=("Arial", 14), width=20)
    entry_search.grid(row=0, column=1, padx=10, pady=10)

    btn_search = tk.Button(search_frame, text="Cari", command=search_data, font=("Arial", 14), width=10, bg='#FFC107', fg='black')
    btn_search.grid(row=0, column=2, padx=10, pady=10)

    columns = ('Nama', 'Email', 'Password')
    treeview = ttk.Treeview(root, columns=columns, show='headings', height=10)
    treeview.pack(pady=20)

    for col in columns:
        treeview.heading(col, text=col)

    create_table()
    load_data()

    treeview.bind("<<TreeviewSelect>>", on_select)

    logout_frame = tk.Frame(root, bg='#87CEFA')
    logout_frame.pack(fill=tk.X, side=tk.TOP)
    
    label_welcome = tk.Label(logout_frame, text=f"Email: {user_email}", font=("Arial", 12), bg='#87CEFA', anchor='e', width=30)
    label_welcome.pack(side=tk.TOP, padx=20)

    btn_logout = tk.Button(logout_frame, text="Logout", command=root.quit, font=("Arial", 12), width=10, bg='#F44336', fg='white')
    btn_logout.pack(side=tk.BOTTOM, padx=20)

    root.mainloop()

login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("800x600")
login_window.configure(bg='#87CEFA')

login_frame = tk.Frame(login_window, bg='#87CEFA')
login_frame.pack(pady=40)   

label_login_email = tk.Label(login_frame, text="Email", font=("Arial", 12), bg='#00FFFF')
label_login_email.grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_login_email = tk.Entry(login_frame, font=("Arial", 14), width=30)
entry_login_email.grid(row=0, column=1, padx=10, pady=10)

label_login_password = tk.Label(login_frame, text="Password", font=("Arial", 12), bg='#00CED1')
label_login_password.grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_login_password = tk.Entry(login_frame, font=("Arial", 14), show="*", width=30)
entry_login_password.grid(row=1, column=1, padx=10, pady=10)

btn_login = tk.Button(login_window, text="Login", command=validate_login, font=("Arial", 14), width=15, bg='#4CAF50', fg='white')
btn_login.pack(pady=20)

login_window.mainloop()
