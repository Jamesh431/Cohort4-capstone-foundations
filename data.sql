CREATE TABLE IF NOT EXISTS Users (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  full_name TEXT NOT NULL,
  phone TEXT,
  email TEXT NOT NULL UNIQUE,
  hashed_password TEXT,
  user_type TEXT DEFAULT user,
  date_created TEXT,
  hire_date TEXT,
  active INTEGER DEFAULT 1
);


CREATE TABLE IF NOT EXISTS Competency_Assessment_Data (
  comp_name TEXT NOT NULL UNIQUE,
  test_name TEXT,  
  date_created TEXT,
  PRIMARY KEY (comp_name, test_name)
);


CREATE TABLE IF NOT EXISTS Assessment_Results (
  test_id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  full_name TEXT,
  competency TEXT,
  assessment TEXT,
  score INTEGER,
  date_taken TEXT,
  admined_by TEXT,
  admin_id INTEGER,
  best_score INTEGER,

  FOREIGN KEY (user_id)
    REFERENCES Users(user_id),
  FOREIGN KEY (full_name)
    REFERENCES Users(full_name),
  FOREIGN KEY (admined_by)
    REFERENCES Users(user_id),
  FOREIGN KEY (admin_id)
    REFERENCES Users(full_name),
  FOREIGN KEY (competency)
    REFERENCES Competency_Assessment_Data(comp_name),
  FOREIGN KEY (assessment)
    REFERENCES Competency_Assessment_Data(test_name));