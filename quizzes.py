from db import db

def add_quiz(q_id, quiz):
    sql = "INSERT INTO quizzes (questionID, quiz) VALUES (:questionID, :quiz)"
    db.session.execute(sql,  {"questionID":q_id, "quiz":quiz})
    db.session.commit()

def exercise_quizzes(q_id):
    sql = "SELECT * FROM quizzes"
    return db.session.execute(sql, {"questionID": q_id}).fetchall()

def exerciseID_for_answer(q_id):
    sql = "SELECT * FROM quizzes WHERE questionID=:questionID"
    return db.session.execute(sql, {"questionID": q_id}).fetchall()

