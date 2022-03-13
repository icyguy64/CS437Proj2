import socket
import picar_4wd as fc

HOST = "192.168.18.47" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    car_status = ""
    try:
        while 1:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            data  = client.recv(1024)      # receive 1024 Bytes of message in binary format
            if car_status == "":
                car_status = "idle"
            if data != b"":
                print(data)     
                data1 = fc.cpu_temperature()
                data3 = car_status
                data2 = fc.power_read()
                #print(data1.to_bytes())
                data_msg = str(data1) + "," + str(data2) + "," + (data3)
                client.sendall(bytes(data_msg, 'ascii'))
                #client.sendall(b"10") # Echo back to client
            if data == b"up\r\n":
                fc.forward(1)
                car_status = "forward"
            elif data == b"left\r\n":
                fc.turn_left(1)
                car_status = "turning"
            elif data == b"right\r\n":
                fc.turn_right(1)
                car_status = "turning"
            elif data == b"down\r\n":
                fc.backward(1)
                car_status = "reversing"
            elif data == b"stop\r\n":
                fc.stop()
                car_status = "idle"
    except: 
        print("Closing socket")
        client.close()
        s.close()    
