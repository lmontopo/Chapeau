import server


routing_dictionary = {'/' : 'templates/index.html',
											'/home' : 'templates/user_info.html', 
											'/get_user_info' : 'templates/get_user_info.html', 
											'/welcome' : 'templates/passing_vars.html'  }

server.go(routing_dictionary)

