import webapp2
import cgi
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile("^.{3,20}$")
EMAIL_RE = re.compile("^[\S]+@[\S]+.[\S]+$")

def valid_username(username):
    return username and USER_RE.match(username)

def valid_password(password):
    return password and PASS_RE.match(password)

def valid_email(optional_email):
    return not optional_email or EMAIL_RE.match(optional_email)

def buildpage(username, optional_email, username_error, password_error, verify_error, email_error):
    header = "<h2>Signup</h2>"
    username_label = "<label>Username: </label>"
    username_text_box = "<input type='text' name='username' value='%s' />"%username
    username_error = "<label class='error' style='color:red'>"+"%s"%username_error+"</label>"

    password_label = "<label>Password: </label>"
    password_text_box ="<input type='password' name='password' required/>"
    password_error = "<label class='error' style='color:red'>"+"%s"%password_error+"</label>"

    verify_password_label = "<label>Verify Password: </label>"
    verify_password_text_box = "<input type='password' name='verify_password' required/>"
    verify_error = "<label class='error' style='color:red'>"+"%s"%verify_error+"</label>"

    optional_email_label = "<label>Email (Optional): </label>"
    optional_email_text_box = "<input type='text' name='optional_email' value='%s' required/>"%optional_email
    email_error = "<label class='error' style='color:red'>"+"%s"%email_error+"</label>"

    submit_button = "<input type='submit' value='Submit'>"

    form = ("<form method='post'>" + username_label + username_text_box + username_error + "<br>" + password_label + password_text_box + password_error + "<br>" + verify_password_label + verify_password_text_box + verify_error + "<br>" + optional_email_label + optional_email_text_box + email_error + "<br>" + submit_button + "</form>")

    return header+form

def welcomepage(username):
     header = "<h2>Welcome, '%s'</h2>"%username
     return header

class MainHandler(webapp2.RequestHandler):
    def get(self):
        content = buildpage("", "", "", "", "", "")
        self.response.write(content)

    def post(self):

        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify_password = self.request.get('verify_password')
        optional_email = self.request.get('optional_email')
        username_error = ""
        password_error = ""
        verify_error = ""
        email_error = ""


        if not valid_username(username):
            username_error = "Please enter a valid username."
            have_error = True
        if not valid_password(password):
            password_error = "Please enter a valid password."
            have_error = True
        elif password != verify_password:
            verify_error = "Your passwords do not match."
            have_error = True
        if not valid_email(optional_email):
            email_error = "Please enter a valid email."
            have_error = True
        if have_error:
            self.response.write(buildpage(username, optional_email, username_error, password_error, verify_error, email_error))
        else:
            self.redirect('/welcome?username=' + username)

class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.response.write(welcomepage(username))
        else:
            self.redirect("/")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
