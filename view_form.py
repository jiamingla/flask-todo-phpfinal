#  引入flask_wtf
from flask_wtf import FlaskForm
#  各別引入需求欄位類別
from wtforms import StringField, SubmitField, BooleanField
#from wtforms.fields.html5 import EmailField
#  引入驗證
#from wtforms.validators import DataRequired, Email

#  從繼承FlaskForm開始
class TodoForm(FlaskForm):
  content = StringField('content', validators=[DataRequired(message='Not Null')])
  done = BooleanField('done')
  submit = SubmitField('Submit')