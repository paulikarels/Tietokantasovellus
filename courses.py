from db import db

def add_course(userID, title, op):
    sql = "INSERT INTO courses (userID, title, credits) VALUES (:userID, :title, :op)"

    #can't take values from inserts/updates because of sqlalchemy v.1.4.2 :)))) 
    #c_id = db.session.execute(sql, {"u_id":u_id, "title":title, "op":op  }).fetchone()[0]
    #    
    
    #sqlQuery = 'SELECT id FROM courses WHERE title=:title ORDER BY id DESC LIMIT 1'
    #c_id = db.session.execute(sqlQuery, {"title": title}).fetchall()



    db.session.execute(sql, {"userID":userID, "title":title, "op":op })
    db.session.commit()

    test = db.session.execute("SELECT id FROM courses ORDER BY id DESC LIMIT 1").fetchone()
    return test

def get_all():
    sql = 'SELECT id, title FROM courses ORDER BY id'
    return db.session.execute(sql).fetchall()

def get_course(c_id):
    sql = "SELECT * FROM courses WHERE id=:id"
    result = db.session.execute(sql, {"id": c_id}).fetchall()
    return result[0]

def id_taken(c_id):
    sql = 'SELECT id FROM courses WHERE id=:id'
    return db.session.execute(sql, {"id": c_id}).fetchall()[-1]
    
def enroll_User(c_id, u_id):
    sql = "INSERT INTO userEnrollments (courseID, userID, scores) VALUES (:courseID, :userID, 0)"
    db.session.execute(sql,  {"courseID":c_id, "userID":u_id})
    db.session.commit()

def check_enrollment(u_id):
    sql = "SELECT courseID FROM userEnrollments WHERE userID =:u_id"
    result = db.session.execute(sql, {"u_id":u_id}).fetchall()
    res = []
    for tes in result:
        res.append(tes[0])

    return res