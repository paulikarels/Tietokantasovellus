from db import db

def get_course(e_id):
    sql = "SELECT * FROM exercises WHERE id=:id"
    result = db.session.execute(sql, {"id": e_id}).fetchall()
    return result[0]

def course_exercise(e_id):
    sql = "SELECT * FROM exercises WHERE courseID=:courseID"
    exercises = db.session.execute(sql, {"courseID": e_id}).fetchall()
    return exercises

def add_exercise(courseID, description):
    sql = "INSERT INTO exercises (courseID, description, done) VALUES (:courseID, :description, 'false')"
    db.session.execute(sql, {"courseID":courseID, "description":description})
    db.session.commit()

def get_course_id(Q_exercisesID):
    sql = "select E.courseid from questions Q, exercises E WHERE  :Q_exercisesID  = E.id LIMIT 1"
    exercises = db.session.execute(sql, {"Q_exercisesID": Q_exercisesID}).fetchall()
    return exercises