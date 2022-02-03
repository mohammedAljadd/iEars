import socket,cv2, pickle,struct

# create socket
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
port = 9999


# Connect to the server --------------------------------------------------------------------------------
client_socket.connect((host_ip,port)) # a tuple


# Send option ------------------------------------------------------------------------------------------
client_socket.send(bytes("Facial recognition", 'utf-8'))

# Receive message where asked to stream
asked_streaming = client_socket.recv(256).decode('utf-8')

# Start streaming --------------------------------------------------------------------------------------
cap = cv2.VideoCapture(0)
while True:
	ret,photo = cap.read()
	cv2.imshow('Client camera', photo)
	ret,buffer = cv2.imencode(".jpg",photo,[int(cv2.IMWRITE_JPEG_QUALITY),30])
	x_as_bytes = pickle.dumps(buffer)
	client_socket.sendto((x_as_bytes),(host_ip, port))
	key = cv2.waitKey(1) & 0xFF
	if key  == ord('q'):
		break
cv2.destroyAllWindows()
cap.release()


client_socket.close()