import server

user_answers = {}

def first(dict, client):
	global user_answers
	if question1 in dict.keys():
		user_answers.update(dict)
		print user_answers, 'user answers'
		render(client, 'views/question_2.html' user_answers)
	else:
		render(client, 'views/question_1.html', user_answers)


# def func(dict):
# 	return "SUPERHERO!"

routing_dict = {'/welcome' : 'views/welcome.html',
				'/first_question': first,
				'/second_question': (agregator, 'views/question_2.html'),
				'/third_question':  (agregator, 'views/question_3.html')}

server.go(routing_dict)