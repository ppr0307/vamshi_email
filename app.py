from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
import csv,json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Flask-Mail configuration
app.config["MAIL_SERVER"] = 'mail.abc.local'
app.config["MAIL_PORT"] = 25
app.config["MAIL_USE_TLS"] = True
# app.config["MAIL_USERNAME"] = 'your_email@example.com'
# app.config["MAIL_PASSWORD"] = 'your_email_password'

mail = Mail(app)




@app.route('/', methods=['GET', 'POST'])
def email_form():
    if request.method == 'POST':
        request_fields = request.get_json()
        from_email = request_fields["fromEmail"]
        to_email = request_fields["toEmail"]
        subject = request_fields["subject"]


        json_email_form = {}
        json_email_form["from_email"] = split_and_convert_to_json(request_fields["fromEmail"])
        json_email_form["to_email"] = split_and_convert_to_json(request_fields["toEmail"])
        json_email_form["subject"] = split_and_convert_to_json(request_fields["subject"])
        json_email_form["email_body_title"] = split_and_convert_to_json(request_fields["emailBodyTitle"])
        json_email_form["baselineUTC"] = split_and_convert_to_json(request_fields["baselineUTC"])
        json_email_form["previousTag"] = split_and_convert_to_json(request_fields["previousTag"])
        json_email_form["fwBugFixes"] = split_and_convert_to_json(request_fields["fwBugFixes"])     # fwBugFixes - Text area field
        json_email_form["keyFeatures"] = split_and_convert_to_json(request_fields["keyFeatures"])    # keyFeatures - Text area field
        json_email_form["performanceResults"] = split_and_convert_to_json(request_fields["performanceResults"])     # performanceResults - Text area field
        json_email_form["perfIssues"] = split_and_convert_to_json(request_fields["perfIssues"])         # perfIssues - Text area field
        json_email_form["stabilityResults"] = split_and_convert_to_json(request_fields["stabilityResults"])      # stabilityResults - Text area field
        json_email_form["cvPerfReport"] = split_and_convert_to_json(request_fields["cvPerfReport"])
        json_email_form["cvPerfDashboard"] = split_and_convert_to_json(request_fields["cvPerfDashboard"])
        json_email_form["performanceLive"] = split_and_convert_to_json(request_fields["performanceLive"])
        json_email_form["functionalRegression"] = split_and_convert_to_json(request_fields["functionalRegression"])   # functionalRegression - Text area field
        json_email_form["releaseContent"] = split_and_convert_to_json(request_fields["releaseContent"])         # releaseContent - Text area field
        # print(json.dumps(json_email_form))



        # Final JSON output to render as html email body 
        json_final = {}
        
        # add json_email node to final json
        json_final["email_form"] = json_email_form
        
        # Read CSV file
        # csv_file_path = 'data.csv'  # Replace 'data.csv' with the path to your CSV file
        # json_csv_data = []

        # with open(csv_file_path, 'r') as csv_file:
        #     csv_reader = csv.DictReader(csv_file)
        #     for row in csv_reader:
        #         json_csv_data.append(row)
        # json_final["csv_rows"] = json_csv_data

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


def split_and_convert_to_json(input_string):
    lines = input_string.split('\n')
    if len(lines) <= 1:
        return input_string
    json_array = [{'line': line.strip()} for line in lines if line.strip()]
    return json_array



if __name__ == '__main__':
    app.run(debug=True)
