from fabric.api import *
import fabric.contrib.files

filename = '/etc/haproxy/haproxy.cfg'
class HAProxyClient:

    def add_backend(ip1, ip2):
        settingDefault = '''
        tee -a /etc/haproxy/haproxy.cfg << EOF
    backend http_backend
            option tcp-check
            server lb1 example1 check port 80 
            server lb2 example2 check port 80
        '''
        run(settingDefault)
        fabric.contrib.files.sed(filename, 'example1', ip1)
        fabric.contrib.files.sed(filename, 'example2', ip2)

    def add_frontend():
        settingDefault = '''
        tee -a /etc/haproxy/haproxy.cfg << EOF
    
    frontend http_front
            bind *:80
            default_backend http_backend
        '''
        run(settingDefault)



    def change_ip(oldip, newip):
        # exanple change_ip('192.168.0.24', '172.32.32.19')
        fabric.contrib.files.sed(filename, oldip, newip,)

    def delete_backend():
        filename = '/etc/haproxy/haproxy.cfg'

        search = 'backend'

        if fabric.contrib.files.contains(filename, search):
            print('contains')
            fabric.contrib.files.sed(filename, 'backend .*', '',)
            fabric.contrib.files.sed(filename, 'option .*', '',)
            fabric.contrib.files.sed(filename, 'server .*', '',)
            print('success')
        else:
            print('the file does not contains')

    def delete_frontend():
        filename = '/etc/haproxy/haproxy.cfg'
        search = 'frontend'
        if fabric.contrib.files.contains(filename, search):
            print('contains')
            fabric.contrib.files.sed(filename, 'frontend .*', '',)
            fabric.contrib.files.sed(filename, 'bind .*', '',)
            fabric.contrib.files.sed(filename, 'default_backend .*', '',)
            print('success')
        else:
            print('the ' + filename + ' does not contains')



