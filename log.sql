CREATE TABLE users(
    ID SERIAL PRIMARY KEY,
    Fullname TEXT NOT NULL,
    Email TEXT NOT NULL,
    Username TEXT NOT NULL,
    Friends TEXT,
    Requests TEXT,
    Password TEXT NOT NULL,
    Salt TEXT NOT NULL,
    NumMessages INT DEFAULT 10
);

CREATE TABLE messages(
    ID  SERIAL PRIMARY KEY,
    Sender TEXT NOT NULL,
    Receiver TEXT NOT NULL,
    Message TEXT NOT NULL,
    Read INTEGER DEFAULT 0,
    Print INTEGER DEFAULT 0,
    Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
