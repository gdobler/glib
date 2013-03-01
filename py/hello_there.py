import time
import sys

def hello_there():

    for i in range(3,0,-1):
        print '         \r',
        sys.stdout.flush()
        print '{0}.\r'.format(i),
        sys.stdout.flush()
        time.sleep(0.5)
        print '{0}..\r'.format(i),
        sys.stdout.flush()
        time.sleep(0.5)
        print '{0}...\r'.format(i),
        sys.stdout.flush()
        time.sleep(0.5)

    print 'HELLO THERE!!!'

    return
