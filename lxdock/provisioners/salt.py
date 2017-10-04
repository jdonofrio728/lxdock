import os

from voluptuous import Any, Exclusive, IsFile, Required

from .base import Provisioner

class SaltProvisioner(Provisioner):
    """ Provisions using salt masterless """

    name = "salt"
    schema = {
        Required('log_level', default='info'): str,
        Required('verbose', default=False): bool
    }

    _bootstrap = "https://raw.githubusercontent.com/saltstack/salt-bootstrap/stable/bootstrap-salt.sh"
    guest_required_packages_ubuntu = ["curl"]


    # Guest Specific Provisioning
    def provision_single(self, guest):
        pass

  
    # Run salt bootstrap script
    def setup_single(self, guest):
        curl = which('curl')
        fetch = which('fetch')
        # Check for curl
        if curl:
            guest.run([curl, '-O', '-L', self._bootstrap])
        elif fetch:
            guest.run([fetch, '-o', self._bootstrap])
        else:
            print ("Missing curl and fetch, please install them prior to executing this provisioner")
            return
        guest.run(['sh', '-c', 'bootstrap-salt.sh'])
        print(guest.name)




# unix which implementation borrowed from stackoverflow answer by Jay
# https://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None
