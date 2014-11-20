#http server.py - this makes it so that Susan can see what I write to her in her browser. 
import socket 
import threading
import pdb
import urllib

#------- Receive messages from Clients ----------
def listen(clientsocket):
	msg = clientsocket.recv(1000)
	if msg:
		request = separate(msg)
		if request['type'] == "GET":
			get(clientsocket, request)
		if request['type'] == "POST":
			post(clientsocket, request)
			

# ------ Handles get requests ------- 
def get(clientsocket, request):
	if request['path'] in routing_dictionary.keys():
		page = routing_dictionary[request['path']]
	else:
		page = 'templates/sorry.html'
	read_file = open(page, 'r')
	read_text = read_file.read()
	read_file.close()
	
	return render(clientsocket, read_text)


# ------- Handles post requests --------
def post(clientsocket, request):
	message_file = open('templates/passing_vars.html', 'r')
	message_text = message_file.read()
	message_file.close()
	new_message = message_text %request['body']
	return render(clientsocket, new_message)


# ----- sends http msg and page to client socket, then closes socket -----
def render(clientsocket, new_msg):
	clientsocket.send('HTTP/1.0 200 OK\n\n')
	clientsocket.send(new_msg)
	clientsocket.close()


def separate(msg):
	msg = msg.split(' ')
	request_type = msg[0]
	full_path = msg[1]
	
	if full_path.find('?') > 0:
		full_path = full_path.split('?')
		path = full_path[0]
		query = parse_function(full_path[1])
		print query
	else:
		path = full_path
		query = {}

	raw_body = msg[-1]
	start = raw_body.find("\r\n\r\n") + 4
	body = parse_function(raw_body[start:])

	separate_request = { 'type': request_type, 'path': path, 'query': query, 'body': body }
	#print separate_request
	return separate_request

# ------ Parses raw request to find user input ------ 
def parse_function(data):
	parsed_data = {}

	while len(data) > 0:
		start_of_input = data.find('=') + 1
		end_of_input = data.find('&')
		data_key = data[0:start_of_input - 1]
		if end_of_input > 0:

			data_value = data[start_of_input:end_of_input]
			data = data[end_of_input + 1:]
		else:
			data_value = data[start_of_input:]
			data = ''
		data_value = data_value.replace('+', ' ')
		parsed_data[data_key] = urllib.unquote(data_value)
	#print parsed_data
	return parsed_data #returns a dictionary 


# ----- Putting everything together! --------
# pdb.set_trace()
routing_dictionary = {'/' : 'templates/index.html', '/home' : 'templates/user_info.html', '/get_user_info' : 'templates/get_user_info.html' }

#create server socket on port 9999
serversocket = socket.socket()
port = 9999

#this makes it so that there is no time gap in between running my code
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serversocket.bind(('', port))
serversocket.listen(5) 	

#this loop ensures new clients are always accepted
#remember each client socket can only handle one http request before closing.
while True:
	try:
		clientsocket, addr = serversocket.accept()
		listen(clientsocket)
	except socket.error:
		break
