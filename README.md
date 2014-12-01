### INTRODUCTION

Chapeau is a very lightweight web framework build primarely for learning purposes.  Chapeau can do for you: 

- it includes a web server, written using the Python socket Module
- parses raw http requests 
- POST and GET request handling
- basic string replacement in html templates
- allows users to to specify any desired http headings in request response
- serves apps on local host on port 9999

###### THE COMPONENTS OF A CHAPEAU WEB APP 
Every Chapeau web app must contain the following components: 

1. `import chapeau`
2. define a Python dictionary called `routing_dictionary`
3. call: `chapeau.go(routing_dictionary)`

A full, working, Chapeau web application could be as simple as: 

```
import chapeau
routing_dicitonary = {'/' : 'path/to/file/hello_world.html'}
chapeau.go(routing_dictionary)
```

As long as the file 'hello_world.html' exists in the path 'path/to/file' then this app is completely functional and will simply render 'hello_world.html' in the client's browser. 

### ROUTING DICTIONARY 

This section will discuss how to define the routing dictionary, and the options that users have in doing so.  In particular we will discuss: 

* Routing to static html pages.
* Passing variables to pre-determined html pages.
* Routing to functions. 
* Obtaining more information about the requests object. 
* Storing and retreive data. 


######ROUTING TO STATIC HTML PAGES

This is the same as the initial hello_world example.  Here is another example with more than one URL: 
```
routing_dictionary = {
                '/'  : 'path/to/file/hello_world.html',	          '/welcome'    : 'path/to/file/welcome.html',
	'/goodbye'   	: 'path/to/file/goodbye.html'
	                    }
```


###### BASIC VARIABLE PASSING 
Cheapeau makes it very easy to pass user input from one page to the next.  We often refer to these kinds of apps as 'mad-libbs-style-apps'.  Here is a very simple mad-libs-style-app that prompts the user for their Name, Surname and age, and upon submission, redirects the user to a page that says "Welcome, (user's Name) (user's Surname).  You are (user's age) years old.":

```python
import chapeau
routing_dictionary = {'/'   : 'views/user_info.html', 
		    	'/welcome'  : 'views/welcome.html'  }
chapeau.go(routing_dictionary)
``` 

Here is the corresponding the "user_info.html" file, which is stored in the views subdirectory.  (Note: You don't have to store your html files in a sub-directory caled views to use chapeau. Just make sure you specify the appropriate path to your html file.)

```html
<html>
<meta charset="utf-8">
<title>A short quiz</title>
	<body>
	<h2>
		You will be asked 5 questions.
		Please answer them to the best of your ability.
	</h2>
	<form method = 'post' action = '/welcome' >
		<p>
	Name: <input type = 'text' name='name' />
		</p>
		<p>
	Age: <input type='text' name='age' />
		</p>
		<p>
	Surname: <input type='text' name='surname' />
		</p>
		<p>
	<input type='submit' value='Submit' />
		</p>
	</form>
</body>
</html>
```
And here is the "welcome.html" file:

```html
<html>
<meta charset="utf-8">
<title> Hello </title>
<h2> Hello, %(name)s %(surname)s.  You are %(age)s years old. </h2>
</html>
```

Of importance here is that **the input names in our "user_input.html" file correspond to the variable names in our "welcome.html" file**.  To pass variables from one page to the next, we type `%(input_name)s` into the html file which will receive the input, and Chapeau will take care of the rest. 

Remember also that the html form needs to indicate which URL should be routed to upon submission.  In our example, we have indicated that "action = '/welcome'". 

Here we have implimented our form to submit a POST request but it should be mentioned that chapeau also allows user input to be submitted through GET requests.

###### ROUTING TO FUNCTIONS 

In the mad-libbs-style-app, the data substition is done for you completely, and so you, as a user of Chapeau, never handle the variables directly. While this is nice for mad-libbs-style-apps, it can be extremely limiting as well.  Functions to the rescue! 

If you'd like to gain a little more control over your program we suggest using functions in the routing dictionary.  To do this, simply make the value of a specific URL be the name of a function which you have previously defined.  Here is what you need to know about the function: 

* Any function you put into the routing dictionary must be pre-defined by you, the user of Chapeau. 
* Your functions you MUST receive two variables as input: 
 - The first variable will be the http request, parsed, and stored in a dictionary.  
 - The second variable will be an object representing the client with which you are communicating.  
* You're function MUST return the function `chapeau.render(client, path, input, header)`.  
 - Here the `client` should be exactly the same as the second parameter that your function takes in.  
 - The `path` specifies the location of a particular html file which you hope to render.  
 - The `input` is a dictionary of variables and values we wish to pass into our html page.  If no variables are to be passed, set `input = {}`.   
 -  `headers` is an otional parameter in the form of a dictionary..  If you would like to pass any extra headers to the client, you may specify them here as key value pairs.

Let's begin with a very simply example to illustrate how a simple function might work. The following app will ask the user for their name and age, and then routes them to a page that tells them how old they'll be in 5 years.  

The app: 
```python 
import chapeau
def age_plus_five(request, client):
	my_dict = request['body']
	print my_dict, 'dict'
	if 'age' in my_dict:
		my_dict['age'] = int(my_dict['age']) + 5
	return server.render(client, 'templates/passing_vars.html', my_dict)
routing_dictionary = {
					'/home' : 'templates/user_info.html', 
					'/welcome' : age_plus_five  }

chapeau.go(routing_dictionary)
```

The "user_info.html" and the "passing_vars.html" pages will be the same as in the previous example.  The only difference is the app itself.  Things to pay attention to here: 

* If variables are being passed through a GET request, then they will be stored as key value pairs in `reqest['query']`.  
* If variables are being passed through a POST request, then they will be stored as key value pairs in `request['body']`.

Since our form sent a POST request, we looked in `request['body']`, found the value corresponding to age, and added 5 to it. 

######  MORE INFORMATION ABOUT REQUESTS 
This section describes in greater detail what the `requests` object is that is being passed to a function.  Requests is a dictionary with 5 keys: `'body'`, `'query'`, `'path'`, `'type'`, `'headers'`.  

* The value of `'body'` is a dictionary containing any key value pairs received from the user through a POST request
* The value of `'query'` is a dictionary containing any key value pairs received from the user through a GET request
* The value of `'path'` is a URL 
* The value of `'type'` is either GET or POST, depending on which kind of request is being made. 
* The value of `'headers'` is a dictionary containing all of the headers in the received request and the values of these headers. 

Here is what the requests object looks like in the POST request of the  previous example:  `{'body': {'age': '20', 'surname': 'Brown', 'name': 'Mary'}, 'path': '/welcome', 'query': {}, 'type': 'POST', 'headers': {'Origin': 'http://10.0.7.65:9999', 'Content-Length': '30', 'Accept-Language': 'en-US,en;q=0.8', 'Accept-Encoding': 'gzip,deflate,lzma', 'Connection': 'keep-alive', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 OPR/25.0.1614.71', 'Host': '10.0.7.65:9999', 'Referer': 'http://10.0.7.65:9999/home', 'Cache-Control': 'max-age=0', 'Content-Type': 'application/x-www-form-urlencoded'}}`.


###### STORING DATA 
How can we store data to be retrieved later?  It might be tempting to make global variables in your app, which you're functions can update and then access later. However global variables will not allow for data to be stored separately for more than one client. Here we will discuss how Cookies can be used in a Chapeau app to store data.

Let's start with an example:
Suppose we want to impliment a quiz which asks the user one question per page.  Before rendering the results page we want to retreive all of the user's answers at once in order to analyze them and determine the result.  Here's how an app might look in this situation: 

```python
import chapeau
user_answers = {}

def first(request, client):
	print request
	if 'question1' in request['body']:
		header = {'Set-Cookie': 'question1=%s' %request['body']['question1']}
		chapeau.render(client, 'views/question_2.html', user_answers, header)
	else:
		chapeau.render(client, 'views/question_1.html', user_answers)

def second(request, client):
	if 'question2' in request['body']:
		header = {'Set-Cookie': 'question2=%s' %request['body']['question2']}
		chapeau.render(client, 'views/question_3.html', user_answers, header)
	else:
		chapeau.render(client, 'views/question_2.html', user_answers)

def third(request, client):
	if 'question3' in request['body']:
		cookies = request['headers']['Cookie'].split('; ')
		for cookie in cookies:
			temp = cookie.split('=')
			user_answers.update({temp[0] : temp[1]})
		user_answers.update({'question3' : request['body']['question3']})
		result = make_decision(user_answers)
		chapeau.render(client, 'views/result.html', result)
	else:
		chapeau.render(client, 'views/question_3.html', user_answers)

def make_decision(user_answers):
	if user_answers['question3'] != 'NYC':
		return 'stupid-head.'
	elif user_answers['question2'] == 'gummybears':
		return 'SUPERHERO!'
	return 'normal human...'
	
routing_dict = {'/welcome' : 'views/welcome.html',
				'/first_question': 'views/question_1.html',
				'/first_question_post': first,
				'/second_question':  'views/question_2.html',
				'/second_question_post': second,
				'/third_question':  'views/question_3.html',
				'/third_question_post': third}

chapeau.go(routing_dict)
```

And here are the html pages: 
welcome.html:
```html
<html>
<head>
<title> Buzz-Feed Style Quiz </title>
<style>
div {
	float: center;
	width: 100px;
	height: 50px;
	color: blue;
}

</style>
</head>
<body>
Press the button to take a quiz
<div> <a href="/first_question"> Start </a> </div>
</body>
</html>
```

question_1.html
```html
<html>
<head>
<title> Question 1 </title>
</head>
<body>
<h1> First Question </h1>
<h2> What is your favorite fruit? </h2>
<form method = 'post' action = '/first_question_post'>
<input type="radio" name="question1" value="banana">Banana<br>
<input type="radio" name="question1" value="orange">Orange<br>
<input type="radio" name="question1" value="grapes">Grapes<br>
<input type="radio" name="question1" value="mango">Mango<br>
<input type ="submit" value="Submit">
</body>
</html>
```

question_2.html
```html
<html>
<head>
<title> Question 2 </title>
</head>
<body>
<h1> Second Question </h1>
<h2> Whats your favorite candy? </h2>
<form method = 'post' action = '/second_question_post'>
<input type="radio" name="question2" value="licorice">Licorise<br>
<input type="radio" name="question2" value="lollipop">Lolli Pop<br>
<input type="radio" name="question2" value="gummybears">Gummy Bears<br>
<input type="radio" name="question2" value="swedishfish">Swedish Fish<br>
<input type ="submit" value="Submit">
</body>
</html>
```

question_3.html
```html
<html>
<head>
<title> Question 3 </title>
</head>
<body>
<h1> Question 3 </h1>
<h2> Whats ideal vacation spot? </h2>
<form method = 'post' action = '/third_question_post'>
<input type="radio" name="question3" value="disneyland">Disney Land<br>
<input type="radio" name="question3" value="beach">Beach Holidy<br>
<input type="radio" name="question3" value="paris">Paris<br>
<input type="radio" name="question3" value="NYC">New York City<br>
<input type ="submit" value="Submit">
</body>
</html>
```

result.html
```html
<html>
<head>
<title> Result </title>
</head>
<body>
<h1> Results </h1>
<h2> Based on a sensitive scientific method, we have concluded that you are a %s </h2>
</body>
</html>
```

Lets walk through what happens as this app runs.  
* First, a client visits the main page.  
* When the client presses the start button they are redirected to the 'question_1' page.  
* When they submit their answers to this form, the url changes to '/first_question_post', and we are routed to the first function.  
* Assuming that the client has actually answered the question (as opposed to simply clicking submit without answering the question), then the first condition in the function will be satisfied. The program will set a header to be "Set-Cookie", which will contain the clients answer to question 1.  This header is included in the render function where we re-direct to question 2.  
* Then the client answers question 2, presses submit, and we do the same thing for question 2.  
* Then when we get to question 3, we find the cookies header in the requests object, and find the answers to the previous two questions. These answers and the answer to question 3 are saved in a dictionary called `user_input`.
* `user_input` is passed to the `make_decision` function which analyses these answers to determin a result, either 'stupid-head',  'superhero' or 'normal human'.  This result is then sent back to the `third` function and saved as `result`.  
* The third function then renders the result page to the client with the appropriate quiz result by calling `render(client,'views/result.html', result)`. 
