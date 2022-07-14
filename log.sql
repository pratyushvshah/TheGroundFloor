CREATE TABLE users(
    ID SERIAL PRIMARY KEY,
    Fullname TEXT NOT NULL,
    Email TEXT NOT NULL,
    Username TEXT NOT NULL,
    Password TEXT NOT NULL,
    Salt TEXT NOT NULL
);

CREATE TABLE chatfriends(
    Username TEXT NOT NULL,
    Friends TEXT DEFAULT NULL,
    Requests TEXT DEFAULT NULL
);

CREATE TABLE chatmessages(
    ID  SERIAL PRIMARY KEY,
    Sender TEXT NOT NULL,
    Receiver TEXT NOT NULL,
    Message TEXT NOT NULL,
    Read INTEGER DEFAULT 0,
    Print INTEGER DEFAULT 0,
    Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chatsettings(
    Username TEXT NOT NULL,
    NumMessages INT DEFAULT 10
);