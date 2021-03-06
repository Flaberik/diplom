import hashlib

from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, current_user, login_required, logout_user

from app import app
from app import oid
from app.forms import *
from app.models import *

# ---------------------------------------------------------------------#
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data, password=md5(form.password.data)).first()

        if user is None:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        session['username'] = form.login.data
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html',user=g.user, title='Sign In', form=form)


# ---------------------------------------------------------------------#

def test(form):
    if form.validate_on_submit():
        group_id = Groups.query.filter_by(group_name=request.form['group_select']).first().id
        teacher_id = Teachers.query.filter_by(teacher_name=request.form['teacher_select']).first().id
        lesson_id = Lessons.query.filter_by(lesson_name=request.form['lesson_select']).first().id
        denom = 0;
        try:
            if (request.form['denom'] == '1'):
                denom = 1;
        except:
            pass
        hash = md5(str(group_id) + str(request.form['day_select']) + str(request.form['pair_select']) + str(denom))
        if (request.form['Submit'] == 'Внести'):
            sch = Schedule.query.filter_by(hash_sum=hash).first()

            if sch is None:
                schedule = Schedule(group_id=group_id,
                                    teacher_id=teacher_id,
                                    lesson_id=lesson_id,
                                    num_room=request.form['num_room'], day_week=request.form['day_select'],
                                    pair=request.form['pair_select'], denom=denom, hash_sum=hash)
                db.session.add(schedule)
                db.session.commit()
            else:
                db.session.query(Schedule).filter_by(hash_sum=hash).update(
                    {'teacher_id': teacher_id, 'lesson_id': lesson_id, 'num_room': request.form['num_room']})
                db.session.commit()
        elif (request.form['Submit'] == 'Удалить'):
            db.session.query(Schedule).filter_by(hash_sum=hash).delete()
            db.session.commit()


# ---------------------------------------------------------------------#

# ---------------------------------------------------------------------#
@app.route('/data', methods=['GET', 'POST'])
def data():
    form = TeacherForm()
    inset = ''
    submit = ''

    if form.validate_on_submit() and 'username' in session:
        inset = request.form['inset']
        submit = request.form['Submit']
        if inset == 'teachers':
            if submit == 'Добавить':
                try:
                    teacher = Teachers(teacher_name=request.form['add_teacher'],available_lessons=request.form['data'])
                    db.session.add(teacher)
                    db.session.commit()
                except:
                    db.session.rollback()

            elif submit == 'Редактировать':
                try:
                    t_name = request.form['new_teacher_name']
                    if len(t_name) > 1:
                        db.session.query(Teachers).filter_by(teacher_name=request.form['select_teacher']).update(
                            {'teacher_name': t_name, 'available_lessons': request.form['data']})
                        db.session.commit()
                except:
                    db.session.rollback()
            elif submit == 'Удалить':
                try:
                    t_name = request.form['select_teacher']
                    db.session.query(Schedule).filter_by(teacher_id=Teachers.query.filter_by(
                        teacher_name=t_name).first().id).delete()
                    db.session.query(Teachers).filter_by(teacher_name=t_name).delete()
                    db.session.commit()
                except:
                    db.session.rollback()

        if inset == 'groups':
            if submit == 'Добавить':
                try:
                    group = Groups(group_name=request.form['add_group'])
                    db.session.add(group)
                    db.session.commit()
                except:
                    db.session.rollback()

            elif submit == 'Редактировать':
                try:
                    t_name = request.form['new_group_name']
                    if len(t_name) > 1:
                        db.session.query(Groups).filter_by(group_name=request.form['edit_group_select']).update(
                            {'group_name': t_name})
                        db.session.commit()
                except:
                    db.session.rollback()

            elif submit == 'Удалить':
                try:
                    db.session.query(Schedule).filter_by(group_id=Groups.query.filter_by(
                        group_name=request.form['del_group_select']).first().id).delete()
                    db.session.query(Groups).filter_by(group_name=request.form['del_group_select']).delete()
                    db.session.commit()
                except:
                    db.session.rollback()

        if inset == 'lessons':
            if submit == 'Добавить':
                try:
                    lesson = Lessons(lesson_name=request.form['add_lesson'])
                    db.session.add(lesson)
                    db.session.commit()
                except:
                    db.session.rollback()

            elif submit == 'Редактировать':
                try:
                    t_name = request.form['new_lesson_name']
                    if len(t_name) > 1:
                        db.session.query(Lessons).filter_by(lesson_name=request.form['edit_lesson_select']).update(
                            {'lesson_name': t_name})
                        db.session.commit()
                except:
                    db.session.rollback()

            elif submit == 'Удалить':
                try:
                    db.session.query(Schedule).filter_by(lesson_id=Lessons.query.filter_by(
                        lesson_name=request.form['del_lesson_select']).first().id).delete()
                    db.session.query(Lessons).filter_by(lesson_name=request.form['del_lesson_select']).delete()
                    db.session.commit()
                except:
                    db.session.rollback()

    return render_template('newteacher.html', user=g.user, title='Teachers', form=form, inset=inset,
                           teachers=get_teachers(),
                           groups=get_groups(), lessons=get_lessons())


# ---------------------------------------------------------------------#
@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))

# ---------------------------------------------------------------------#
@app.before_request
def before_request():
    g.user = current_user

# ---------------------------------------------------------------------#

# ---------------------------------------------------------------------#
@login_required
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = FlaskForm()
    if 'username' in session:
        test(form)
    result = db.session.query(Schedule, Groups, Teachers, Lessons).filter(Schedule.group_id == Groups.id,
                                                                          Schedule.teacher_id == Teachers.id,
                                                                          Schedule.lesson_id == Lessons.id).all()
    days_enum = {'ПН': 1, 'ВТ': 2, 'СР': 3, 'ЧТ': 4, 'ПТ': 5}

    # res = [[], [], [], []]
    #
    # for sh, gr, te, le in result:
    #     res[0].append({'day_week': sh.day_week, 'pairs': sh.pairs, 'num_room': sh.num_room, 'denom': sh.denom})
    #     res[1].append({'group_name': gr.group_name})
    #     res[2].append({'teacher_name': te.teacher_name})
    #     res[3].append( {'lesson_name': le.lesson_name})

    res = []

    for sh, gr, te, le in result:
        res.append({'day_week': sh.day_week, 'pairs': sh.pair, 'num_room': sh.num_room, 'denom': sh.denom,'group_name': gr.group_name,'teacher_name': te.teacher_name,'lesson_name': le.lesson_name})


    return render_template("index.html", title="Главная", user=g.user, form=form,
                           teachers=get_teachers(), groups=get_groups(), days_enum=days_enum, result=result, test=res,
                           lessons=get_lessons())


@app.route('/l', methods=['GET', 'POST'])
def load_page():
    result = []
    form = FlaskForm()

    if 'username' in session:
        if (form.validate_on_submit()):
            group_id = Groups.query.filter_by(group_name=request.form['group_select']).first().id
            teacher_id = Teachers.query.filter_by(teacher_name=request.form['teacher_select']).first().id
            lesson_id = Lessons.query.filter_by(lesson_name=request.form['lesson_select']).first().id
            load = Load(group_id=group_id, lesson_id=lesson_id, teacher_id=teacher_id, weeks=request.form['weeks'],
                        academic_hours_week=request.form['academic_hours_week'],
                        academic_hours_term=request.form['academic_hours_term'],
                        courseworks=request.form['courseworks'], lab_works=request.form['lab_works'],
                        ind_works=request.form['ind_works'], exams=request.form['exams'], advice=request.form['advice'],
                        total_hours=request.form['total_hours'], term=request.form['term_select'])
            db.session.add(load)
            db.session.commit()

    for lo, gr, te, le in db.session.query(Load, Groups, Teachers, Lessons).filter(Load.group_id == Groups.id,
                                                                                   Load.teacher_id == Teachers.id,
                                                                                   Load.lesson_id == Lessons.id).all():
        result.append(
            {'id': lo.id, 'group_name': gr.group_name, 'lesson_name': le.lesson_name, 'teacher_name': te.teacher_name,
             'weeks': lo.weeks, 'academic_hours_week': lo.academic_hours_week,
             'academic_hours_term': lo.academic_hours_term, 'courseworks': lo.courseworks,
             'lab_works': lo.lab_works, 'ind_works': lo.ind_works, 'exams': lo.exams, 'advice': lo.advice,
             'total_hours': lo.total_hours, 'term': lo.term})

    return render_template("load.html", user=g.user, form=form, title='Нагрузка', result=result, teachers=get_teachers(),
                           lessons=get_lessons(),
                           groups=get_groups())


def get_groups():
    groups = []
    for group in Groups.query.all():
        groups.append({'id': group.id, 'group_name': group.group_name})

    return groups


def get_lessons():
    lessons = []
    for lesson in Lessons.query.all():
        lessons.append({'id': lesson.id, 'lesson_name': lesson.lesson_name})
    return lessons


def get_teachers():
    teachers = []
    for teacher in Teachers.query.all():
        teachers.append({'id': teacher.id, 'teacher_name': teacher.teacher_name, 'available_lessons': teacher.available_lessons})
    return teachers


def md5(text):
    return hashlib.md5(str(text).encode('UTF-8')).hexdigest()
