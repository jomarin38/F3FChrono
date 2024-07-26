import json

class config:
    def __init__(self, file_name=None):
        self.conf = ""
        self.configFileName = file_name
        if file_name is not None:
            self.read(file_name)


    def read(self, config_file):
        try:
            self.conf = json.load(open(config_file,'r'))
            self.configFileName = config_file
        except IOError:
            pass
        except:
            raise


if __name__ == '__main__':
    conf = config("config.json")
    print("msg : ")
    for msg in conf.conf['msg']:
        print(msg + " : " + str(conf.conf['msg'][msg]))
    for seq in conf.conf['sequencer']:
        print("seq, msg : " + str(conf.conf['msg'][seq['msg']])+
              "timer : " + str(seq['timer']))