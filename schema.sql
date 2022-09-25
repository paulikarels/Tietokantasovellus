/*CREATE TABLE visitors (id SERIAL PRIMARY KEY, time TIMESTAMP);
*/

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    admin BOOLEAN,
    username TEXT UNIQUE,
    password TEXT 
);

--credits?
-- INSERT INTO courses (userID, title, credits) VALUES (1, 'Kokkailun perusteet', 2);
-- INSERT INTO courses (userID, title, credits) VALUES (1, 'Advanced laiskottelu', 15);
-- CREATE SEQUENCE id_seq;
-- ALTER TABLE courses ALTER COLUMN id SET DEFAULT nextval('id_seq');
CREATE TABLE  courses (
    id SERIAL PRIMARY KEY,
    userID INTEGER REFERENCES users ON DELETE CASCADE,
    title TEXT UNIQUE,
    credits INTEGER
);

--scores?
CREATE TABLE userEnrollments  (
    id SERIAL PRIMARY KEY,
    courseID INTEGER REFERENCES courses ON DELETE CASCADE,
    userID INTEGER REFERENCES users ON DELETE CASCADE,
    scores INTEGER
);

--acts mainly as a permission handler for creating courses
CREATE TABLE courseInstructors (
    courseID INTEGER REFERENCES courses ON DELETE CASCADE,
    userID INTEGER REFERENCES users ON DELETE CASCADE
);

--exercises/assigments
-- INSERT INTO exercises (courseID, description) VALUES (1, 'Keittaminen');
-- INSERT INTO exercises (courseID, description) VALUES (1, 'Paistaminen');
-- INSERT INTO exercises (courseID, description) VALUES (2, 'Makuuasento');

--consider deleteing DONE
CREATE TABLE exercises (
    id SERIAL PRIMARY KEY,
    courseID INTEGER REFERENCES courses ON DELETE CASCADE,
    description TEXT,
    done BOOLEAN DEFAULT false
    --answer TEXT,
    --correctAnswer TEXT
);
/*
INSERT INTO questions (exercisesID, question, answer) VALUES (1, 'Missa yleensa keitetaan kananmunat?', 'vedessa');
INSERT INTO questions (exercisesID, question, answer) VALUES (1, 'Mika on veden kiehumispiste?', 100);
INSERT INTO questions (exercisesID, question, answer) VALUES (1, 'Tama on vain testi?', 'test');
*/
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    exercisesID INTEGER REFERENCES exercises ON DELETE CASCADE,
    question TEXT,
    answer TEXT
);

/*
INSERT INTO quizzes (questionID, quiz) VALUES (1, 'vedessa');
INSERT INTO quizzes (questionID, quiz) VALUES (1, 'Coca-Colassa');
INSERT INTO quizzes (questionID, quiz) VALUES (1, 'Saippuassa');

INSERT INTO quizzes (questionID, quiz) VALUES (2, 80);
INSERT INTO quizzes (questionID, quiz) VALUES (2, 100);

INSERT INTO quizzes (questionID, quiz) VALUES (3, 'test');
INSERT INTO quizzes (questionID, quiz) VALUES (3, 'no test');
 
*/
CREATE TABLE quizzes (
    id SERIAL PRIMARY KEY,
    questionID INTEGER REFERENCES questions ON DELETE CASCADE,
    quiz TEXT
);

/*
INSERT INTO userQuizAnswers (userID, questionID, quizID, correct) VALUES (1, 1, 1, true); 
INSERT INTO userQuizAnswers (userID, questionID, quizID, correct) VALUES (1, 2, 4, false); 

*/

CREATE TABLE userQuizAnswers (
    userID INTEGER REFERENCES users ON DELETE CASCADE,
    questionID INTEGER REFERENCES questions ON DELETE CASCADE,
    quizID INTEGER REFERENCES quizzes ON DELETE CASCADE,
    correct BOOLEAN
);

/*
SELECT * FROM courseQuestions;
INSERT INTO  courseQuestions (courseID, questionID) VALUES (1, 1);
INSERT INTO  courseQuestions (courseID, questionID) VALUES (1, 2);
 */
 /*
CREATE TABLE courseQuestions (
    courseID INTEGER REFERENCES courses ON DELETE CASCADE,
    questionID INTEGER REFERENCES questions ON DELETE CASCADE
);

/*
SELECT * FROM exerciseQuestions;
INSERT INTO  exerciseQuestions (exerciseID, questionID) VALUES (1, 1);
INSERT INTO  exerciseQuestions (exerciseID, questionID) VALUES (2, 2);
 */
 /*
CREATE TABLE exerciseQuestions (
    exerciseID INTEGER REFERENCES exercises ON DELETE CASCADE,
    questionID INTEGER REFERENCES questions ON DELETE CASCADE
);
*/

/*
CREATE TABLE quiz (
    id SERIAL PRIMARY KEY,
    question TEXT
);
*/