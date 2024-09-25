from flask import Flask, abort, render_template, redirect, url_for, flash, request, session
from load_artifacts import Artifacts
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, NumberRange
import numpy as np
from flask_bootstrap import Bootstrap5
import pandas as pd
from smtplib import SMTP
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
Bootstrap5(app)

my_email = os.getenv('MY_EMAIL')
my_pass = os.getenv('MY_PASSWORD')

the_time = datetime.now()


class HouseForm(FlaskForm):
    p_type = SelectField("Property Type", coerce=str, choices=[], validators=[DataRequired()])
    bathroom = IntegerField("Bathroom(s)", validators=[DataRequired(), NumberRange(min=1, max=10)])
    bedroom = IntegerField("Bedroom(s)", validators=[DataRequired(), NumberRange(min=1, max=10)])
    location = SelectField("Location", coerce=str, choices=[], validators=[DataRequired()])

    submit = SubmitField('Submit')


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()], render_kw={'class': 'form-control'})
    email = StringField("Email", validators=[DataRequired()], render_kw={'class': 'form-control'})
    subject = StringField("Subject", validators=[DataRequired()], render_kw={'class': 'form-control'})
    message = TextAreaField("Message", validators=[DataRequired()], render_kw={'class': 'form-control'})

    submit = SubmitField('Send', render_kw={'class': 'button'})


artifacts = Artifacts()


def predict_price(bedroom, bathroom, location, pro_type):
    x = np.zeros(len(artifacts.columns))
    x[0] = bedroom
    x[1] = bathroom

    try:
        property_type_index = artifacts.columns.index(pro_type.lower())
        if property_type_index >= 0:
            x[property_type_index] = 1
    except ValueError:
        print(f"Location '{pro_type}' not found, setting value to 0.")

    try:
        location_index = artifacts.columns.index(location.lower())
        if location_index >= 0:
            x[location_index] = 1
    except ValueError:
        print(f"Location '{location}' not found, setting value to 0.")

    x_df = pd.DataFrame([x], columns=[cols.title() for cols in artifacts.columns])

    # Predict using the model and return the result
    return artifacts.model.predict(x_df)[0]


@app.route("/", methods=['GET', 'POST'])
def home():
    form = HouseForm()
    form.p_type.choices = [(p_type, p_type.title()) for p_type in artifacts.p_type]
    form.p_type.choices.append(("townhouse", "Townhouse"))
    form.location.choices = [(location, location.title()) for location in artifacts.location]
    form.location.choices.append(("other", "Others"))
    mean_price = artifacts.mean_price_list

    if form.validate_on_submit():
        p_type = form.p_type.data
        location = form.location.data
        bedroom = form.bedroom.data
        bathroom = form.bathroom.data

        form = HouseForm(
            p_type=p_type,
            bathroom=bathroom,
            bedroom=bedroom,
            location=location
        )
        form.p_type.choices = [(p_type, p_type.title()) for p_type in artifacts.p_type]
        form.p_type.choices.append(("townhouse", "Townhouse"))
        form.location.choices = [(location, location.title()) for location in artifacts.location]
        form.location.choices.append(("other", "Others"))
        mean_price = artifacts.mean_price_list

        the_price = predict_price(bedroom=bedroom, bathroom=bathroom, location=location, pro_type=p_type)
        return render_template('index.html',
                               form=form,
                               prediction="{:,.2f}".format(the_price),
                               mean_price=mean_price,
                               times=the_time
                               )
    return render_template('index.html', form=form, mean_price=mean_price, times=the_time)


@app.route('/about')
def about():
    return render_template('about.html', times=the_time)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        name = form.name.data
        email = form.email.data
        subject = form.subject.data
        message = form.message.data
        connection = SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(my_email, my_pass)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg=f"{subject}\n\n"
                f"{message}.\nAccount Details:\n"
                f"Name: {name}\n"
                f"Email: {email}")
        connection.quit()

        flash('Message sent successfully, I will get back to you shortly.', "success")

        return redirect(url_for('contact'))

    return render_template("contact.html", form=form, times=the_time)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
