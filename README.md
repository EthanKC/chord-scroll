# ChordScroll
### Video Demo: https://youtu.be/SE1FmSIF9Ek
### Description: 
A flask web app that let's users save guitar chords or tabs, and then auto scroll at their chosen speed. The purpose is to allow the user to play through a song without having to stop to scroll down. 

### Introduction:
I'm an amateur guitar player. There are several sites that contain great chords and tabs, but for all of them you have to have a membership to use auto-scroll functionality. I wanted to make something I can use to autoscroll without having to pay. I opted to require that users register and log in for a very specific reason. Sites like [Ultimate Guitar](https://www.ultimate-guitar.com) provide an extensive library or tabs and chords that can be accessed without registering. However, they actually pay royalties to record companies to be able to store and share those tabs. To get around that, each user of ChordScroll creates and maintains their own library of songs, that is only accessible to them.

## Files
### [app.py](app.py)
The main file of the web app, this lays out all of the url routes that can be accessed for the web app. At the top, I've imported needed functions from the cs50, flask, flask_session, and werkzeug.security libraries. I've also imported a couple of functions from my [helpers.py](#helperspy) file. 

Below that I do some basic configuration of the app. The secret_key is necessary to allow the use of **flash()**. The app.config functions set up the session to use the filesystem instead of signed cookies. The _db_ variable is set to use my chord-scroll.db. And the @app.after_request ensures responses aren't cached. 

The first route is **"/"**, and it only uses the get method. It uses the @login_required from [helpers.py](#helperspy) to indicate that this route is only accessible if the user is logged in. The **index()** function queries the database for the song title, id, artist, type, and genre, and sets the resutls to variable _songs_. It then renders template [index.html](#indexhtml), and passes in _songs_. then, [index.html](#indexhtml) displays the _songs_ data in a table. More details on that can be found in the [index.html](#indexhtml) section. 
Interestingly, the **"/"** route was actually the last one I completed. Originally, I had a **"/library"** route and library.html file that created a separate page to display the saved songs. I had some ideas that I might make the index page an introduction to the web app, or maybe a page where you could search either saved songs, or even search for chords or tabs through Google. Ultimately, I decided it was cleaner to just have the home page display the users saved songs. 

Next is the **"/login"** route. I copied this directly from the [CS50 Finance problem set](https://www.cs50.harvard.edu/x/2024/psets/9/finance/). The only difference is that instead of redirecting to an apology page, I opted to flash messages indicating that the user didn't provide a valid username or password. 

The **"/register"** route is largely the same as what I submitted for the [CS50 Finance problem set](https://www.cs50.harvard.edu/x/2024/psets/9/finance/). However, I did add the need for the user to select a security question. This sets up the ability for a user to reset their password if they ever forget. 
The route starts by setting the necessary variables. Most are being collected from the form on the [register.html](#registerhtml) page, but the _questions_ variable queries the security table on the database to pull back all of the available questions listed there. 
If the method is post, it validates that all of the information was entered into the form correctly, and then inserts a new user row into the users table of the database. 
If the method is get, it renders [register.html](#registerhtml), passing _questions_. 

The **"/logout"** route was also copied directly from [CS50 Finance problem set](https://www.cs50.harvard.edu/x/2024/psets/9/finance/). It simply clears the session, and redirects to **"/"**.

The **"/account"** route only supports the get method, and is only accessible if you are logged in. I queries the database for the current user's username to set the _username_ variable. Then it renders the [account.html](#accounthtml) template and passes in _username_.

The **"/password_reset"** route supports both get and post. It also requires that the user be logged in. This route is what allows a logged in user to reset their password from the [account.html](#accounthtml) page. 
If the method is post, it gathers the _oldPassword_, _newPassword_, and _confirmation_ from the form on [password_reset.html](#password_resethtml). It then proceeds to make sure that all three fields were filled out in the form. After that, it queries the users table on the database for the logged in user, and checks that the _oldPassword_ they entered, when hashed, matches the hash saved for this user on the table. Finally, it confirms that the _newPassword_ and _confirmation_ match. If it successfully gets through all the validation, it updates the user row on the users table to have the new password. 
If the get method is used, it simply renders the [password_reset.html](#password_resethtml) template.

The **"/forgot_password_u"** and **/"forgot_password"** work together to allow a user who isn't logged in to reset their password if they forgot it. To start, the **"/forgot_password_u"** route supports the get and post methods. 
If the get method is used, it renders the [forgot_password_username.html](#forgot_password_usernamehtml) template. 
If post is used, it starts by setting the _username_ variable equal to the value pulled from the form in [forgot_password_username.html](#forgot_password_usernamehtml). It validates that a username was entered in the form, then it queries the database using that username to confirm that the user actually exists. If it finds the user, queries the database to identify the user's security question, which it sets as variable _question_. It then sets _session\["temp_user_id\]_ equal to the user_id associated with the username that was entered. This creates a temporary session that isn't considered being logged in, but allows the user information to persist to the [forgot_password.html](#forgot_passwordhtml) page. Finally, it renders the [forgot_password.html](#forgot_passwordhtml) template and passes along the _question_ variable. 


The **"forgot_password"** route is similar to the **"password_reset"** route. Instead of requiring the user to enter their current password, it has the user answer the security question they chose when registering. 
If the get method is used, it renders the [forgot_password_username.html](#forgot_password_usernamehtml) template. This makes sure that the user starts at the beginning of the forgot password flow. 
If the post method is used, it starts by gathering the _answer_, _newPassword_, and _confirmation_ variables from the form on [forgot_password.html](#forgot_passwordhtml). It validates that each field was populated, then queries the users table to get all of the user information for this user. Next, it checks to make sure the answer to the security question provided matches the answer given when the user registered. If it matches, it confirms that _newPassword_ and _confirmation_ match. If they match, it updates the database with the new password, and redirects to the **"/login"** route. 

The **"/new"** route is what lets the user add new songs to their library. It takes get and post methods. It requires that the user is logged in to access.  
If the get method is used, it queries the genre table to set the _genres_ variable, and queries the types table to set the _types_ variable. It then renders [new.html](#newhtml) and passes _genres_ and _types_. 
If the post method is used, it starts by collecting variables from the form in [new.html](#newhtml). It then validates that each field (except for artist) is populated. It also queries the genre and type tables in the database to validate that the selections for those fields in the form exist on the tables in the database. If all of the validation passes, it updates the database with the new song. If the artist field was populated, it populates the given artist. If it isn't populated, it leaves that blank, which causes the database to populate artist as the default value "No Artist". 

The **"/song/\<title\>_\<int:id\>"** route supports the get method. the **song()** function takes arguments title and id. This route displays a saved song from the database on the [song.html](#songhtml) page.
It starts by querying the database for song id, title, artist, song_text, type, and genre using the session user id, and the song id from the url. It sets the results of that query to variable _song_. It then validates that a song was found. If one was found, it renders the [song.html](#songhtml) and passes _song_. If a song isn't found in the database, it calls the **error()** function from [helpers.py](#helperspy) to display the [error.html](#errorhtml) page saying "Song Not Found". 

The **"/song/\<title\>_\<int:id\>/edit"** supports the get and post methods. The user has to be logged in to access this route. The **edit()** function takes arguments title and id. This route allows the user to edit an existing song. 
If the get method is used, the database is queried for song info using the session user id and the song id. It stores that data to the _song_ variable. If a song is found, the genre and type tables are queried and the results are stored to variables _genres_ and _types_. The it renders [edit.html](#edithtml) and passes _song_, _genres_, and _types_. If a song isn't found, it calls the **error()** function to display a page with error "Song Not Found".
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

It starts with with the head element, in which are some meta tags to make the site mobile responsive. Specifically, these are required for bootstraps responsiveness to work. 
Next, I link to the [Bootstraps stylesheet](https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH) and the [Bootstrap javascript file](https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz), both of which you can find more information on at https://getbootstrap.com/. Then I link to the [Quill Realtime Editor style sheet](https://cdn.jsdelivr.net/npm/quill@2.0.2/dist/quill.snow.css) (find more info about Quill at https://quilljs.com/), and finally my own [style.css](#stylecss).
The final thing in the head is the title element, which lists the title as "ChordScroll: {% block title %}{% endblock %}. This sets what will show as the page title on the tabs, and the jinja block allows each page to show a different title. 

After the head element is the body element. It starts with creating the navbar. I copied this from [CS50 Finance problem set](https://www.cs50.harvard.edu/x/2024/psets/9/finance/), then adjusted it to fit my needs for this site. First, the word "ChordScroll" is set as a link to **"/"**. This acts as a sort of icon for the site, and functionally when pressed takes you to the home page. It is located to the far left on the navbar. 

The rest of the navbar elements determine the rest of the links in the navbar. It uses jinja to create an if loop that says if there is a session user_id (meaning a user is logged in), display one set of links. If there isn't a session user_id (meaning a user isn't logged in) display a different set of links. These links are all built as unordered lists, with each entry in the list being a link. 

If there is a session user_id, the first unordered list contains two links: "Home" and "New". This list has bootstrap class me-auto, which sets the margin to the end of the list, functionally setting the elements to the start of the container. This results in "Home" being directly to the right of "ChordScroll" on the far left of the navbar, and "New" being directly to the right of "Home". "Home" links to **"/"**, and "New" links to **"/new"**. 
The next unordered list also has two links: "Account" and "Log Out". This list has a bootstrap class ms-auto, whicch sets the margin to the start of the list, functionally setting the elements to the end of the container. This results "Log Out" being at the far right of the navbar, and "Account" being directly to the left of it. "Account" links to **"/account"**, and "Log Out" links to **"/logout"**.  

If there isn't a session user, the first unordered list is just the "Home" link, and it directs to **"/login"**. The second unordered list has "Register" which directs to **"/register"** and "Login" which directs to **"/loging"**

After the navbar is some jinja code that sets up to post flashed messages at the top of the page, just below the navbar. 

Finally, the main element is a container, within which is a jinja block. This is where the bulk of the page specific code will go in all the other template pages. 

### [index.html](templates/index.html)

This is the home page of the app. It starts by setting the title to "Home" in the jinja title block. Then it has a table to display all of the songs in the users library. First, above that table is a table with no headers, and 4 columns that each contains an input element. In order, the elements ar id'd as titleFilter, artistFilter, genreFilter, and typeFilter. They all call the **filter()** function onkeyup. The **filter()** function, which I pulled from [W3Schools](https://www.w3schools.com/howto/howto_js_filter_table.asp) and modified, is defined at the end of the page. It checks the text input into an input field, and hides any rows in the main songTable that don't match the filter. It takes two arguments: elementId, to identify which input field to pull the text from, and index, to tell it which column in the songTable to compare that text to. 
I considered also adding sorting functionality to the table, but opted not to due to the complexity. 

After the filter table is the songTable. This table has 6 headers. The first 4 are "Title", "Artist", "Genre", and "Type". The last two are empty. The body of the table displays a row for each song saved to the songs table for the logged in user. It does this using a jinja for loop to loop through each row passed over from [app.py](#apppy) in the _songs_ variable. The first column of each row contains the title. The title is also a link to the **"/song/\<title\>_\<int:id\>"** route in [app.py](#apppy), except that \<title\> and \<int:id\> are populated by song.title and song.id using the jinja for loop. This turns the title into a link the user can click to display the saved song. 
The second column is the artist name, third column is the genre, and fourth is the type. The fifth column is a button with the text "Edit" that directs the user to **"/song/\<title\>_\<int:id\>\/edit"**, and link with the title link the \<title\> and \<int:id\> fields are populated by the for loop. This button opens the song in the [edit.html](#edithtml) page to allow the user to edit the saved song. Finally, the fifth column is a "Delete" button that allows the user to delete that song by calling the "**"/delete"** route with the value song.id. 

### [new.html](templates/new.html)

This page allows the user to input and save a new song to their library. It sets the title to "New" in the jinja title block. In the main block is a form with several divs. The form has an action that calls **"/new"** from [app.py](#apppy) with a method of post. It also calls the **submitForm()** function onsubmit. At the bottom of the page, you can see that the **submitForm()** function sets _content_ equal to the contents of the Quill RTE, then sets the value of hiddenInput equal to contents. This is effectively copying the contents of Quill RTE to a format that can be saved to the database. 

The first div consists of the label "Title" and a text input field. 

The second div has the lable "Artist" and a text input field. 

The third div has label "Genre". It then has a select, with the first option disabled "Genre", and the rest of the options are filled with the rows from the genre table. This is done using a jinja for loop to loop through each row passed from [app.py](#apppy) in _genres_. 

The fourth div is the same as the third, except that instead of "Genre" and the genre table, it's "Type" and the type table. 

The fourth div is the Quill RTE, with the label "Song". I made the decision to use an RTE instead of a textarea element because the RTE allows the user to format the text, which is important when you're saving chords or tabs. 

After that last div, but still in the form, is a save button. 

At the end of the block is a script element. Inside script is the **submitForm()** function already described, and some code copied from the [Quill](https://quilljs.com/docs/quickstart) website that initializes the Quill editor on the page. 

### [edit.html](templates/edit.html)

This page allows the user to edit an existing saved song. It starts by setting the title to "Edit". Next is a form that is essentially the same as [new.html](#newhtml). The difference is that the action of the form calls route **"/song/{{ song.title }}_{{ song.id }}/edit"**, and each field is pre-populated with the information already in the database for the saved song. 
At the end of the page is the same script element as [new.html](#newhtml).

### [song.html](templates/song.html)

This is the the most important page of the app. It displays a saved song, and has the auto-scroll functionality that the app is built for. 
It starts by setting the title of the page equal to the song title, which is populated dynamically using a jinja placeholder. 
The main block begins with an h1 element with the song title, and h3 element with the artist, and an h6 element with the genre and type. These are all populated using jijna placeholders that pull from the _song_ variable passed from [app.py](#apppy). Next is an "Edit" button and a "Delete" button that are built the same as the edit and delete buttons in [index.html](#indexhtml). 

Below that is a div with the "scroll-buttons" class. That class is styled in [style.css](#stylecss) to make it sticky and on the right side of the screen. This means that as you scroll, this div will stay with you on the right side. The dive is made up of a form and two buttons. The form contains a label "Scroll Speed" and a number input that defaults to 5, and has a minimum value of 1. The first button is "Scroll" and the second button is "Stop". 

Skipping to the script element at the end of the page, we see the javascript that allows the scroll buttons to work. The **scroll()** function gets the number from the scrollSpeed input. It then uses **window.scrollBy()** to vertically scroll the number of pixels specified in the scrollSpeed input. Lastly, it sets _globalID_ to requestAnimationFram(scroll). By using an animation frame, it helps the scrolling to be more smooth. 

The **stopScroll()** function simply cancelse the globalID animation frame. 

Above both of these functions are 3 listeners. The first listens for the scroll button to be clicked, and when it is it calls the **scroll()** function. The second listener listens for the stop button to be clicked, and when it is it calls the **stopScroll()** function. The third listener uses the compares the pageYoffest with the scrollHeight - window.innerHeight to listen for when you get to the bottom of the page. When the bottom of the page is reached, it calls the **stopScroll()** function. 

Jumping back up to the html, just below the scroll buttons is a div with a p element. Inside that p element is jinja placeholder song.song_text | safe. This displays the saved song text with the saved formatting. 

### [account.html](templates/account.html)

This is a relativelt simple page. It displays the username for the logged in user, and provdes a password reset button to allow them to change their password. To start, it sets the title in the jinja title block to "Account". In the jinja main block, there's a table with two columns. The first header is "Username". and the second header is blank. Then there is one row, and the first column is populated by the logged in users username using a jinja placeholder. The second column is a password reset button that calls the **"/password_reset"** route in [app.py](#apppy).

### [login.html](templates/login.html)

The first page any user sees, this allows registered users to login. It also has a "Forgot Password" button. 
It starts by setting the title to "Log In" in the jinja title block.
In the main block, it has two forms. The first has an action that calls the **"/login"** route in [app.py](#apppy) with a method of post. The form has two inputs and a button. The first input is a text field named "username". The second input is a password field named "password". The button is a submit button with text "Log In". 

The second form has an action that calles the **"/forgot_password_u"** route in [app.py](#apppy). It then has a button with the text "Forgot Password". 

### [register.html](templates/register.html)

This page allows the user to register an account. It starts by setting the title to "Register". 
The entire main block is a form, with an action of **"/register"** and a method of post. The first input is a username text field. Next is a password field, followed by a confirm password field. After that is a select element named "securityQuestion". This allows the user to select from a series of security questions. The options are populated using a jinja for loop to loop through the rows pulled from the database in [app.py](#apppy) and passed over using the _questions_ variable. 
After the security question is a text input field named "securityAnswer". The input for this field will be hashed and saved to the user table. Together with the question, this allows a user who has forgotten their password to reset their password. 
Finally, the form ends with a submit button with the text "Register".

### [password_reset.html](templates/password_reset.html)

This page allows a logged in user to reset their password. It consists of a single form, with an action of **"/password_reset"** and a method of post. Following that, there are 3 inputs and a button. 
The first input is the "Old Password" field, where you enter you current password as a security measure. The second input is "New Password", and the third input is "Confirmation". This helps to ensure there isn't a typo in your new password. Finally, the button is a submit button with the text "Reset Password". 

### [forgot_password_username.html](templates/forgot_password_username.html)

This page is extremely simply, and exists only to collect the username to set up the [forgot_password.html](#forgot_passwordhtml) page. It consists of a single form, with action **"/forgot_password_u"**, method of post. The input field is a text field named "Username". That's followed by a submit button with the text "Submit". 

### [forgot_password.html](templates/forgot_password.html)

Another simple page, though not as simple as [forgot_password_username.html](#forgot_password_usernamehtml). This page again conists of a single form, with action **"/forgot_password" and method post. It's set up exactly the same as [password_reset.html](#password_resethtml), except that instead of taking "Old Password" as the security validation, it presents the security question that the user chose at registration, and then compares their answer to their saved answer in the database. But after that, the "New Password" and "Confirmation" inputs, and the "Reset Password" button, are the same as [password_reset.html](#password_resethtml).

### [error.html](template/error.html)

After a series of simple pages, this last page is the simples. The title is "Error {{ code }}", which allows for the code to be dynamically populated by whatever is passed as the _code_. The main block consists of an h2 element that is also "Error {{ code }}", and an h3 element that is "{{ message }}", allowing it to be dynamically populated by whatever is passed as the _message_ variable. This page gets rendered when the **error()** from [helpers.py](#helperspy) gets called. 
