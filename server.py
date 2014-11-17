#http server.py - this makes it so that Susan can see what I write to her in her browser. 
import socket 
import threading
import pdb

#------- Receive messages from Clients ----------
def listen(clientsocket):
	msg = clientsocket.recv(1000)
	if msg:
		msg = msg.split(' ')
		request_type = msg[0]
		print msg
		if request_type == "GET":
			client_msg = msg[1]
			get(clientsocket, client_msg)
		if request_type == "POST":
			client_msg = msg[1]
			input_dict = parse_function(msg)
			post(clientsocket, client_msg, input_dict)
			

# ------ Handles get requests ------- 
def get(clientsocket, arguments):
	if arguments in routing_dictionary.keys():
		page = routing_dictionary[arguments]
	else:
		page = 'templates/sorry.html'
	read_file = open(page, 'r')
	read_text = read_file.read()
	read_file.close()
	return render(clientsocket, read_text)


# ------- Handles post requests --------
def post(clientsocket, action, user_input):
	message_file = open('templates/passing_vars.html', 'r')
	message_text = message_file.read()
	message_file.close()
	new_message = message_text %user_input
	return render(clientsocket, new_message)


# ----- sends http msg and page to client socket, then closes socket -----
def render(clientsocket, new_msg):
	clientsocket.send('HTTP/1.0 200 OK\n\n')
	clientsocket.send(new_msg)
	clientsocket.close()


# ------ Parses raw request to find user input ------ 
def parse_function(msg):
	raw_data = msg[-1]
	start = raw_data.find("\r\n\r\n") + 4
	data = raw_data[start:]
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
		parsed_data[data_key] = data_value
	print parsed_data
	return parsed_data #returns a dictionary 


# ----- Putting everything together! --------
# pdb.set_trace()
routing_dictionary = {'/' : 'templates/index.html', '/home' : 'templates/user_info.html' }

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
