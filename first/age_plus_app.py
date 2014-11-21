import server


def age_plus_five(dict):
	print dict, 'dict in function'
	if 'age' in dict.keys():
		dict['age'] = int(dict['age']) + 5
	return dict



routing_dictionary = {'/' : 'templates/index.html',
					'/home' : 'templates/user_info.html', 
					'/get_user_info' : 'templates/get_user_info.html', 
					'/welcome' : (age_plus_five, 'templates/passing_vars.html')  }

server.go(routing_dictionary)

