CREATE TABLE IF NOT EXISTS Users (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  full_name TEXT NOT NULL,
  phone TEXT,
  email TEXT NOT NULL UNIQUE,
  hashed_password TEXT,
  user_type TEXT DEFAULT user,
  date_created TEXT,
  hire_date TEXT,
  active INTEGER DEFAULT True
);


CREATE TABLE IF NOT EXISTS Competency_Assessment_Data (
  comp_id INTEGER PRIMARY KEY AUTOINCREMENT,
  comp_name TEXT NOT NULL,
  test_name TEXT,  
  date_created TEXT,
  UNIQUE (comp_name, test_name)
);


CREATE TABLE IF NOT EXISTS Assessment_Results (
  test_id INTEGER PRIMARY KEY AUTOINCREMENT,
  comp_id INTEGER,
  user_id INTEGER,
  score INTEGER,
  date_taken TEXT,
  admin_id INTEGER,
  best_score INTEGER DEFAULT False,

  FOREIGN KEY (user_id)
    REFERENCES Users(user_id),
  FOREIGN KEY (admin_id)
    REFERENCES Users(user_id),
  FOREIGN KEY (comp_id)
    REFERENCES Competency_Assessment_Data(comp_id));