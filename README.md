# netcat
Simply her majesty NETCAT

This code serves as a versatile network utility tool, combining elements of a command-line interface (CLI) and a basic TCP server-client architecture. It enables users to perform various networking tasks such as executing commands on remote systems, uploading files, and establishing interactive command shells over TCP/IP.

**Usage:**

1. **Execute Commands:**
   - Use the `-e` or `--execute` option to execute a specific command on the target system.
   - Example: `python netcat.py -t 192.168.1.108 -p 5555 -e="cat /etc/passwd"`

2. **Upload Files:**
   - Use the `-u` or `--upload` option to upload a file to the target system.
   - Example: `python netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt`

3. **Start Command Shell:**
   - Use the `-c` or `--command` option to start an interactive command shell on the target system.
   - Example: `python netcat.py -t 192.168.1.108 -p 5555 -l -c`

4. **Establish Connection:**
   - Connect to a listening server using the target IP address and port.
   - Example: `python netcat.py -t 192.168.1.108 -p 5555`

**Step-by-Step Guide:**

1. **Setup Environment:**
   - Save the code as `netcat.py` in your preferred directory.
   - Ensure you have Python installed on your system.

2. **Understand Command-line Options:**
   - Review the available command-line options provided by the argparse module.
   - Options include executing commands (`-e`), uploading files (`-u`), starting command shells (`-c`), specifying the target IP (`-t`), and port (`-p`).

3. **Run the Script:**
   - Open a terminal or command prompt.
   - Navigate to the directory where `netcat.py` is saved.

4. **Execute Commands:**
   - To execute a command on the target system, use the `-e` option followed by the desired command.
   - Example: `python netcat.py -t 192.168.1.108 -p 5555 -e="cat /etc/passwd"`

5. **Upload Files:**
   - To upload a file to the target system, use the `-u` option followed by the path to the file.
   - Example: `python netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt`

6. **Start Command Shell:**
   - To start an interactive command shell on the target system, use the `-c` option.
   - Example: `python netcat.py -t 192.168.1.108 -p 5555 -l -c`
   - Once connected, you can enter commands interactively, and the output will be displayed.

7. **Connect to Listening Server:**
   - To connect to a listening server, specify the target IP (`-t`) and port (`-p`).
   - Example: `python netcat.py -t 192.168.1.108 -p 5555`

8. **Interact with Server:**
   - Depending on the options used, you can execute commands, upload files, or interactively communicate with the server.

9. **Terminate Connection:**
   - To terminate the connection, use `Ctrl + C` or send an appropriate termination signal.

10. **Explore Further:**
    - Customize the behavior by modifying the code or adding additional features as needed.
    - Ensure proper error handling and security measures when deploying in real-world scenarios.
