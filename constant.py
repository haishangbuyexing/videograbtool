DB_USER = 'isoft'
DB_PASSWD = 'smbee60f9'
DB_NAME = 'smb'

SQL_VIDEO_DATABASE = """
CREATE DATABASE IF NOT EXISTS video 
default character set utf8 COLLATE utf8_general_ci;
"""

SQL_VIDEO_USER = """
GRANT ALL PRIVILEGES on smb.* to '%s'@'localhost' IDENTIFIED BY '%s';
""" % (DB_USER, DB_PASSWD)
