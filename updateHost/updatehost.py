import socket
from shutil import copyfile
import argparse

LOCAL_HOSTS = '/etc/hosts'

def getIPbyHostName(hostName):
    try:
        addr = socket.gethostbyname(hostName)
    except OSError:
        print("can't find this service ip")
        return None

    return addr


def update(hostnames=None):

    copyfile(LOCAL_HOSTS,'hosts.bak')

    try:
        updateIP(hostnames)
    except Exception:
        print("update failed")
        copyfile('hosts.bak',LOCAL_HOSTS)


def updateIP(hostNames = None):
    input = open(LOCAL_HOSTS, 'r')
    lines = input.readlines()
    input.close()

    output = open(LOCAL_HOSTS, 'w')
    #新建一个
    if hostNames != None:
        for name in hostNames:
            updatehostnameip(name,output)
        return

    #更新之前的
    for line in lines:

        if not line:
            break

        if line.strip() == '\n' or line.strip() == '':
            continue

        changeLineIp(line,hostNames,output)

    output.close()

def changeLineIp(line,hostNames,output):

    ipadrrs, oldhostname = line.split()
    oldhostname = oldhostname.rstrip(' \n')
    # print('ip:%s hostname:%s' % (ipadrrs, oldhostname))

    # 不更新localhost
    if (oldhostname.lower() == 'localhost'):
        output.write(line)
        return

    # 不传参数，更改所有的IP
    if hostNames == None:
        updatehostnameip(oldhostname, output)
        return

    #已经修改过hostname 的跳过
    hostnames = map(lambda x : x.lower(),hostNames)
    if oldhostname.lower() not in hostnames:
        output.write(line)
        return


def updatehostnameip(hostname,output):
    ipadrrs = getIPbyHostName(hostname)
    if ipadrrs != None:
        iphost = ipadrrs + " " + hostname + '\n'
        print('update host:%s newip:%s' % (hostname, iphost))
        output.write(iphost)
    else:
        print("can't find ip by hostname:%s" % (hostname))


def main():
    parser = argparse.ArgumentParser(description='update host to new ip')
    parser.add_argument('-s','--hostnames',nargs = '+')
    args = parser.parse_args()
    hostnames =  args.hostnames
    update(hostnames)


if __name__ == '__main__':
    main()



