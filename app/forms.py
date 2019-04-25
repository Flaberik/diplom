from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, PasswordField, SelectField
from wtforms.validators import Required

#---------------------------------------------------------------------#
class LoginForm(FlaskForm):
    login = TextField('login', validators = [Required()])
    password = PasswordField('password', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

#---------------------------------------------------------------------#
class SignUp(FlaskForm):
    login = TextField('login', validators = [Required()])
    pass_one = PasswordField('passf', validators = [Required()])
    pass_two = PasswordField('passf', validators = [Required()])

class TeacherForm(FlaskForm):
    teacher_name = TextField('tn')
#---------------------------------------------------------------------#
