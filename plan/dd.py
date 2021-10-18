from subprocess import run, PIPE
import sys

def metaclean(path):
    rcode = 0
    ofstring = 'of=' + path
    
    szcmd = ['echo','smart','|','sudo','-S','sudo', 'blockdev', '--getsz', path]
    # find the end of the drive
    szresult = run(szcmd, stdout = PIPE, stderr = PIPE, universal_newlines = True)
    rcode = rcode + szresult.returncode
    # zero first 16 miB
    ddcmd = ['echo','smart','|','sudo','-S','sudo','dd','if=/dev/zero',ofstring,'bs=4096','count=4096']
    ddresult = run(ddcmd, stdout = PIPE, stderr = PIPE, universal_newlines = True)
    rcode = rcode + ddresult.returncode

    # zero end of drive

    seek = int(szresult.stdout)-1024
    seekstr = 'seek=' + str(seek) 
    ddcmd = ['echo','smart','|','sudo','-S','sudo', 'dd', 'if=/dev/zero', ofstring,'bs=512', seekstr, 'count=4096']

    ddresult = run(ddcmd, stdout = PIPE, stderr = PIPE, universal_newlines = True)
    rcode = rcode + ddresult.returncode
    return(rcode)
