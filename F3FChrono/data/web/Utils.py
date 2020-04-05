import socket
import requests
from F3FChrono.chrono import ConfigReader


class Utils:

    _port_number = 8000
    _protocol = 'http://'

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
        return Utils._protocol + Utils.get_ip() + ':' + str(Utils.get_port_number()) + '/f3franking'

    @staticmethod
    def get_logout_url():
        return Utils._protocol + Utils.get_ip() + ':' + str(Utils.get_port_number()) + '/administrator/logout_f3f_admin'

    @staticmethod
    def server_alive():
        try:
            request_url = Utils.get_base_url()+'/is_alive'
            response = requests.post(request_url)
            return True
        except:
            return False
