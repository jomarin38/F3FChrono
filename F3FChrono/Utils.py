import os
import re

def get_raspi_revision():
    rev_file = '/sys/firmware/devicetree/base/model'
    info = { 'pi': '', 'model': '', 'rev': ''}
    raspi = model = revision = ''
    try:
        fd = os.open(rev_file, os.O_RDONLY)
        line = os.read(fd,256)
        os.close(fd)
        print (line)
        m=re.split(r'\s', line.decode('utf-8'))
        if m:
            info['pi'] = m[3]
            info['model'] = m[5]
        return info
    except:
        pass
    return info


def is_running_on_pi():
    pi = get_raspi_revision()
    return pi['pi'] != ''
