from datetime import date, datetime
from flask import Flask, render_template, redirect, request, current_app, url_for


def home():
    
    return render_template('home.html')


def about():
    return render_template('about.html')


def booking():   
    return render_template('booking.html')