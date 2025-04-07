# import os
# import sqlite3
# import tkinter as tk
# from tkinter import ttk, messagebox

# class DBViewer:
#     def __init__(self, master, db_path, table_name="ContiData"):
#         self.master = master
#         self.master.title("SQLite Database Viewer")
#         self.db_path = db_path
#         self.table_name = table_name

#         # Create a frame to hold the treeview and scrollbar
#         frame = ttk.Frame(master)
#         frame.pack(fill=tk.BOTH, expand=True)

#         # Create the Treeview widget (columns will be determined dynamically)
#         self.tree = ttk.Treeview(frame, show="headings")
#         self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

#         # Create a vertical scrollbar for the treeview
#         scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
#         self.tree.configure(yscrollcommand=scrollbar.set)
#         scrollbar.pack(side=tk.RIGHT, fill="y")

#         self.load_data()

#     def load_data(self):
#         # Check if the database file exists
#         if not os.path.exists(self.db_path):
#             messagebox.showerror("Error", f"Database file not found: {self.db_path}")
#             return

#         # Open the database in read-only mode using a URI
#         uri = f"file:{self.db_path}?mode=ro"
#         try:
#             conn = sqlite3.connect(uri, uri=True)
#         except sqlite3.Error as e:
#             messagebox.showerror("Connection Error", f"Failed to open database:\n{e}")
#             return

#         conn.row_factory = sqlite3.Row
#         cur = conn.cursor()

#         # Retrieve column information dynamically using PRAGMA
#         try:
#             cur.execute(f"PRAGMA table_info({self.table_name});")
#             columns_info = cur.fetchall()
#         except sqlite3.Error as e:
#             messagebox.showerror("Error", f"Failed to retrieve table schema:\n{e}")
#             conn.close()
#             return

#         if not columns_info:
#             messagebox.showerror("Error", f"Table '{self.table_name}' not found in the database.")
#             conn.close()
#             return

#         # Build a list of column names from the schema
#         self.columns = [col["name"] for col in columns_info]
#         self.tree["columns"] = self.columns
#         for col in self.columns:
#             self.tree.heading(col, text=col)
#             self.tree.column(col, width=120, anchor="center")

#         # Retrieve all records from the table
#         try:
#             cur.execute(f"SELECT * FROM {self.table_name};")
#             rows = cur.fetchall()
#         except sqlite3.Error as e:
#             messagebox.showerror("Error", f"Failed to query data:\n{e}")
#             conn.close()
#             return

#         # Insert each row into the Treeview widget
#         for row in rows:
#             values = tuple(row[col] for col in self.columns)
#             self.tree.insert("", tk.END, values=values)

#         conn.close()

# def main():
#     # Change the path as necessary; use a raw string to avoid escape issues.
#     db_path = r"C:\Users\poonams\Documents\Release\continental_data.db"
#     root = tk.Tk()
#     viewer = DBViewer(root, db_path)
#     root.mainloop()

# if __name__ == "__main__":
#     main()



import os
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

class DBViewer:
    def __init__(self, master, db_path, table_name="ContiData"):
        self.master = master
        self.master.title("SQLite Database Viewer")
        self.db_path = db_path
        self.table_name = table_name

        self.setup_style()
        self.create_widgets()
        self.load_data()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.Treeview",
                        background="white",
                        fieldbackground="white",
                        bordercolor="black",
                        borderwidth=1,
                        relief="solid",
                        rowheight=25)
        style.configure("Custom.Treeview.Heading",
                        background="#f0f0f0",
                        foreground="black",
                        borderwidth=1,
                        relief="solid")
        style.map("Custom.Treeview", background=[("selected", "#347083")])
        self.style = style

    def create_widgets(self):
        frame = ttk.Frame(self.master)
        frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(frame, style="Custom.Treeview", show="headings")
        self.tree.grid(row=0, column=0, sticky="nsew")

        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.grid(row=0, column=1, sticky="ns")

        hsb = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=hsb.set)
        hsb.grid(row=1, column=0, sticky="ew")

        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

    def load_data(self):
        if not os.path.exists(self.db_path):
            messagebox.showerror("Error", f"Database file not found: {self.db_path}")
            return

        uri = f"file:{self.db_path}?mode=ro"
        try:
            conn = sqlite3.connect(uri, uri=True)
        except sqlite3.Error as e:
            messagebox.showerror("Connection Error", f"Failed to open database:\n{e}")
            return

        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        try:
            cur.execute(f"PRAGMA table_info({self.table_name});")
            columns_info = cur.fetchall()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to retrieve table schema:\n{e}")
            conn.close()
            return

        if not columns_info:
            messagebox.showerror("Error", f"Table '{self.table_name}' not found in the database.")
            conn.close()
            return

        self.columns = [col["name"] for col in columns_info]
        self.tree["columns"] = self.columns

        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        try:
            cur.execute(f"SELECT * FROM {self.table_name};")
            rows = cur.fetchall()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to query data:\n{e}")
            conn.close()
            return
        for idx, row in enumerate(rows):
            values = tuple(row[col] for col in self.columns)
            self.tree.insert("", tk.END, values=values)
            if idx % 2 == 0:
                self.tree.item(self.tree.get_children()[-1], tags=("even",))
        self.tree.tag_configure("even", background="#f9f9f9")

        conn.close()

def main():
    # Change the path as necessary; use a raw string to avoid escape issues.
    db_path = r"C:\Users\poonams\Documents\Release\continental_data.db"
    root = tk.Tk()
    viewer = DBViewer(root, db_path)
    root.mainloop()

if __name__ == "__main__":
    main()
    
