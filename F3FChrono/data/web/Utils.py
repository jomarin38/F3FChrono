import socket
import requests
from F3FChrono.chrono import ConfigReader


class Utils:

    _port_number = 8000

    @staticmethod
    def get_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    @staticmethod
    def set_port_number(port_number):
        Utils._port_number=port_number

    @staticmethod
    def get_port_number():
        return Utils._port_number

    @staticmethod
    def get_base_url():
        return 'http://' + Utils.get_ip() + ':' + str(ConfigReader.config.conf['webserver_port']) + '/f3franking'

    @staticmethod
    def server_alive():
        try:
            request_url = Utils.get_base_url()+'/is_alive'
            response = requests.post(request_url)
            return True
        except:
            return False
