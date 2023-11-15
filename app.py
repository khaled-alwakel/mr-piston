import os
from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, usd

#  Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///autoservice.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


#========[ Register ]==========#
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

           # deal with name
        if not name:
            name_alert ="missing username"
            return render_template("apology.html", alert = name_alert)
        
        # deal with password
        if not password:
            pass_alert ="missing password"
            return render_template("apology.html", alert = pass_alert)
        if password != confirmation:
            confirm_alert ="password do not match"
            return render_template("apology.html", alert = confirm_alert)
        password = generate_password_hash(password)

     
        try:
            new_user = db.execute("INSERT INTO users (username, hash) VALUES(?,?)", name, password)
        except:
            exist_alert ="username already registered"
            return render_template("apology.html", alert = exist_alert)
           
        session["user_id"] = new_user
        return redirect("/login")
    
    return render_template("register.html")


#========[ Login ]==========#
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            name_alert = "must provide username"
            return render_template("apology.html", alert = name_alert)
        

        # Ensure password was submitted
        elif not request.form.get("password"):
            pass_alert ="must provide password"
            return render_template("apology.html", alert = pass_alert)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            check_alert ="invalid username and/or password"
            return render_template("apology.html", alert = check_alert)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        name = rows[0]["username"]
        return render_template("index.html" ,name = name)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    

#========[ Homepage ]==========#
@app.route("/")
def index():
    """Show index page"""
    return render_template("index.html")


#========[ services ]==========#
@app.route("/services")
def services():
    """Show service page"""
    return render_template("services.html")


#========[ Booking ]==========#
@app.route("/appointment", methods=["POST", "GET"])
@login_required
def book():
    if request.method == "POST":
        name = request.form.get("name")
        brand = request.form.get("brand")
        date = request.form.get("date")
        phone = request.form.get("phone")
        service = request.form.get("service")

        if not name or not brand or not date  or not phone or not service:
            miss_alert = "please fill all fields up "
            return render_template("apology.html", alert = miss_alert)
            
        #insert booking
        user_id = session["user_id"]
        db.execute("INSERT INTO appointments (user_id, name, brand, date, phone, service) VALUES (?,?,?,?,?,?)",user_id, name, brand, date, phone, service)
        
        return redirect("/appointment")
    else:
        services = [
        "auto maintenance ",
        "brake repair pads",
        "shocks replacement",
        "system diagnosis ",
        "air conditioning ",
        "tires & wheels balancing",
        "towing service",
        "jump start",
        "body repair & painting"
        ]
        return render_template("appointment.html", services = services)
    
    
#========[ appointments ]==========#
@app.route("/appointments")
@login_required
def appointments():
    user_id = session["user_id"]
    rows = db.execute("SELECT * FROM appointments WHERE user_id =?",user_id)
    return render_template("appointments.html", rows = rows)


#========[ Delete Appointment ]==========#
@app.route("/delete", methods=["POST"])
@login_required
def delete():

    id = request.form.get("id")
    if id:
        user_id = session["user_id"]
        db.execute("DELETE FROM appointments WHERE id = ? AND user_id =?", id,user_id)
    return redirect("/appointments")


#========[ parts ]==========#
@app.route("/parts")
def parts():
    rows = db.execute("SELECT * FROM  parts")
    return render_template("parts.html", rows = rows)

    
#========[ Favorites ]==========#
@app.route("/fav", methods=["POST","GET"])
@login_required
def fav():
    # Ensure cart exists
    if "cart" not in session:
        session["cart"] = []
        
    if request.method == "POST":
        part_id = request.form.get("part_id")
        if part_id:
               session["cart"].append(part_id)
        return redirect("/parts")

    rows = db.execute("SELECT * FROM parts  WHERE id IN (?)",session["cart"])
    return render_template("fav.html", rows = rows)


#========[ Settings ]==========#
@app.route("/settings", methods=["POST","GET"])
@login_required
def settings():
    return render_template("settings.html")


#========[ Update name ]==========#
@app.route("/update_name", methods=["POST","GET"])
@login_required
def update_name():
    if request.method =="POST":
        old = request.form.get("old-username")
        new = request.form.get("new-username")
        confirm = request.form.get("confirmation")
        
        if not old or not new or not confirm:
            miss_alert = "please fill up the forms"
            return render_template("apology.html", alert = miss_alert)
        
        if new != confirm:
            confirm_alert = "new name dont match"
            return render_template("apology.html", alert = confirm_alert)
        
        #is old match the one in database
        user_id = session["user_id"]
        rows= db.execute("SELECT username FROM users WHERE id = ?", user_id)
        if old  != rows[0]["username"]:
            check_alert = "sorry old username is not correct"
            return render_template("apology.html", alert = check_alert)
            
        
        db.execute("UPDATE users SET username = ? WHERE id =?",new,user_id)
        return redirect("/update_name")
    
    return redirect("/settings")
    

#========[ Update password ]==========#
@app.route("/update_pass", methods=["POST","GET"])
@login_required
def update_pass():
    if request.method =="POST":
        old = request.form.get("old-password")
        new = request.form.get("new-password")
        confirm = request.form.get("confirmation")
        
        if not old or not new or not confirm:
            miss_alert = "please fill up the forms"
            return render_template("apology.html", alert = miss_alert)
        
        if new != confirm:
            confirm_alert = "new password dont match"
            return render_template("apology.html", alert = confirm_alert)
        
        #is old match the one in database
        user_id = session["user_id"]
        rows= db.execute("SELECT hash FROM users WHERE id = ?", user_id)
        hashed_old = generate_password_hash(old)
        
        if hashed_old  != rows[0]["hash"]:
            check_alert = "sorry old password is not correct"
            return render_template("apology.html", alert = check_alert)
        
        password = generate_password_hash(new)
     
        db.execute("UPDATE users SET hash = ? WHERE id =?",password,user_id)
        return redirect("/update_pass")
    
    return redirect("/settings")




#========[ log out ]==========#
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

#============[ End ]=============#



