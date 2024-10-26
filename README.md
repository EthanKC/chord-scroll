# ChordScroll
### Video Demo:
### Description: 
A flask web app that let's users save guitar chords or tabs, and then auto scroll at their chosen speed. The purpose is to allow the user to play through a song without having to stop to scroll down. 

### Inspiration:
I'm an amateur guitar player. There are several sites that contain great chords and tabs, but for all of them you have to have a membership to use auto-scroll functionality. I wanted to make something I can use to autoscroll without having to pay. 

## Files
### [app.py](app.py)
The main file of the web app, this lays out all of the url routes that can be accessed for the web app. At the top, I've imported needed functions from the cs50, flask, flask_session, and werkzeug.security libraries. I've also imported a couple of functions from my helpers.py file. 

Below that I do some basic configuration of the app. The secret_key is necessary to allow the use of flash(). The app.config functions set up the session to use the filesystem instead of signed cookies. The db variable is set to use my chord-scroll.db. And the @app.after_request ensures responses aren't cached. 

The first route is "/". It uses the @login_required from helpers.py to indicate that this route is only accessible if the user is logged in.

### [helpers.py](helpers.py)



