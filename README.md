# ChordScroll
### Video Demo:
### Description: 
A flask web app that let's users save guitar chords or tabs, and then auto scroll at their chosen speed. The purpose is to allow the user to play through a song without having to stop to scroll down. 

### Introduction:
I'm an amateur guitar player. There are several sites that contain great chords and tabs, but for all of them you have to have a membership to use auto-scroll functionality. I wanted to make something I can use to autoscroll without having to pay. I opted to require that users register and log in for a very specific reason. Sites like [Ultimate Guitar](https://www.ultimate-guitar.com) provide an extensive library or tabs and chords that can be accessed without registering. However, they actually pay royalties to record companies to be able to store and share those tabs. To get around that, each user of ChordScroll creates and maintains their own library of songs, that is only accessible to them.

## Files
### [app.py](app.py)
The main file of the web app, this lays out all of the url routes that can be accessed for the web app. At the top, I've imported needed functions from the cs50, flask, flask_session, and werkzeug.security libraries. I've also imported a couple of functions from my [helpers.py](#helperspy) file. 

Below that I do some basic configuration of the app. The secret_key is necessary to allow the use of flash(). The app.config functions set up the session to use the filesystem instead of signed cookies. The _db_ variable is set to use my chord-scroll.db. And the @app.after_request ensures responses aren't cached. 

The first route is **"/"**, and it only uses the get method. It uses the @login_required from [helpers.py](#helperspy) to indicate that this route is only accessible if the user is logged in. The index() function queries the database for the song title, id, artist, type, and genre, and sets the resutls to variable _songs_. It then renders template [index.html](#indexhtml), and passes in _songs_. then, [index.html](#indexhtml) displays the _songs_ data in a table. More details on that can be found in the [index.html](#indexhtml) section. 
Interestingly, the **"/"** route was actually the last one I completed. Originally, I had a **"/library"** route and library.html file that created a separate page to display the saved songs. I had some ideas that I might make the index page an introduction to the web app, or maybe a page where you could search either saved songs, or even search for chords or tabs through Google. Ultimately, I decided it was cleaner to just have the home page display the users saved songs. 

Next is the **"/login"** route. I copied this directly from the [CS50 Finance problem set](https://www.cs50.harvard.edu/x/2024/psets/9/finance/). The only difference is that instead of redirecting to an apology page, I opted to flash messages indicating that the user didn't provide a valid username or password. 

The **"/register"** route is largely the same as what I submitted for the [CS50 Finance problem set](https://www.cs50.harvard.edu/x/2024/psets/9/finance/). However, I did add the need for the user to select a security question. This sets up the ability for a user to reset their password if they ever forget. 
The route starts by setting the necessary variables. Most are being collected from the form on the [register.html](#registerhtml) page, but the _questions_ variable queries the security table on the database to pull back all of the available questions listed there. 
If the method is post, it validates that all of the information was entered into the form correctly, and then inserts a new user row into the users table of the database. 
If the method is get, it renders [register.html](#registerhtml), passing _questions_. 

The **"/logout"** route was also copied directly from [CS50 Finance problem set](https://www.cs50.harvard.edu/x/2024/psets/9/finance/). It simply clears the session, and redirects to **"/"**.

The **"/account"** route only supports the get method, and is only accessible if you are logged in. I queries the database for the current user's username to set the _username_ variable. Then it renders the [account.html](#accounthtml) template and passes in _username_.

The **"/password_reset"** route supports both get and post. It also requires that the user be logged in. This route is what allows a logged in user to reset their password from the [account.html](#accounthtml) page. 
If the method is post, it gathers the _oldPassword_, _newPassword_, and _confirmation_ from the form on [password_reset.html](#passwordresethtml). It then proceeds to make sure that all three fields were filled out in the form. After that, it queries the users table on the database for the logged in user, and checks that the _oldPassword_ they entered, when hashed, matches the hash saved for this user on the table. Finally, it confirms that the _newPassword_ and _confirmation_ match. If it successfully gets through all the validation, it updates the user row on the users table to have the new password. 
If the get method is used, it simply renders the [password_reset.html](#passwordresethtml) template.

The **"/forgot_password_u"** and **/"forgot_password"** work together to allow a user who isn't logged in to reset their password if they forgot it. To start, the **"/forgot_password_u"** route supports the get and post methods. 
If the get method is used, it renders the [forgot_password_username.html](#forgotpasswordusernamehtml) template. 
If post is used, it starts by setting the _username_ variable equal to the value pulled from the form in [forgot_password_username.html](#forgotpasswordusernamehtml). It validates that a username was entered in the form, then it queries the database using that username to confirm that the user actually exists. If it finds the user, queries the database to identify the user's security question, which it sets as variable _question_. It then sets _session\["temp_user_id\]_ equal to the user_id associated with the username that was entered. This creates a temporary session that isn't considered being logged in, but allows the user information to persist to the [forgot_password.html](#forgotpasswordhtml) page. Finally, it renders the [forgot_password.html](#forgotpasswordhtml) template and passes along the _question_ variable. 


The **"forgot_password"** route is similar to the **"password_reset"** route. Instead of requiring the user to enter their current password, it has the user answer the security question they chose when registering. 
If the get method is used, it renders the [forgot_password_username.html](#forgotpasswordusernamehtml) template. This makes sure that the user starts at the beginning of the forgot password flow. 
If the post method is used, it starts by gathering the _answer_, _newPassword_, and _confirmation_ variables from the form on [forgot_password.html](#forgotpasswordhtml). It validates that each field was populated, then queries the users table to get all of the user information for this user. Next, it checks to make sure the answer to the security question provided matches the answer given when the user registered. If it matches, it confirms that _newPassword_ and _confirmation_ match. If they match, it updates the database with the new password, and redirects to the **"/login"** route. 

The **"/new"** route is what lets the user add new songs to their library. It takes get and post methods. It requires that the user is logged in to access.  
If the get method is used, it queries the genre table to set the _genres_ variable, and queries the types table to set the _types_ variable. It then renders [new.html](#newhtml) and passes _genres_ and _types_. 
If the post method is used, it starts by collecting variables from the form in [new.html](#newhtml). It then validates that each field (except for artist) is populated. It also queries the genre and type tables in the database to validate that the selections for those fields in the form exist on the tables in the database. If all of the validation passes, it updates the database with the new song. If the artist field was populated, it populates the given artist. If it isn't populated, it leaves that blank, which causes the database to populate artist as the default value "No Artist". 

The **"/song/\<title\>_\<int:id\>"** route supports the get method. the song() function takes arguments title and id. This route displays a saved song from the database on the [song.html](#songhtml) page.
It starts by querying the database for song id, title, artist, song_text, type, and genre using the session user id, and the song id from the url. It sets the results of that query to variable _song_. It then validates that a song was found. If one was found, it renders the [song.html](#songhtml) and passes _song_. If a song isn't found in the database, it calls the error() function from [helpers.py](#helperspy) to display an error page saying "Song Not Found". 

The **"/song/\<title\>_\<int:id\>/edit"** supports the get and post methods. The user has to be logged in to access this route. The edit() function takes arguments title and id. This route allows the user to edit an existing song. 
If the get method is used, the database is queried for song info using the session user id and the song id. It stores that data to the _song_ variable. If a song is found, the genre and type tables are queried and the results are stored to variables _genres_ and _types_. The it renders [edit.html](#edithtml) and passes _song_, _genres_, and _types_. If a song isn't found, it calls the error() function to display a page with error "Song Not Found".
If the post method is used, it starts by setting variables using form input on [edit.html](#edithtml). It then validates that all fields were filled, and that they have valid entries. If it passes all the validation, it updates the songs table with the new information. 

The last route is **"/delete"**. This route allows the user to delete a song from the database. It only supports the post method. It starts by setting _id_ from form input. If it finds an id, it uses that id and the session user_id to find and delete the song from the songs table. It then flashes "Song Deleted" and redirects to **"/"**. If _id_ isn't found, it flashes "Error: id not found on song table" and redirects to **"/"**

### [helpers.py](helpers.py)

helpers.py contains two python functions that can be imported into [app.py](#apppy). It starts by importing redirect, render_templates, and session from flask, and importing wraps from functools. Then it defines two functions: **login_required()** and **error()**.
I copied **login_required()** directly from [CS50 Finance problem set](https://www.cs50.harvard.edu/x/2024/psets/9/finance/). It's used in [app.py](#apppy) routes to require that the user be logged in to access that route. It works by checking if there is a session user_id, and if there isn't it redirects the user to **"/login"**.
I based the **error()** function off of the apology function in [CS50 Finance problem set](https://www.cs50.harvard.edu/x/2024/psets/9/finance/). Instead of rendering a page with an image that had the error and message printed on it, I opted to simply display the error and message text in headers. The function takes two arguments, message, and code (code defaults to 400 if left empty). It then renders template [error.html](#errorhtml) and passes in code and message. 

### [chord-scroll.db](chord-scroll.db)

This is the database that stores all the data for the ChordScroll web app. It contains 5 tables (_users_, _security_, _songs_, _type_, _genre_, and _sqlite\_sequence_), 3 unique indexes (_username_, _types_, and _genres_) and 1 non-unique index (_titles_). Every table except _sqlite\_sequence_ has an id field that is an integer and primary key for that table. 

The _users_ table stores all the user information for logging in and resetting a forgotten password. It has the following columns: id, username, hash (to store the hashed password), security_question (a foreign key to the id on the _security_ table, it stores the security question the user selected when registering), and security_answer_hash (stores the hash of the users answer to the security question).

The _security_ table has two columns: id and question. The question column stores all the security questions that a user can choose from when registering an account. 

The _songs_ table stores the songs that users save to their library. It has the following columns: id, title, artist (defaults to "No Artist"), song_text (this is the actual tabs/chords/lyrics etc being saved), type_id (this is a foreign key to the id field on the _type_ table), genre_id (this is a foreign key to the id field on the _genre_ table), and user_id (this is a foreign key to the id field on the _users_ table). 

The _type_ table stores all the type options a user can choose from for a song. It has an id column, and type column that stores the types. It has 4 rows: Chords, Tabs, Lyrics, and Other. 

The _genre_ table stores all the genre options a user can choose from for a song. It has an id column, and genre column that stores the genres. It has 8 rows: Blues, Country, Folk, Jazz, Pop, Rock, Singer-Songwriter, and Other. 

The _sqlite\_sequence_ table is one that sqlite creates automatically if any of the user created tables have autoincrementing fields. This table simply keeps track of the autoincrementing for each table that uses it, so that the database knows what id to use for the next row that gets written. 

### [style.css](static/style.css)

This is my primary CSS file. I used bootstrap for most of my styling, as well as some inline styling here and there, so there's not a lot in style.css. It starts by setting the scroll-behavior for _html_ (so every page on the web app) to smooth. This is important for the auto-scroll functionality on the [song.html](#songhtml) page. The only other selector is for the class _scroll-buttons_. This class is set to position: sticky, top: 100px, width: max-content, and margin-left: auto. This is all to style the auto scroll buttons on the [song.html](#songhtml) page. 

### [layout.html](templates/layout.html)

This file contains the html boilerplate and navbar that is needed for every html file in the web app. Instead of copying and pasting this code to each file, I've created this layout file, and then use Jinja to extend this file on each other html file, and Jinja blocks to set placeholders which get populated in each individual html file. 

### [account.html](templates/account.html)

