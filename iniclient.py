import configparser
class Config:
    def __init__(self):
        self.INI = 'config/config.ini'
        self.config = configparser.ConfigParser()
        self.config.read(self.INI)
        self.chrome_version = self.config.get('section1', 'option1')
    def get_version(self):
        return str(self.chrome_version)
    def set_version(self, version):
        self.config.set('section1', 'option1', version)
        with open(self.INI, 'w') as file:
            self.config.write(file)