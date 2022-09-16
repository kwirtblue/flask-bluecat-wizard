from app import app, db
from flask import render_template, redirect, request, url_for, flash, abort
import forms, login, models, api_calls, os
from flask_login import login_required, login_user, current_user, logout_user
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
import requests, datetime, tarfile, sys, rrdtool
from imported.rrdfilesgraph import rrdgraph, scanfolder, timestamp


@app.route("/login", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def login_page():
    login_form = forms.LoginForm()
    if request.method == "GET":
        return render_template("login.html", login_form = login_form)
    if request.method == "POST":
        if login_form.validate_on_submit():
            user = models.User.query.filter_by(username = login_form.username_field.data).first()
            if user and check_password_hash(user.password_hash, login_form.password_field.data):
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
            else:
                flash("Invalid login credentials, please try again.")
                return render_template("login.html", login_form = login_form)
        else:
            flash("Invalid login credentials, please try again.")
            return render_template("login.html", login_form=login_form)

@app.route("/register", methods=["GET", "POST"])
def register():
    register_form = forms.RegistrationForm()
    if request.method == "GET":
        return render_template('register.html', register_form = register_form)
    if request.method == "POST":
        if register_form.validate_on_submit():
            user = models.User(username = register_form.username.data)
            user.set_password(register_form.password.data)
            db.session.add(user)
            try:
                db.session.commit()
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
            except:
                db.session.rollback()
                flash("Username is already in use!")
                return render_template('register.html', register_form = register_form)
        else:
            flash("Passwords do not match!")
            return render_template('register.html', register_form = register_form)

@app.route("/dashboard")
@app.route("/dashboard", methods=['GET','POST'])
@login_required
def dashboard():
    user = current_user
    return render_template("dashboard.html", user=user)


@app.route("/api", methods=['GET', 'POST'])
@app.route("/api/<api_call>", methods=['GET', 'POST'])
@login_required
def api(api_call=None):
    #pull updated server list from db
    server_list = []
    for item in models.HostList.query.all():
       server_list.append(item.ip)
    #Create forms
    add_server_form = forms.AddServer()
    api_login_form = forms.APILoginForm()
    confirm_delete_form = forms.ConfirmDelete()
    #add server list to api login form
    api_login_form.host_ip.choices = server_list
    #handle post requests
    if request.method == 'POST':
        flash("Call Method: " + str(request.method))
        #handle login request
        flash("Call: " + str(api_call))
        if api_call == "apilogin":
            if api_login_form.validate_on_submit():
                username = api_login_form.username_field.data
                password = api_login_form.password_field.data
                server_ip = api_login_form.host_ip.data
                api_login_form.host_ip.server_ip = server_ip
            #retrieve log in and retrieve token
                raw_token = api_calls.try_login(server_ip, username, password)
                #check if token has a value
                if raw_token:
                    bam_token = raw_token.split()[2] + " " + raw_token.split()[3]
                    current_user.set_api_token(bam_token)
                    db.session.add(current_user)
                    try:
                        db.session.commit()
                        flash("Token saved for user: " + str(username))
                    except:
                        db.session.rollback()
                        flash("Failed to save token")
                # if token exists, run getSystemInfo() api call
                    system_info = api_calls.getSystemInfo(bam_token, server_ip)
                    current_user.system_info = system_info
                    timestamp = str(datetime.datetime.now())[0:19]
                    current_user.sys_info_timestamp = timestamp
                    db.session.add(current_user)
                    try:
                        db.session.commit()
                    except:
                        db.session.rollback()
                return render_template ('api.html', api_login_form=api_login_form, user=current_user, add_server_form=add_server_form, confirm_delete_form=confirm_delete_form)
            else:
               flash(api_login_form.errors)
               return render_template('api.html', api_login_form=api_login_form, user=current_user, add_server_form=add_server_form, confirm_delete_form=confirm_delete_form)
        #handle request to add server to drop down list
        if api_call == "addserver":
            if add_server_form.validate_on_submit():
                server_ip = add_server_form.server_ip.data
                flash(server_ip)
                add_server = models.HostList(ip = server_ip)
                db.session.add(add_server)
                try:
                    db.session.commit()
                    flash("Server added!")
                except:
                    db.session.rollback()
                    flash("Failed to add server!")
            else:
                flash("Invalid IP Address!")
            return redirect("")
#       remove server from list
        if api_call == "removeserver":
            if confirm_delete_form.validate_on_submit():
                server_remove_choice = confirm_delete_form.hidden_input.data
                server_to_remove = models.HostList.query.filter_by(ip=server_remove_choice).first()
                try:
                    db.session.delete(server_to_remove)
                    db.session.commit()
                    flash(str(server_remove_choice) + " has been removed!")
                except:
                    db.session.rollback()
                    flash("Failed to remove " + str(server_remove_choice))
                return redirect("")
            else:
                return redirect("")

#handles anything that isn't a post request (GET requests)
    else:
         return render_template('api.html', api_login_form=api_login_form,
                                user=current_user,
                                add_server_form=add_server_form,
                                confirm_delete_form=confirm_delete_form
                                )

@app.route("/healthcheck")
@app.route("/healthcheck/<action>", methods=['GET', 'POST'])
@login_required
def health_check(action=None):
    #scp_add_server_form
    scp_add_server_form = forms.AddScpServer()
    server_list = []
    for item in models.HostList.query.all():
        server_list.append(item.ip)
    scp_add_server_form.host_ip.choices = server_list
    #add_datarake_form
    upload_datarake_form = forms.UploadDatarakeForm()
    #health_check_options_form
    health_check_form = forms.HealthCheckForm()
    # handle post requests
    if request.method == 'POST':
        flash("Call Method: " + str(request.method))
        # handle login request
        flash("Call: " + str(action))
        if action == 'analyzedatarake':
            if health_check_form.validate_on_submit():
                file=request.files['dr_file']
                file_ext = os.path.splitext(file.filename)[1]
                if file_ext == '.tgz':
                    #try:
                        fname = secure_filename(file.filename)
                        path = 'Tmp/uploads/datarakes/'
                        extracted_path = path + fname.split('.tgz')[0]
                        file.save(os.path.join(path,fname))
                        flash('Datarake uploaded successfully!')
                        with tarfile.open(os.path.join(path,fname)) as datarake:
                            members = []
                            for compressed_file in datarake.getmembers():
                                if compressed_file.name.endswith('.rrd'):
                                    members.append(compressed_file)
                            datarake.extractall(members=members, path=path)
                        weeksneeded = health_check_form.weeksneeded.data
                        filenames = scanfolder(extracted_path + '/data/rrdtool/data')
                        #flash(timestamp(filenames, extracted_path + '/data/rrdtool/data', weeksneeded))
                        #rrdgraph(filenames, extracted_path, timeframe, res_path, hostname=None, username=None, password=None)
                        #    for tarinfo in datarake.getmembers():
                        #        flash(tarinfo.name)
                        #try:
                        #    datarake = tarfile.open(os.path.join(path,fname), 'w:gz')
                        #    datarake.extract(path=os.path.join(path,"/",fname,'/data/rrdtool/data'))
                        #    datarake.close()
                        #except:
                        #    flash('Failed to extract tgz file!')
                #temporarily setting the attributes for remote server to none until I add remote functionality
                #need to extract files and create these variables

                #    except:
                #        flash('File failed to save')
                #    health_check_form.rrd_graphs.data
                else:
                    flash('Incorrect file type, please select a valid .tgz file!')
                return redirect('')
            return redirect('')
        if action == "addserver":
            if scp_add_server_form.validate_on_submit():
                server_ip = scp_add_server_form.server_ip.data
                flash(server_ip)
                add_server = models.HostList(ip = server_ip)
                db.session.add(add_server)
                try:
                    db.session.commit()
                    flash("Server added!")
                except:
                    db.session.rollback()
                    flash("Failed to add server!")
            else:
                flash("Invalid IP Address!")
            selected_ip = scp_add_server_form.host_ip.data
            return redirect('')

    return render_template("healthcheck.html",
                           scp_add_server_form=scp_add_server_form,
                           server_list=server_list,
                           health_check_form = health_check_form
                           )

@app.route('/analyzer', methods=['GET','POST'])
@login_required
def analyzer():
    if request.method == 'POST':
        pass

    return render_template('analyzer.html', hc_form = forms.InitiateHCForm())

@app.route("/logout")
@login_required
def logout():
    current_user.remove_api_token()
    current_user.remove_system_info()
    try:
        db.session.add(current_user)
        db.session.commit()
    except:
        pass
    flash('You are now logged out.')
    logout_user()
    return redirect("login")

