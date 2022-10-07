from db import db

def get_id(e_id):
    sql = "SELECT id FROM questions WHERE exercisesID=:exercisesID"
    return db.session.execute(sql, {"exercisesID": e_id}).fetchall()

def exercise_questions(q_id):
    sql = "SELECT * FROM questions WHERE exercisesID=:exercisesID"
    return db.session.execute(sql, {"exercisesID": q_id}).fetchall()

def get_all():
    sql = "SELECT * FROM questions "
    return db.session.execute(sql).fetchall()
     
def get_all_exerciseIds():
    sql = "SELECT exercisesid FROM questions"
    return db.session.execute(sql).fetchall()
     
    
def correct_answer_check(q_answer, q_id):
    sql = "SELECT * FROM questions WHERE answer=:q_answer AND id=:q_id"
    result = db.session.execute(sql, {"q_answer": q_answer, "q_id":q_id} ).fetchall()
    if (result):
        return True
    else:
        return False

def add_question(e_id, question, answer):
    sql = "INSERT INTO questions (exercisesID, question, answer) VALUES (:exercisesID, :question, :answer)"
    db.session.execute(sql,  {"exercisesID":e_id, "question":question, "answer":answer})
    db.session.commit()

def course_questions():
    sql = "SELECT * FROM exerciseQuestions"
    return db.session.execute(sql).fetchall()


def addUserQuestionQuiz(u_id, question_id, quiz_id, correct):
    sql = "INSERT INTO userQuizAnswers (userID, questionID, quizID, correct) VALUES (:userid, :questionid, :quizid, :correct)"
    db.session.execute(sql,  {"userid":u_id, "questionid":question_id, "quizid":quiz_id, "correct":correct})
    db.session.commit()
    
def userQuizData(u_id):
    sql = "SELECT * FROM userQuizAnswers WHERE userID=:u_id"
    result = db.session.execute(sql,  {"u_id":u_id}).fetchall()
    if not bool(result): 
          return db.session.execute(sql,  {"u_id":u_id}).fetchall()
    else:
        return result

def userQuizData2(u_id):
    sql = "SELECT * FROM userQuizAnswers WHERE userID=:u_id"
    result = db.session.execute(sql,  {"u_id":u_id}).fetchall()
    if not bool(result): 
        res = []
        for tes in result:
            res.append(tes[0])

        return res
    else:
        res = []
        for tes in result:
            res.append(tes[3])

        return res

    
def userQuizResultCheck(u_id):
    sql = "SELECT correct FROM userQuizAnswers WHERE userID=:u_id"
    return db.session.execute(sql,  {"u_id":u_id}).fetchone()

def testingQuest(u_id):
    sql = "SELECT questionID FROM userQuizAnswers WHERE userID=:u_id"
    result=  db.session.execute(sql,{"u_id":u_id}).fetchall()
    res = []
    for tes in result:
        res.append(tes[0])

    return res


'''
CREATE TABLE userQuizAnswers (
    userID INTEGER REFERENCES users ON DELETE CASCADE,
    questionID INTEGER REFERENCES questions ON DELETE CASCADE,
    quizID INTEGER REFERENCES quizzes ON DELETE CASCADE,
    correct BOOLEAN
);
'''