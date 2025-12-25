import sqlite3
print("Creating professional Child Vaccination Database...")

conn = sqlite3.connect('child_vacc.db')
c = conn.cursor()

# Drop existing tables
c.execute('DROP TABLE IF EXISTS vaccination_history')
c.execute('DROP TABLE IF EXISTS appointments')
c.execute('DROP TABLE IF EXISTS vaccines')
c.execute('DROP TABLE IF EXISTS children')

# Professional Children Table
c.execute('''CREATE TABLE children 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              name TEXT NOT NULL, aadhaar TEXT UNIQUE NOT NULL, dob TEXT NOT NULL, 
              parent_name TEXT NOT NULL, parent_email TEXT, parent_phone TEXT NOT NULL,
              address TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              status TEXT DEFAULT 'active')''')

# India NIS 2025 Vaccines (Complete Schedule)
c.execute('''CREATE TABLE vaccines 
             (id INTEGER PRIMARY KEY, name TEXT UNIQUE, age_weeks INTEGER, 
              description TEXT, mandatory INTEGER DEFAULT 1)''')

vaccines_data = [
    (1, 'BCG', 0, 'Bacille Calmette-Guerin (Tuberculosis)', 1),
    (2, 'OPV-0', 0, 'Oral Polio Vaccine Birth Dose', 1),
    (3, 'Hepatitis B - Birth', 0, 'Hepatitis B Birth Dose', 1),
    (4, 'Pentavalent-1 (DPT+Hib+HepB)', 6, '6 weeks Primary Dose 1', 1),
    (5, 'IPV-1', 6, 'Inactivated Polio Vaccine Dose 1', 1),
    (6, 'Rotavirus-1', 6, 'Rotavirus Vaccine Dose 1', 1),
    (7, 'PCV-1', 6, 'Pneumococcal Conjugate Vaccine Dose 1', 1),
    (8, 'Pentavalent-2', 10, '6 weeks Primary Dose 2', 1),
    (9, 'Rotavirus-2', 10, 'Rotavirus Vaccine Dose 2', 1),
    (10, 'PCV-2', 14, 'Pneumococcal Dose 2', 1),
    (11, 'Pentavalent-3', 14, '6 weeks Primary Dose 3', 1),
    (12, 'IPV-2', 14, 'Inactivated Polio Vaccine Dose 2', 1),
    (13, 'MR-1', 39, 'Measles Rubella Vaccine 9 months', 1),
    (14, 'JE-1', 39, 'Japanese Encephalitis Dose 1', 0),
    (15, 'Vitamin A -1', 52, 'Vitamin A Dose 1 (52 weeks)', 1),
    (16, 'DPT Booster-1', 78, 'DPT Booster 18 months', 1),
    (17, 'MR-2', 78, 'Measles Rubella Dose 2', 1),
    (18, 'JE-2', 78, 'Japanese Encephalitis Dose 2', 0),
    (19, 'Vitamin A -2', 104, 'Vitamin A Dose 2 (2 years)', 1)
]
c.executemany('INSERT INTO vaccines VALUES (?,?,?,?,?)', vaccines_data)

# Appointments Table
c.execute('''CREATE TABLE appointments 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, child_id INTEGER, 
              vaccine_id INTEGER, scheduled_date TEXT, status TEXT DEFAULT 'pending',
              notes TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              FOREIGN KEY(child_id) REFERENCES children(id),
              FOREIGN KEY(vaccine_id) REFERENCES vaccines(id))''')

# Vaccination History
c.execute('''CREATE TABLE vaccination_history 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, child_id INTEGER, 
              vaccine_id INTEGER, vaccinated_date TEXT, batch_no TEXT,
              next_due TEXT, FOREIGN KEY(child_id) REFERENCES children(id),
              FOREIGN KEY(vaccine_id) REFERENCES vaccines(id))''')

conn.commit()
print("SUCCESS! Professional database created with 19 India NIS 2025 vaccines.")
print("Database file: child_vacc.db")
conn.close()
