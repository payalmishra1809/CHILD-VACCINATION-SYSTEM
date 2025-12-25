import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import qrcode
from PIL import Image, ImageTk
import re

class ProfessionalVaccinationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Child Vaccination Management System - India NIS 2025")
        self.root.geometry("1300x850")
        self.root.configure(bg='#f8f9fa')
        self.root.resizable(True, True)
        
        self.conn = sqlite3.connect('child_vacc.db')
        self.c = self.conn.cursor()
        self.entries = {}
        self.create_modern_ui()
        self.refresh_all()
    
    def create_modern_ui(self):
        # Modern style configuration
        style = ttk.Style()
        style.theme_use('clam')
        
        # Custom styles for invisible borders + modern look
        style.configure('Clean.TNotebook', background='#f8f9fa', borderwidth=0)
        style.configure('Clean.TNotebook.Tab', padding=[30,15], font=('Segoe UI', 12, 'bold'),
                       background='#e9ecef', foreground='#495057')
        style.map('Clean.TNotebook.Tab',
                 background=[('selected', '#ffffff'), ('active', '#dee2e6')],
                 foreground=[('selected', '#212529'), ('active', "#506377")])
        
        style.configure('Card.TFrame', background='white', relief='flat', borderwidth=1)
        style.configure('Header.TLabel', font=('Segoe UI', 18, 'bold'), background='#f8f9fa', foreground='#2c3e50')
        style.configure('SubHeader.TLabel', font=('Segoe UI', 14, 'bold'), background='#f8f9fa', foreground='#34495e')
        style.configure('Clean.Treeview', background='white', fieldbackground='white', borderwidth=0, font=('Segoe UI', 10))
        style.configure('Clean.Treeview.Heading', font=('Segoe UI', 11, 'bold'), background='#495057', foreground='white')
        
        # Header Section
        self.create_header()
        
        # Main content area
        self.notebook = ttk.Notebook(self.root, style='Clean.TNotebook')
        self.notebook.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.setup_tabs()
    
    def create_header(self):
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill='x', pady=(0,10))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="👩‍⚕️ Child Vaccination Management System", 
                              bg='#2c3e50', fg='white', font=('Segoe UI', 20, 'bold'))
        title_label.pack(side='left', padx=30, pady=20)
        
        subtitle_label = tk.Label(header_frame, text="India National Immunization Schedule 2025 | Ministry of Health Compliant", 
                                 bg='#2c3e50', fg='#bdc3c7', font=('Segoe UI', 11))
        subtitle_label.pack(side='left', padx=20, pady=25)
    
    def setup_tabs(self):
        self.create_register_tab()
        self.create_dashboard_tab()
        self.create_schedule_tab()
        self.create_reports_tab()
    
    def create_card_frame(self, parent, title=""):
        """Creates modern card-style frame"""
        card = tk.Frame(parent, bg='white', relief='flat', bd=0)
        card.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Card header
        if title:
            header = tk.Frame(card, bg='#ecf0f1', height=50)
            header.pack(fill='x')
            header.pack_propagate(False)
            tk.Label(header, text=title, bg='#ecf0f1', fg='#2c3e50', 
                    font=('Segoe UI', 14, 'bold'), pady=15).pack(side='left', padx=25)
        
        # Card content
        content = tk.Frame(card, bg='white')
        content.pack(fill='both', expand=True, padx=25, pady=25)
        return content
    
    def create_register_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='👶 Child Registration')
        
        content = self.create_card_frame(frame, "Register New Child")
        
        # Two column layout
        main_row = tk.Frame(content, bg='white')
        main_row.pack(fill='both', expand=True)
        
        # Left column - Child info
        left_col = tk.Frame(main_row, bg='white')
        left_col.pack(side='left', fill='both', expand=True, padx=(0,15))
        
        tk.Label(left_col, text="Child Information", bg='white', 
                font=('Segoe UI', 13, 'bold'), fg='#34495e').pack(anchor='w', pady=(0,15))
        
        fields_left = [
            ("Child Full Name *", "child_full_name"),
            ("Aadhaar Number (12 digits) *", "aadhaar_number_12_digits"), 
            ("Date of Birth (YYYY-MM-DD) *", "date_of_birth_yyyy_mm_dd")
        ]
        
        for label_text, key in fields_left:
            tk.Label(left_col, text=label_text, bg='white', font=('Segoe UI', 10, 'bold'), 
                    fg='#5a6c7d').pack(anchor='w', pady=(0,8))
            entry = tk.Entry(left_col, font=('Segoe UI', 11), width=28, relief='flat', 
                           bd=1, bg='#f8f9fa', highlightthickness=1, highlightcolor='#3498db')
            entry.pack(fill='x', pady=(2,15))
            self.entries[key] = entry
        
        # Right column - Parent info
        right_col = tk.Frame(main_row, bg='white')
        right_col.pack(side='right', fill='both', expand=True, padx=(15,0))
        
        tk.Label(right_col, text="Parent/Guardian Information", bg='white', 
                font=('Segoe UI', 13, 'bold'), fg='#34495e').pack(anchor='w', pady=(0,15))
        
        fields_right = [
            ("Parent/Guardian Name *", "parent_guardian_name"),
            ("Parent Email", "parent_email"),
            ("Parent Mobile *", "parent_mobile"),
            ("Full Address", "full_address")
        ]
        
        for label_text, key in fields_right:
            tk.Label(right_col, text=label_text, bg='white', font=('Segoe UI', 10, 'bold'), 
                    fg='#5a6c7d').pack(anchor='w', pady=(0,8))
            entry = tk.Entry(right_col, font=('Segoe UI', 11), width=28, relief='flat', 
                           bd=1, bg='#f8f9fa', highlightthickness=1, highlightcolor='#3498db')
            entry.pack(fill='x', pady=(2,15))
            self.entries[key] = entry
        
        # Action buttons
        btn_frame = tk.Frame(content, bg='white')
        btn_frame.pack(pady=(0,20))
        tk.Button(btn_frame, text="✅ Register Child", bg='#27ae60', fg='white', 
                 font=('Segoe UI', 12, 'bold'), width=16, height=2, relief='flat', 
                 bd=0, cursor='hand2', command=self.register_child).pack(side='left', padx=10)
        tk.Button(btn_frame, text="🔄 Clear Form", bg='#95a5a6', fg='white', 
                 font=('Segoe UI', 12, 'bold'), width=14, height=2, relief='flat', 
                 bd=0, cursor='hand2', command=self.clear_entries).pack(side='left', padx=10)
    
    def create_dashboard_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='📊 Dashboard')
        
        content = self.create_card_frame(frame, "Vaccination Dashboard")
        
        # Stats cards
        stats_row = tk.Frame(content, bg='white')
        stats_row.pack(fill='x', pady=(0,25))
        
        total_card = tk.Frame(stats_row, bg='#3498db', width=200, height=80)
        total_card.pack(side='left', padx=15, pady=10)
        total_card.pack_propagate(False)
        tk.Label(total_card, text="Total Children", bg='#3498db', fg='white', 
                font=('Segoe UI', 11, 'bold')).pack(pady=(15,0))
        self.total_children_label = tk.Label(total_card, text="0", bg='#3498db', fg='white', 
                                           font=('Segoe UI', 24, 'bold'))
        self.total_children_label.place(relx=0.5, rely=0.65, anchor='center')
        
        overdue_card = tk.Frame(stats_row, bg='#e74c3c', width=200, height=80)
        overdue_card.pack(side='left', padx=15, pady=10)
        overdue_card.pack_propagate(False)
        tk.Label(overdue_card, text="Overdue Vaccines", bg='#e74c3c', fg='white', 
                font=('Segoe UI', 11, 'bold')).pack(pady=(15,0))
        self.overdue_label = tk.Label(overdue_card, text="0", bg='#e74c3c', fg='white', 
                                    font=('Segoe UI', 24, 'bold'))
        self.overdue_label.place(relx=0.5, rely=0.65, anchor='center')
        
        # Data table
        table_frame = tk.Frame(content, bg='white')
        table_frame.pack(fill='both', expand=True)
        
        columns = ('ID', 'Child Name', 'Age(Months)', 'Due Vaccines', 'Status', 'Last Updated')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=18, style='Clean.Treeview')
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Action buttons
        btn_frame = tk.Frame(content, bg='white')
        btn_frame.pack(pady=(15,0))
        tk.Button(btn_frame, text="🔄 Refresh Dashboard", bg='#3498db', fg='white', 
                 font=('Segoe UI', 11, 'bold'), width=18, relief='flat', bd=0, 
                 cursor='hand2', command=self.refresh_dashboard).pack(side='left', padx=10)
        tk.Button(btn_frame, text="📈 Analytics", bg='#9b59b6', fg='white', 
                 font=('Segoe UI', 11, 'bold'), width=14, relief='flat', bd=0, 
                 cursor='hand2', command=self.show_analytics).pack(side='left', padx=10)
    
    def create_schedule_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='💉 Vaccination Schedule')
        
        content = self.create_card_frame(frame, "Schedule & Reminders")
        
        # Selection
        sel_frame = tk.Frame(content, bg='white')
        sel_frame.pack(fill='x', pady=(0,25))
        tk.Label(sel_frame, text="Select Child:", bg='white', font=('Segoe UI', 12, 'bold'), 
                fg='#34495e').pack(side='left', pady=15)
        
        self.child_combo = ttk.Combobox(sel_frame, font=('Segoe UI', 11), width=50, state='readonly')
        self.child_combo.pack(side='left', padx=(15,0), pady=12)
        
        tk.Button(sel_frame, text="📋 Show Schedule", bg='#27ae60', fg='white', 
                 font=('Segoe UI', 11, 'bold'), width=16, relief='flat', bd=0, 
                 cursor='hand2', command=self.show_detailed_schedule).pack(side='left', padx=15, pady=12)
        
        # Schedule display
        self.schedule_text = tk.Text(content, height=22, font=('Consolas', 11), 
                                   bg='#f8f9fa', fg='#2c3e50', relief='flat', bd=1,
                                   wrap='word', state='normal')
        self.schedule_text.pack(fill='both', expand=True, pady=(0,10))
    
    def create_reports_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='📄 Reports & Records')
        
        content = self.create_card_frame(frame, "Generate Professional Reports")
        
        sel_frame = tk.Frame(content, bg='white')
        sel_frame.pack(fill='x', pady=(0,25))
        tk.Label(sel_frame, text="Select Child for Report:", bg='white', 
                font=('Segoe UI', 12, 'bold'), fg='#34495e').pack(side='left', pady=15)
        
        self.report_combo = ttk.Combobox(sel_frame, font=('Segoe UI', 11), width=50, state='readonly')
        self.report_combo.pack(side='left', padx=(15,0), pady=12)
        
        # Buttons
        btn_frame = tk.Frame(content, bg='white')
        btn_frame.pack(pady=(0,20))
        tk.Button(btn_frame, text="📄 PDF Report", bg='#e74c3c', fg='white', 
                 font=('Segoe UI', 12, 'bold'), width=16, relief='flat', bd=0, 
                 cursor='hand2', command=self.generate_professional_pdf).pack(side='left', padx=12)
        tk.Button(btn_frame, text="🔗 QR Record", bg='#9b59b6', fg='white', 
                 font=('Segoe UI', 12, 'bold'), width=14, relief='flat', bd=0, 
                 cursor='hand2', command=self.generate_qr_record).pack(side='left', padx=12)
    
    # [Keep all previous methods: register_child, refresh_dashboard, show_analytics, etc. - they're the same]
    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def register_child(self):
        try:
            required = ['child_full_name', 'aadhaar_number_12_digits', 'date_of_birth_yyyy_mm_dd', 
                       'parent_guardian_name', 'parent_mobile']
            data = {k: self.entries[k].get().strip() for k in self.entries}
            
            if not all(data[field] for field in required):
                raise ValueError("Please fill all REQUIRED fields marked with *")
            
            if len(data['aadhaar_number_12_digits']) != 12 or not data['aadhaar_number_12_digits'].isdigit():
                raise ValueError("Aadhaar must be exactly 12 digits")
            
            self.c.execute('''INSERT INTO children (name, aadhaar, dob, parent_name, parent_email, 
                             parent_phone, address) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                          (data['child_full_name'], data['aadhaar_number_12_digits'], 
                           data['date_of_birth_yyyy_mm_dd'], data['parent_guardian_name'],
                           data.get('parent_email'), data['parent_mobile'], data['full_address']))
            self.conn.commit()
            
            messagebox.showinfo("SUCCESS", f"Child '{data['child_full_name']}' registered successfully!")
            self.clear_entries()
            self.refresh_all()
            
        except sqlite3.IntegrityError:
            messagebox.showerror("ERROR", "Aadhaar number already exists!")
        except ValueError as ve:
            messagebox.showerror("VALIDATION ERROR", str(ve))
        except Exception as e:
            messagebox.showerror("ERROR", f"Registration failed: {str(e)}")
    
    def clear_entries(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
    
    def refresh_all(self):
        self.refresh_dashboard()
        self.load_combos()
    
    def load_combos(self):
        self.c.execute("SELECT id, name FROM children ORDER BY name")
        children = [f"ID:{r[0]} - {r[1]}" for r in self.c.fetchall()]
        if hasattr(self, 'child_combo'):
            self.child_combo['values'] = children
        if hasattr(self, 'report_combo'):
            self.report_combo['values'] = children
    
    def refresh_dashboard(self):
        self.tree.delete(*self.tree.get_children())
        self.c.execute("SELECT id, name, dob FROM children ORDER BY name")
        children = self.c.fetchall()
        
        total = len(children)
        overdue_count = 0
        
        for child in children:
            child_id, name, dob = child
            age_months = (datetime.now() - datetime.strptime(dob, '%Y-%m-%d')).days // 30
            due_vaccines = self.get_due_vaccines(dob)
            
            status = "OVERDUE" if due_vaccines else "UP-TO-DATE"
            if "OVERDUE" in status: overdue_count += 1
            
            last_updated = datetime.now().strftime("%Y-%m-%d")
            self.tree.insert('', 'end', values=(child_id, name, age_months, len(due_vaccines), status, last_updated))
        
        self.total_children_label.config(text=str(total))
        self.overdue_label.config(text=str(overdue_count))
    
    def get_due_vaccines(self, dob_str):
        dob = datetime.strptime(dob_str, '%Y-%m-%d')
        age_weeks = (datetime.now() - dob).days // 7
        self.c.execute("SELECT name FROM vaccines WHERE age_weeks <= ?", (age_weeks,))
        return [r[0] for r in self.c.fetchall()]
    
    def show_detailed_schedule(self):
        sel = self.child_combo.get()
        if not sel: 
            messagebox.showwarning("Warning", "Select child first!")
            return
        
        child_id = int(sel.split('-')[0].split(':')[1])
        self.c.execute("SELECT dob FROM children WHERE id=?", (child_id,))
        dob = self.c.fetchone()[0]
        due_vaccines = self.get_due_vaccines(dob)
        
        self.schedule_text.delete(1.0, tk.END)
        self.schedule_text.insert(tk.END, f"DUE VACCINES for child ID {child_id}:\n\n")
        for v in due_vaccines:
            self.schedule_text.insert(tk.END, f"• {v}\n")
        if not due_vaccines:
            self.schedule_text.insert(tk.END, "All vaccines up-to-date!")
    
    def show_analytics(self):
        self.c.execute("SELECT name, dob FROM children")
        data = self.c.fetchall()
        if not data:
            messagebox.showwarning("Warning", "No children data!")
            return
        
        names, dobs = zip(*data)
        ages = [(datetime.now() - datetime.strptime(dob, '%Y-%m-%d')).days // 30 for dob in dobs]
        
        fig, ax = plt.subplots(figsize=(12,6))
        ax.bar(names, ages, color='#3498db')
        ax.set_title('Children Ages & Vaccination Status', fontsize=16, fontweight='bold')
        ax.set_ylabel('Age (Months)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        chart_win = tk.Toplevel(self.root)
        chart_win.title("Vaccination Analytics")
        chart_win.geometry("900x600")
        canvas = FigureCanvasTkAgg(fig, chart_win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def generate_professional_pdf(self):
        sel = self.report_combo.get()
        if not sel: 
            messagebox.showwarning("Warning", "Select child!")
            return
        
        child_id = int(sel.split('-')[0].split(':')[1])
        self.c.execute("SELECT * FROM children WHERE id=?", (child_id,))
        child = self.c.fetchone()
        
        filename = f"REPORT_{child[1].replace(' ','_')}.pdf"
        p = canvas.Canvas(filename, pagesize=letter)
        p.setFont("Helvetica-Bold", 20)
        p.drawString(50, 750, "VACCINATION REPORT")
        p.setFont("Helvetica-Bold", 16)
        p.drawString(50, 720, f"Child: {child[1]}")
        p.setFont("Helvetica", 12)
        p.drawString(50, 690, f"Aadhaar: {child[2]} | DOB: {child[3]}")
        p.drawString(50, 670, f"Parent: {child[4]} | Phone: {child[6]}")
        p.save()
        
        messagebox.showinfo("Success", f"PDF saved: {filename}")
    
    def generate_qr_record(self):
        sel = self.report_combo.get()
        if not sel: 
            messagebox.showwarning("Warning", "Select child!")
            return
        
        child_id = int(sel.split('-')[0].split(':')[1])
        self.c.execute("SELECT name, aadhaar FROM children WHERE id=?", (child_id,))
        data = self.c.fetchone()
        
        qr = qrcode.QRCode(version=1, box_size=15, border=5)
        qr.add_data(f"Child: {data[0]}\nAadhaar: {data[1]}\nVaccination Record")
        qr.make(fit=True)
        img = qr.make_image(fill_color="#3498db", back_color="white")
        filename = f"QR_{data[0].replace(' ','_')}.png"
        img.save(filename)
        
        messagebox.showinfo("Success", f"QR saved: {filename}")
    
    def on_closing(self):
        self.conn.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ProfessionalVaccinationApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
