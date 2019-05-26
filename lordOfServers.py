import sys, warnings, argparse, paramiko
warnings.filterwarnings(action='ignore',module='.*paramiko.*')
client = paramiko.SSHClient()

# argparser
parser =  argparse.ArgumentParser()
group_target = parser.add_mutually_exclusive_group(required=True)
group_target.add_argument("-t", "--target", nargs="+", help="host on which you'll send the command (cannot be used with -f)")
group_target.add_argument("-f", "--file", nargs="+", help="file of hosts on which you'll send the command (cannot be used with -t)")
parser.add_argument("-c", "--command", nargs=1, type=str, help="command to send", required=True)
parser.add_argument("-u", "--user", nargs=1, help="account used for command execution", required=True)
parser.add_argument("-P", "--passw", nargs=1, help="password which belong to the user", required=True)
parser.add_argument("-p", "--port", nargs=1, default="22", type=int, help="port to use")
parser.add_argument("-v", "--verbose", help="print parameters used. BEWARE that -vv will also print password !", action="count")
parser.add_argument("-T", "--testing", help="turn on testing mode, which will not send command to targets", action="store_true")
args = parser.parse_args()

# params
target = args.target
file = args.file
passw = args.passw[0]
cmd = args.command[0]
user = args.user[0]
port = args.port
verbosity = args.verbose
test = args.testing

# functions
def verbose(verbosity):
    print("Debug:")
    print(" command:"+cmd)
    print(" target:"+str(target))
    print(" file:"+str(file))
    print(" port:"+str(port))
    print(" user:"+user)
    print(" testing:"+str(test))
    if verbosity>1:
        print(" pass:"+passw)

def readfile(file):
    f = open(file, "r")
    lines = f.readlines()
    for line in lines:
        print(line)
    f.close()

def send(server):
    print("sending on: "+server)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port=port, username=user, password=passw)
    #client.exec_command(cmd)
    stdin, stdout, stderr = client.exec_command(cmd)
    for line in stdout.read().splitlines():
         print (line)
    client.close()

# main code
if args.verbose:
    verbose(verbosity)

if args.file:
    readfile(file)

if not args.testing:
    for server in target:
        send(server)
