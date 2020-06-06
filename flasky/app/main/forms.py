from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField,IntegerField,DateField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Role, User


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

class PostForm(FlaskForm):
    #body = PageDownField("What's on your mind?", validators=[DataRequired()])
    name = StringField('客户姓名', validators=[Length(0, 64)])
    phnumber = StringField('手机号码', validators=[Length(0, 64)])
    #homeaddress = StringField('家庭地址', validators=[Length(0, 64)])
    #career = StringField('职业', validators=[Length(0, 64)])
    #company = StringField('公司名称', validators=[Length(0, 64)])
    jobaddress = StringField('办公地址', validators=[Length(0, 64)])
    #families = IntegerField('家庭成员')
    #insurance = IntegerField('保单数')
    #source = StringField('客户来源', validators=[Length(0, 64)])
    #married = BooleanField('是否已婚')
    #bobies = BooleanField('是否有小孩')
    #liking = StringField('兴趣爱好', validators=[Length(0, 64)])
    #connects = IntegerField('跟进数次')
    #income = IntegerField('年收入')
    submit = SubmitField('Submit')

class PostForm1(FlaskForm):
    #body = PageDownField("What's on your mind?", validators=[DataRequired()])
    name = StringField('客户姓名', validators=[Length(0, 64)])
    phnumber = StringField('手机号码', validators=[Length(0, 64)])
    homeaddress = StringField('家庭地址', validators=[Length(0, 64)])
    career = StringField('职业', validators=[Length(0, 64)])
    company = StringField('公司名称', validators=[Length(0, 64)])
    jobaddress = StringField('办公地址', validators=[Length(0, 64)])
    families = IntegerField('家庭成员')
    insurance = IntegerField('保单数')
    source = StringField('客户来源', validators=[Length(0, 64)])
    married = BooleanField('是否已婚')
    bobies = BooleanField('是否有小孩')
    liking = StringField('兴趣爱好', validators=[Length(0, 64)])
    connects = IntegerField('跟进数次')
    income = IntegerField('年收入')
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    #body = PageDownField("What's on your mind?", validators=[DataRequired()])
    meetway = StringField('沟通方式', validators=[DataRequired()])
    meetcase = StringField('沟通借口', validators=[DataRequired()])
    meetdate = DateField('拜访日期')
    meetadress = StringField('拜访地址', validators=[DataRequired()])
    meettimese = IntegerField('拜访次数')
    beetway = StringField('客养方式', validators=[DataRequired()])
    newsabout = PageDownField("客户最新情况", validators=[DataRequired()])
    thisthink = StringField('沟通保险观念', validators=[DataRequired()])
    fation = StringField('客户反馈', validators=[DataRequired()])
    planbook = BooleanField('是否做计划书')
    badthing = PageDownField("拜访不足总结", validators=[DataRequired()])
    donething = PageDownField("做了哪些准备", validators=[DataRequired()])
    nexttime = IntegerField('几天后再联系')
    todo = PageDownField("这个客户以后怎么跟", validators=[DataRequired()])
    submit = SubmitField('Submit')

class CommentForm1(FlaskForm):
    #body = PageDownField("What's on your mind?", validators=[DataRequired()])
    meetway = StringField('沟通方式', validators=[DataRequired()])
    meetcase = StringField('沟通借口', validators=[DataRequired()])
    meetdate = DateField('拜访日期')
    #meetadress = StringField('拜访地址', validators=[DataRequired()])
    #meettimese = IntegerField('拜访次数')
    beetway = StringField('客养方式', validators=[DataRequired()])
    #newsabout = PageDownField("客户最新情况", validators=[DataRequired()])
    #thisthink = StringField('沟通保险观念', validators=[DataRequired()])
    #fation = StringField('客户反馈', validators=[DataRequired()])
    #planbook = BooleanField('是否做计划书')
    #badthing = PageDownField("拜访不足总结", validators=[DataRequired()])
    #donething = PageDownField("做了哪些准备", validators=[DataRequired()])
    #nexttime = IntegerField('几天后再联系')
    #todo = PageDownField("这个客户以后怎么跟", validators=[DataRequired()])
    submit = SubmitField('Submit')


class InsuranceForm1(FlaskForm):
    insurname = StringField('险种', validators=[DataRequired()])
    toubaoriqi  = IntegerField('投保日期')
    baofei  = IntegerField('保费')
    baoer  = IntegerField('保额')
    submit = SubmitField('Submit')



class InsuranceForm(FlaskForm):
    insurname = StringField('险种', validators=[DataRequired()])
    toubaoriqi  = IntegerField('投保日期')
    baofei  = IntegerField('保费')
    baoer  = IntegerField('保额')
    baodanhao  = IntegerField('投保单号')
    toubaoriqi  = DateField('投保日期')
    shengxiaoriqi  = IntegerField('生效日期')
    baodanzhuangtai  = StringField('保单状态')
    jiaofeifangshi  = StringField('缴费方式')
    jiaofeiqi  = IntegerField('缴费期')
    baoxianqijian  = IntegerField('保险期间')
    shixiaoriqi  = IntegerField('失效日期')
    banknumber  = IntegerField('银行账户')
    bankname  = StringField('缴费银行')
    nextgetmoney  = IntegerField('投保日期')
    #tbname = StringField('投保人')
    bbname  = StringField('被保人')
    syname  = StringField('收益人')
    jjname  = StringField('紧急联系人')
	
    submit = SubmitField('Submit')