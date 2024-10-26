# ChordScroll
### Video Demo:
### Description: 
A flask web app that let's users save guitar chords or tabs, and then auto scroll at their chosen speed. The purpose is to allow the user to play through a song without having to stop to scroll down. 

### Introduction:
I'm an amateur guitar player. There are several sites that contain great chords and tabs, but for all of them you have to have a membership to use auto-scroll functionality. I wanted to make something I can use to autoscroll without having to pay. I opted to require that users register and log in for a very specific reason. Sites like [Ultimate Guitar](www.ultimate-guitar.com) provide an extensive library or tabs and chords that can be accessed without registering. However, they actually pay royalties to record companies to be able to store and share those tabs. To get around that, each user of ChordScroll creates and maintains their own library of songs, that is only accessible to them.

## Files
### [app.py](app.py)
The main file of the web app, this lays out all of the url routes that can be accessed for the web app. At the top, I've imported needed functions from the cs50, flask, flask_session, and werkzeug.security libraries. I've also imported a couple of functions from my [helpers.py](#helpers.py) file. 

Below that I do some basic configuration of the app. The secret_key is necessary to allow the use of flash(). The app.config functions set up the session to use the filesystem instead of signed cookies. The _db_ variable is set to use my chord-scroll.db. And the @app.after_request ensures responses aren't cached. 

The first route is **"/"**, and it only uses the get method. It uses the @login_required from [helpers.py](#helpers.py) to indicate that this route is only accessible if the user is logged in. The index() function queries the database for the song title, id, artist, type, and genre, and sets the resutls to variable _songs_. It then renders template [index.html](#index.html), and passes in _songs_. then, [index.html](#index.html) displays the _songs_ data in a table. More details on that can be found in the [index.html](#index.html) section. 

Interestingly, the **"/"** route was actually the last one I completed. Originally, I had a **"/library"** route and library.html file that created a separate page to display the saved songs. I had some ideas that I might make the index page an introduction to the web app, or maybe a page where you could search either saved songs, or even search for chords or tabs through Google. Ultimately, I decided it was cleaner to just have the home page display the users saved songs. 



### [helpers.py](helpers.py)



