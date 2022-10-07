from app import app
import users
import courses
import exercises
import questions
import quizzes
from flask import render_template, redirect, request, session, flash

def error(message, destination):
    flash(message)
    return redirect(destination)

@app.route('/')
def index():
    return render_template("index.html", username=users.username())

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return error("Väärä tunnus tai salasana", "login")
            #return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        admin = request.form["admin_rights"]

        #return render_template("register.html", admin=eval(admin))
        if len(username) < 4:
            return error("Käyttäjänimi liian lyhyt", "register")

        if len(password) < 4:
            return error("Salasana liian lyhyt", "register")


        if users.register(username, password, eval(admin)):
            return redirect("/")
        else:
            return error("Rekisteröinti ei onnistunut, käyttäjä on jo olemassa", "register")

@app.route('/logout')
def logout():
    users.logout()
    return redirect('/')

@app.route('/newCourse', methods=["GET", "POST"])
def add_course():
    if request.method == "POST":
        title = request.form["title"]
        op = request.form["op"]
        
        userID = session.get("user_id", -1)
        admin = users.get_admin_status()
        test = courses.add_course(userID, title, op)
        #return render_template("newCourse.html", courses=test, admin=admin)
        return redirect("/course/"+str(test[0]))
        #return redirect("/course/"+str(1))
    if request.method == "GET":
        admin = users.get_admin_status()
        return render_template("newCourse.html", admin=admin)

@app.route('/newQuiz/<int:id>', methods=["GET", "POST"])
def add_Quiz(id):
    if request.method == "POST":
        question = request.form["question"]
        answer = request.form["answer"]
        
        quiz1 = request.form["quiz1"]
        quiz2 = request.form["quiz2"]
        quiz3 = request.form.get('quiz3')

        checkA = [quiz1, quiz2, quiz3]
          
        if (answer not in checkA):
            return error("Ei oikeaa vastausta valinnoissa!", '/newQuiz/'+str(id))

        questions.add_question(id, question, answer)
        q_id = questions.get_id(id)[-1][0]
        quizzes.add_quiz(q_id, quiz1)
        quizzes.add_quiz(q_id, quiz2)
        if ( quiz3 ):
            quizzes.add_quiz(q_id, quiz3)


        courseID = exercises.get_course_id(id)[0][0]
        admin = users.get_admin_status()
        return redirect('/course/' + str(courseID))
        return render_template(
            "newQuiz.html", admin=admin, question=question, answer=answer, quiz1=quiz1, quiz2=quiz2, quiz3=quiz3, q_id=q_id
        )
    if request.method == "GET":
        admin = users.get_admin_status()
        return render_template(
            "newQuiz.html", admin=admin
        )

# POST maybe later.
@app.route('/courses', methods=["GET", "POST"])
def allcourses():
    if request.method == "POST":
        allcourses = courses.get_all()
        return render_template("courses.html", courses=allcourses)
    if request.method == "GET":
        allcourses = courses.get_all()
        return render_template("courses.html", courses=allcourses)

#https://stackoverflow.com/questions/6320113/how-to-prevent-form-resubmission-when-page-is-refreshed-f5-ctrlr
#https://en.wikipedia.org/wiki/Post/Redirect/Get
# will reconstruct/clean later
@app.route('/course/<int:id>', methods=["GET", "POST"])
def course(id):

    if request.method == "POST":
            
        if ( "description" in request.form  ):
            addedExercise = request.form["description"]
            courseID = courses.id_taken(id)[0]

            exercises.add_exercise(int(courseID), addedExercise)

            course = courses.get_course(id)
            exercise = exercises.course_exercise(id)
            e_id = exercise[0][0]
            question = questions.get_all()
            #quizObject = str(request.form['quizValue'].replace("(", "").replace(")", "").replace("'", "")).rsplit(", ")
 
            #not working properly 24.9 -- post
            userID = session.get("user_id", -1)
            test6 = questions.userQuizData(userID)
            getQuestionID = questions.testingQuest(userID)
            UserAnswers = questions.userQuizResultCheck(userID)
            admin = users.get_admin_status()
            test8 = UserAnswers



            quiz = quizzes.exercise_quizzes(id)

            idddd = courseID
            

            #return redirect("/")
            return render_template(
                "course.html", title=course[2], credits=course[3],
                exercises=exercise, questions=question, 
                quizzes=quiz, id=str(id), test6=test6, getQuestionID=getQuestionID, admin=admin, course=course, userID=userID, addedExercise=addedExercise, idddd=idddd
            )

        else:
            course = courses.get_course(id)
            exercise = exercises.course_exercise(id)
            e_id = exercise[0][0]
            question = questions.get_all()
            #exerciseQuestions = questions.course_questions()
            quiz = quizzes.exercise_quizzes(id)
            userID = session.get("user_id", -1)
            test3 = request.form.getlist('quizValue')

            #test4 = questions.correct_answer_check((test3))

            quizObject = str(request.form['quizValue'].replace("(", "").replace(")", "").replace("'", "")).rsplit(", ")

            #not working properly 24.9 -- get
            answer = questions.correct_answer_check(quizObject[2])
            questions.addUserQuestionQuiz(userID, quizObject[1], quizObject[0], answer)


            test6 = questions.userQuizData(userID)
            getQuestionID = questions.testingQuest(userID)
            #test6 = questions.userQuizResultCheck(userID)


        return render_template(
            "course.html", title=course[2], credits=course[3],
            exercises=exercise, questions=question,
            quizzes=quiz, id=str(id),  test2=userID, test3=test3, quizAnswer=answer, test6=test6, getQuestionID=getQuestionID, userID=userID, course=course
        )


    if request.method == "GET":
        #if courses.is_id_taken(id):
        course = courses.get_course(id)
        exercise = exercises.course_exercise(id)

        #question = questions.exercise_questions(e_id)
        question = questions.get_all()
        questionE_id = questions.get_all_exerciseIds()

        #quizObject = str(request.form['quizValue'].replace("(", "").replace(")", "").replace("'", "")).rsplit(", ")


        #not working properly 24.9 -- post
        userID = session.get("user_id", -1)
        test6 = questions.userQuizData(userID)
        getQuestionID = questions.testingQuest(userID)
        UserAnswers = questions.userQuizResultCheck(userID)
        admin = users.get_admin_status()
        test8 = UserAnswers



        quiz = quizzes.exercise_quizzes(id)

        return render_template(
            "course.html", title=course[2], credits=course[3],
            exercises=exercise, questions=question, 
            quizzes=quiz, id=str(id), test6=test6, getQuestionID=getQuestionID, test8=test8, admin=admin, course=course, userID=userID, questionE_id = questionE_id
        )
