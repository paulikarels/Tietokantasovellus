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

@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        admin = request.form["admin_rights"]

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
        if  test == False:
            return error("Kurssinimi on jo olemassa!", "newCourse")

        return redirect("/course/"+str(test[0]))
    if request.method == "GET":
        admin = users.get_admin_status()
        return render_template("newCourse.html", admin=admin)

@app.route('/newQuiz/<int:id>', methods=["GET", "POST"])
def add_Quiz(id):
    if request.method == "POST":
        admin = users.get_admin_status()
        question = request.form["question"]
        answer = request.form["answer"]
        
        quiz1 = request.form["quiz1"]
        quiz2 = request.form["quiz2"]
        quiz3 = request.form.get('quiz3')

        checkA = [quiz1, quiz2, quiz3]
          
        if (answer not in checkA):
            error("Ei oikeaa vastausta valinnoissa!", '/newQuiz/'+str(id))    
            return render_template(
                "newQuiz.html", admin=admin, question=question, answer=answer, quiz1=quiz1, quiz2=quiz2, quiz3=quiz3
            )  

        questions.add_question(id, question, answer)
        q_id = questions.get_id(id)[-1][0]
        quizzes.add_quiz(q_id, quiz1)
        quizzes.add_quiz(q_id, quiz2)
        if ( quiz3 ):
            quizzes.add_quiz(q_id, quiz3)

        courseID = exercises.get_course_id(id)[0][0]
        return redirect('/course/' + str(courseID))

    if request.method == "GET":
        admin = users.get_admin_status()
        return render_template(
            "newQuiz.html", admin=admin
        )

@app.route('/courses', methods=["GET", "POST"])
def allcourses():
    if request.method == "POST":
        allcourses = courses.get_all()
        return render_template("courses.html", courses=allcourses)
    if request.method == "GET":
        allcourses = courses.get_all()
        return render_template("courses.html", courses=allcourses)

@app.route('/myCourses', methods=["GET", "POST"])
def userscourses():
    if request.method == "POST":
        userID = session.get("user_id", -1)
        usercourses = courses.get_user_courses(userID)
        return render_template("myCourses.html", usercourses=usercourses)
    if request.method == "GET":
        userID = session.get("user_id", -1)
        
        enrollments = courses.check_enrollment(userID) 
        if not enrollments:
            enrollments = False

        allcourses = courses.get_all()
        userCreatedCourses = courses.get_user_courses(userID)
        return render_template(
            "myCourses.html", userCreatedCourses=userCreatedCourses, enrollments=enrollments, allcourses=allcourses
        )


@app.route('/myCourse/<int:id>', methods=["GET", "POST"])
def mycourses(id):
    if request.method == "POST":
        courseID = courses.id_taken(id)[0]
        course = courses.get_course(id)
        userID = session.get("user_id", -1)
        value = courses.check_enrollment(userID)
        enrollments = courses.user_enrollments(courseID)

        
        userObject = str(request.form['kickUser'].replace("(", "").replace(")", "").replace("'", "")).rsplit(", ")
        questions.deleteUserQuizData(userObject[2], userObject[1])
        courses.remove_user_enrollment(userObject[2], userObject[1])
        return redirect('/myCourse/' + str(courseID))

    if request.method == "GET":
        courseID = courses.id_taken(id)[0]
        course = courses.get_course(id)
        userID = session.get("user_id", -1)
        enrollments = courses.user_enrollments(courseID)
        return render_template(
            "userCourse.html", course=course, userID=userID, enrollments=enrollments, id=id
        )



    
@app.route('/viewCourse/<int:id>', methods=["GET", "POST"])
def viewCourse(id):
    if request.method == "POST":
        userID = session.get("user_id", -1)

        return render_template("viewCourse.html")
    if request.method == "GET":

        userID = session.get("user_id", -1)

        course = courses.get_course(id)
        exercise = exercises.course_exercise(id)
        res = []
        for exercise in exercise:
            res.append(exercises.get_user_exercise_completions(userID, id, exercise.id))

        courseQuestions = []
        for re in res:
            for question in re:
                courseQuestions.append(question.id)

        testQuestion = questions.userQuizData(userID)

        exerciseAssigns = []

        allUserQuizzes = questions.userQuizData3(userID)

        howManyDone = set(courseQuestions) & set(allUserQuizzes)


        return render_template(
            "viewCourse.html", userID=userID, course=course, 
            testQuestion=testQuestion, exercise=exercise, allUserQuizzes=allUserQuizzes, howManyDone=howManyDone,
            exerciseAssigns=exerciseAssigns, res=res,  courseQuestions=courseQuestions
        )

@app.route('/course/<int:id>', methods=["GET", "POST"])
def course(id):

    if request.method == "POST":
            
        if ( "description" in request.form  ):
            addedExercise = request.form["description"]
            courseID = courses.id_taken(id)[0]

            exercises.add_exercise(int(courseID), addedExercise)

            return redirect("/course/"+str(courseID))

        elif ( "quizValue" in request.form  ):
            courseID = courses.id_taken(id)[0]

             
            exercise = exercises.course_exercise(id)

            userID = session.get("user_id", -1)

            quizObject = str(request.form['quizValue'].replace("(", "").replace(")", "").replace("'", "")).rsplit(", ")

            answer = questions.correct_answer_check(quizObject[2], quizObject[1])
            questions.addUserQuestionQuiz(userID, quizObject[1], quizObject[0], answer, courseID)


            return redirect("/course/"+str(courseID))
        elif ( "joinCourse" in request.form  ) :
            courseID = courses.id_taken(id)[0]
            userID = session.get("user_id", -1)
            courses.enroll_User(courseID,userID)
            return redirect("/course/"+str(courseID))

        else:
            courseID = courses.id_taken(id)[0]
            return error("Jokin meni pieleen!", '/course/'+str(courseID))  

    if request.method == "GET":
        userID = session.get("user_id", -1)
        userEnrollment = courses.check_enrollment(userID)

        course = courses.get_course(id)
        exercise = exercises.course_exercise(id)
        
        question = questions.get_all()
        questionE_id = questions.get_all_exerciseIds()

        test6 = questions.userQuizData(userID)
        getQuestionID = questions.testingQuest(userID)
        admin = users.get_admin_status()
        quiz = quizzes.exercise_quizzes(id)

        return render_template(
            "course.html", title=course[2], credits=course[3],
            exercises=exercise, questions=question, 
            quizzes=quiz, id=str(id), test6=test6, getQuestionID=getQuestionID, 
            admin=admin, course=course, userID=userID, questionE_id = questionE_id,
            userEnrollment=userEnrollment
            
        )
