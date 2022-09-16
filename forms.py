from wtforms import StringField, SubmitField, PasswordField, HiddenField, SelectField, IntegerField, FileField, BooleanField
from wtforms.validators import DataRequired, EqualTo, IPAddress
from flask_wtf.file import FileRequired, FileAllowed
from flask_wtf import FlaskForm
import models

class LoginForm(FlaskForm):
    username_field = StringField("username", [DataRequired()])
    password_field = PasswordField("password", [DataRequired()])
    login_button = SubmitField("Log In")

class APILoginForm(FlaskForm):
    username_field = StringField("username", [DataRequired()])
    password_field = PasswordField("password", [DataRequired()])
    host_ip = SelectField('host_ip')
    login_button = SubmitField("Log In")


class RegistrationForm(FlaskForm):
    username=StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    password2 = PasswordField('Repeat Password', [DataRequired(), EqualTo('password', message='Passwords must match')])
    register_button = SubmitField('Register', [])

class AddServer(FlaskForm):
    server_ip = StringField('server_ip', [IPAddress()])
    add_button = SubmitField('Add Server')

class AddScpServer(FlaskForm):
    server_ip = StringField('server_ip', [IPAddress()])
    host_ip = SelectField('host_ip')
    add_button = SubmitField('Add Server')


class ConfirmDelete(FlaskForm):
    hidden_input = HiddenField("server_to_remove" )

class UploadDatarakeForm(FlaskForm):
    file=FileField(
        name='dr_file',
        label='Upload Datarake(.tgz):',
        validators=[FileRequired()
        ])
    submit=SubmitField('Upload Datarake')

class HealthCheckForm(FlaskForm):
    rrd_graphs = BooleanField('RRD Graphs: ',default=True)
    db_stats = BooleanField('DB Stats: ',default=True)
    dhcp_health = BooleanField('DHCP Health: ',default=True)
    file=FileField(
        name='dr_file',
        label='Upload Datarake(.tgz):',
        validators=[FileRequired()
        ])
    weeksneeded = IntegerField('weeksneeded')
    submit=SubmitField('Analyze Datarake')

class InitiateHCForm(FlaskForm):
    customer_selection = SelectField('customer',
                                     choices=['Example Customer 1','Example Customer 2'])
    case_number = IntegerField('case', [DataRequired()])
    server_ip = StringField('server_ip', [IPAddress()])
    submit=SubmitField('Initiate Health Check')



#class RRDGraphForm(FlaskForm):
    #source = SelectField(
    #    label='RRD Source',
    #    choices=[
    #        ('Please Select', 'Please Select'),
    #        ('Upload', 'Upload'),
    #        ('Files from machine','Files from machine')
    #        ]
    #    )
    #file = FileField(
    #    label='Zip the RRDS without folder'
    #)
    #no_of_weeks = StringField(
    #    label='Number Of Weeks',
    #    default='12'
    #)
    #ip_address = StringField(
    #    label='IP Address',
    #    validators=[IPAddress()],
      #  inputs={'configuration': 'configuration', 'address': 'ip_address'},
      #  result_decorator=None,
        #is_disabled_on_start=False,
       # enable_on_complete=['datarake','commands','database_commands','ip_address_username','ip_address_password']
    #)
    #ip_address_username = StringField(
    #    label='IP Address Username',
        # validators=[DataRequired()]
        #is_disabled_on_start=False
    #)
    #ip_address_password = PasswordField(
     #   label='IP Address Password',
     #   default='abc',
     #   validators=[DataRequired()]
    #)
#    submit = SubmitField(label='Submit')