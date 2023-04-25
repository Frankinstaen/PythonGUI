import configparser
settings = configparser.ConfigParser()
settings.read('settings.ini')

Server = settings['DEFAULT']['Server']
Database = settings['DEFAULT']['Database']
Driver = settings['DEFAULT']['Driver']
Database_con = f'mssql://@{Server}/{Database}?driver={Driver}'