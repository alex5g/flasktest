from flask_nav import Nav
from flask_nav.elements import *

topnav=Nav()
topnav.register_element('top',Navbar(u'皖声',View(u'主页','index'),View(u'i want to konw you','getinfo')))