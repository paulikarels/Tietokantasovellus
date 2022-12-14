CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    admin BOOLEAN,
    username TEXT UNIQUE,
    password TEXT 
);


CREATE TABLE  courses (
    id SERIAL PRIMARY KEY,
    userID INTEGER REFERENCES users ON DELETE CASCADE,
    title TEXT UNIQUE,
    credits INTEGER
);


CREATE TABLE userEnrollments  (
    id SERIAL PRIMARY KEY,
    courseID INTEGER REFERENCES courses ON DELETE CASCADE,
    userID INTEGER REFERENCES users ON DELETE CASCADE,
    scores INTEGER
);

CREATE TABLE exercises (
    id SERIAL PRIMARY KEY,
    courseID INTEGER REFERENCES courses ON DELETE CASCADE,
    description TEXT,
    done BOOLEAN DEFAULT false
);

CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    exercisesID INTEGER REFERENCES exercises ON DELETE CASCADE,
    question TEXT,
    answer TEXT
);


CREATE TABLE quizzes (
    id SERIAL PRIMARY KEY,
    questionID INTEGER REFERENCES questions ON DELETE CASCADE,
    quiz TEXT
);

CREATE TABLE userQuizAnswers (
    userID INTEGER REFERENCES users ON DELETE CASCADE,
    courseID INTEGER REFERENCES courses ON DELETE CASCADE,
    questionID INTEGER REFERENCES questions ON DELETE CASCADE,
    quizID INTEGER REFERENCES quizzes ON DELETE CASCADE,
    correct BOOLEAN
);
