import argparse
from http.client import NETWORK_AUTHENTICATION_REQUIRED
import socket
import shlex
import subprocess
import sys
import textwrap
import threading


ascii_art = '''
     _                      _______                      _
  _dMMMb._              .adOOOOOOOOOba.              _,dMMMb_
 dP'  ~YMMb            dOOOOOOOOOOOOOOOb            aMMP~  `Yb
 V      ~"Mb          dOOOOOOOOOOOOOOOOOb          dM"~      V
          `Mb.       dOOOOOOOOOOOOOOOOOOOb       ,dM'
           `YMb._   |OOOOOOOOOOOOOOOOOOOOO|   _,dMP'
      __     `YMMM| OP'~"YOOOOOOOOOOOP"~`YO |MMMP'     __
    ,dMMMb.     ~~' OO     `YOOOOOP'     OO `~~     ,dMMMb.
 _,dP~  `YMba_      OOb      `OOO'      dOO      _aMMP'  ~Yb._
             `YMMMM\`OOOo     OOO     oOOO'/MMMMP'
     ,aa.     `~YMMb `OOOb._,dOOOb._,dOOO'dMMP~'       ,aa.
   ,dMYYMba._         `OOOOOOOOOOOOOOOOO'          _,adMYYMb.
  ,MP'   `YMMba._      OOOOOOOOOOOOOOOOO       _,adMMP'   `YM.
  MP'        ~YMMMba._ YOOOOPVVVVVYOOOOP  _,adMMMMP~       `YM
  YMb           ~YMMMM\`OOOOI`````IOOOOO'/MMMMP~           dMP
   `Mb.           `YMMMb`OOOI,,,,,IOOOO'dMMMP'           ,dM'
     `'                  `OObNNNNNdOO'                   `'
                           `~OOOOO~'   
'''

print (ascii_art)

#1
def execute (cmd):
    cmd = cmd.strip()
    if not cmd:
        return
    #2
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    return output.decode()

class NetCat:
    #7
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        #8  
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 2)

    #9
    def run(self):
        if self.args.listen:  
            self.listen()
        else:
            self.send()

    def send(self):
        #10
        self.socket.connect((self,args.target, self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)
        
        #11
        try:
            #12
            while True:
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.encode()
                    if recv_len < 4096:
                        break
                if response: #13
                    print (response)
                    buffer = input ('> ')
                    buffer += '\n'
                    self.socket.send(buffer.encode())
        except KeyboardInterrupt: #14
            print ("User Terminated")
            self.socket.close()
            sys.exit()

    def listen(self):
        #15
        self.socket.binf((self.args.target, self.args.port))
        self.socket.listen(5)
        #16
        while True:
            client_socket, _ = self.socket.accept() 
            #17
            client_thread = threading.Thread(target=self.handle, args = (client_socket,))
            client_thread.start()

    def handle (self, client_socket):
        #18
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())

        #19
        elif self.args.upload:
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break
            
            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)
            message = f'Saved file {self.args.upload}'
            client_socket.send(message.encode())
        #20
        elif self.args.command:
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b'BHP: #> ')
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)
                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''
                except Exception as e:
                    print(f'server killed {e}')
                    self.socket.close()
                    sys.exit()

if __name__ == '__main__':
    #3
    parser = argparse.ArgumentParser(
        description='BHP Net Tool', 
        formatter_class=argparse.RawDescriptionHelpFormatter, 
        #4
        epilog=textwrap.dedent('''Example: 
            netcat.py -t 192.168.1.108 -p 5555 -l -c # command shell
            netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt # upload to file
            netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd\" # execute command
            echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135 # echo text to server port 135
            netcat.py -t 192.168.1.108 -p 5555 # connect to server
        '''))
    #5
    parser.add_argument('-c', '--command', action='store_true', help='command shell')
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
    parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP')
    parser.add_argument('-u', '--upload', help='upload file')
    args = parser.parse_args()
    if args.listen: #6
        buffer = ''
    else:
        buffer = sys.stdin.read()
 
    nc = NetCat(args, buffer.encode()) 
    nc.run()

""""
COMMENTS SECTION 

1.
we create the function called "execute"
this function contain the "subprocess" library -> y provides a powerful process-creation interface that gives you a number of ways to interact with client programs

2.
from teh subprocces library we use its "check_output" method ->  runs a command on the local operating system and then returns the output from that command.

3.
we use the argparse module to create command line interface.
We’ll provide arguments so it can be invoked to upload a file, execute a command, or start a command shell.

4.
we provide example usage that the code will display when the user invokes it with --help

5.
-c -> set up an interactive shell
-e -> execute one specific command
-l -> indicates that a listener should be set up
-p -> specifies the port on which to communicate
-t -> specify the target IP
-u -> specify the name of the file to upload

The -c, -e, and -u arguments imply the -l argument, because those arguments only apply to the listener side of the communication. 
The sender side makes the connection to the listener, and so it only needs the -t and -parguments to define the target listener

6.
if args.listen:

if we set up as a listener, we invoke NetCat object with an empty buffer string
otherwise, we send the buffer content from stdin
we use the nc.run() to start it up

7.
we initialize the NetCat object with the arguments from the cmd & buffer 

8.
we create a socket object

9.
the run(self) function - is the entry point for mananging Netcat object
if we set up a listener we call the listener() method
otherwise we call the send() method

10.
we connect to the target and port
if we have a buffer, we send that to the target first

11.
we set up a "try/catch" block -> so we can manually close teh connection with CTRL-C

12.
we start a loop to receive data from the target 
if there is no more data, we break out from the loop

13.
otherwise we print the response data and pause to get an interactive input
send that input, and continue with the loop

14.
the loop will contuine until the KeyboardInterrupt occurs -> CTRL-C
this will close the socket

15.
the listen(self) function bind to the target & port 

16.
we start listening in a loo

17.
passing the conncted socket to the handle method

18.
the handle() function executes the task corresponding to the command line argument it receives: 
execute a command, upload a file, or start a shell. If a command should be executed

19.
the handle() function passes that command to the execute() function and sends the output back on the socket. If a file should be uploaded

we set up a loop to listen for content on the listening socket and receive data until there’s no more data coming in. Then we write that accumulated content to the specified file

20.
if a shell is to be created, we set up a loop, send a prompt to the sender, and wait for a command string to come back. 
We then execute the command using the execute() function and return the output of the command to the sender
-------------------------------------------------------------------------------------------------------------

You’ll notice that the shell scans for a newline character to determine 
when to process a command, which makes it netcat friendly. That is, you can 
use this program on the listener side and use netcat itself on the sender side. 
However, if you’re conjuring up a Python client to speak to it, remember to 
add the newline character. In the send method, you can see we do add the 
newline character after we get input from the console
"""