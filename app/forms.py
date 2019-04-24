from flask_wtf import Form
from wtforms import TextField, BooleanField, PasswordField
from wtforms.validators import Required

#---------------------------------------------------------------------#
class LoginForm(Form):
    username = TextField('login', validators = [Required()])
    #pass_f = PasswordField('passf', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

#---------------------------------------------------------------------#
class SignUp(Form):
    login = TextField('login', validators = [Required()])
    pass_one = PasswordField('passf', validators = [Required()])
    pass_two = PasswordField('passf', validators = [Required()])

#---------------------------------------------------------------------#
