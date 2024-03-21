from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
import csv,json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'mail.ouc.local'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'your_email@example.com'
# app.config['MAIL_PASSWORD'] = 'your_email_password'

mail = Mail(app)

@app.route('/', methods=['GET', 'POST'])
def email_form():
    if request.method == 'POST':
        request_fields = request.get_json()
        from_email = request_fields['fromEmail']
        to_email = request_fields['toEmail']
        subject = request_fields['subject']
        email_body_title = request_fields['emailBodyTitle']
        release_tag = request_fields['releaseTag']
        release_notes = request_fields['releaseNotes']
        release_notes_list = release_notes.splitlines()

        # Final JSON output to render as html email body 
        json_final = {}
        
        json_email = {}
        json_email["from_email"] = from_email
        json_email["to_email"] = to_email
        json_email["subject"] = subject
        json_email["email_body_title"] = email_body_title
        json_email["release_tag"] = release_tag
        json_release_notes = []
        for i, r in enumerate(release_notes_list):
            json_release_notes.append({"line": r})
        json_email["release_notes"] = json_release_notes

        # print(json_email)
        # add json_email node to final json
        json_final["email_form"] = json_email
        
        # Read CSV file
        csv_file_path = 'data.csv'  # Replace 'data.csv' with the path to your CSV file
        json_csv_data = []

        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                json_csv_data.append(row)
        json_final["csv_rows"] = json_csv_data

        # Store JSON data into a variable and print it
        # json_variable = json.dumps(json_final)
        # print(json_variable)

        # Sending email
        try:
            msg = Message(subject=subject, sender=from_email, recipients=[to_email])
            # msg.body = f"{email_body_title}\n\n{email_body}"
            msg.html = render_template("email.html",data=json_final)
            mail.send(msg)
            return {"status":"success"}
            flash('Email sent successfully!', 'success')
        except Exception as e:
            print(str(e))
            return {"status":"error", "errorDesc":str(e)}
            # flash(f'Failed to send email. Error: {str(e)}', 'error')

        return redirect(url_for('email_form'))

    return render_template('email_form.html')

if __name__ == '__main__':
    app.run(debug=True)
