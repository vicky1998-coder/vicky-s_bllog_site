from flask import Flask, render_template, request
import requests
import  smtplib
import datetime as dt


GMAIL_ID = "dhagev434@gmail.com"
GMAIL_PASSWORD = "Sample@2021"
YAHOO_ID = "dhagev434@yahoo.com"

app = Flask(__name__)

blog_response = requests.get('https://api.npoint.io/34fe5358f4caeb016623').json()
today = dt.datetime.now()
day = today.strftime('%d')
month = today.strftime("%B")
year = today.year
formatted_date = f"{month} {day}, {year}"
print(formatted_date)


@app.route("/")
def home_page():
    return render_template("index.html", all_blogs=blog_response, date=formatted_date, current_year=year)

@app.route('/about')
def about():
    return render_template("about.html", current_year=year)

@app.route('/contact', methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        name = request.form["username"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]
        output_message = "Successfully sent your message!"
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=GMAIL_ID, password=GMAIL_PASSWORD)
            connection.sendmail(from_addr=GMAIL_ID,
                                to_addrs=YAHOO_ID,
                                msg=f"Subject:Blog Website Contact\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}")
        return render_template("contact.html", reply=output_message)
    return render_template('contact.html', current_year=year)

@app.route('/blog/<blog_id>')
def blog(blog_id):
    print(blog_id)
    for blog in blog_response:
        print(blog)
        if int(blog_id) == blog["id"]:
            print(blog["id"])
            return render_template("post.html", blog_post=blog)
    

if __name__ == "__main__":
    app.run(debug=True)
