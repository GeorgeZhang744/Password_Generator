# Helper class for Password Generator
class PasswordSetting:
    def __init__(self, on_off, setting):
        self.__on_off = on_off
        self.__setting = setting
    
    def is_setting_on(self):
        return self.__on_off
    
    def change_setting(self, on_off):
        self.__on_off = on_off

    def get_components(self):
        return self.__setting