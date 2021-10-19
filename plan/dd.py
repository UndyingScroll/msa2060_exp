import subprocess
import sys

def metaclean(path):
    rcode = []
    ofstring = 'of=' + path
    # find the end of the drive
    rcode.append(ofstring)
    szcmd = ['sudo', 'blockdev', '--getsz', path]
    szresult = subprocess.Popen(szcmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate(input=b'smart\n')
    rcode.append(szresult[0].decode('utf-8'))
    # zero first 16 miB
    ddcmd = ['sudo','dd','if=/dev/zero',ofstring,'bs=4096','count=4096']
    ddresult = subprocess.Popen(ddcmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate(input=b'smart\n')
    result = ddresult[1].decode('utf-8')
    rcode.append(result[:25])

    # zero end of drive

    seek = int(szresult[0].decode('utf-8'))-1024
    seekstr = 'seek=' + str(seek) 
    ddcmd = ['sudo', 'dd', 'if=/dev/zero', ofstring,'bs=512', seekstr, 'count=1024']

    ddresult = subprocess.Popen(ddcmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate(input=b'smart\n')
    result = ddresult[1].decode('utf-8')
    rcode.append(result[:25])
    return(rcode)
