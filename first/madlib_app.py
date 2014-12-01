import chapeau


routing_dictionary = {'/' : 'views/user_info.html', 
					'/get_user_info' : 'views/get_user_info.html', 
					'/welcome' : 'views/passing_vars.html'  }

chapeau.go(routing_dictionary)

