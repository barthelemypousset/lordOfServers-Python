import sys, warnings, argparse, paramiko
warnings.filterwarnings(action='ignore',module='.*paramiko.*')
client = paramiko.SSHClient()

# argparser
parser =  argparse.ArgumentParser()
group_target = parser.add_mutually_exclusive_group(required=True)
group_target.add_argument("-t", "--target", nargs=1, help="host on which you'll send the command (cannot be used with -f)")
group_target.add_argument("-f", "--file", nargs=1, help="file of hosts on which you'll send the command (cannot be used with -t)")
parser.add_argument("-c", "--command", nargs=1, type=str, help="command to send", required=True)
parser.add_argument("-u", "--user", nargs=1, help="account used for command execution", required=True)
parser.add_argument("-P", "--passw", nargs=1, help="password which belong to the user", required=True)
parser.add_argument("-p", "--port", nargs=1, default="22", type=int, help="port to use")
parser.add_argument("-v", "--verbose", help="print parameters used. BEWARE that -vv will also print pasword !", action="count")
args = parser.parse_args()

# params
target = args.target[0]
passw = args.passw[0]
cmd = args.command[0]
user = args.user[0]
port = str(args.port)
verbosity = args.verbose

# functions
def usage():
    print("nope !")

def readfile():
    print("read")

def verbose(verbosity):
    print("Debug:")
    print(" command:"+cmd)
    print(" target:"+target)
    print(" port:"+port)
    print(" user:"+user)
    if verbosity>1:
        print(" pass:"+passw)

def send():
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(target, port=port, username=user, password=passw)
    #client.exec_command(cmd)
    stdin, stdout, stderr = client.exec_command(cmd)
    for line in stdout.read().splitlines():
         print (line)
    client.close()

# main code
if args.verbose:
    verbose(verbosity)

send()
