import chapeau

def age_plus_five(request, client):
	print request
	my_dict = request['body']
	if 'age' in my_dict:
		my_dict['age'] = int(my_dict['age']) + 5
	return chapeau.render(client, 'views/passing_vars.html', my_dict)



routing_dictionary = {
					'/home' : 'views/user_info.html', 
					'/welcome' : age_plus_five  }

chapeau.go(routing_dictionary)

