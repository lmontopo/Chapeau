import chapeau

user_answers = {}

def first(request, client):
	if 'question1' in request['body'].keys():
		header = {'Set-Cookie': 'question1=%s' %request['body']['question1']}
		chapeau.render(client, 'views/question_2.html', user_answers, header)
	else:
		chapeau.render(client, 'views/question_1.html', user_answers)

def second(request, client):
	if 'question2' in request['body'].keys():
		header = {'Set-Cookie': 'question2=%s' %request['body']['question2']}
		chapeau.render(client, 'views/question_3.html', user_answers, header)
	else:
		chapeau.render(client, 'views/question_2.html', user_answers)


def third(request, client):
	if 'question3' in request['body'].keys():
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