from flask_nav import Nav
from flask_nav.elements import *

topnav=Nav()
topnav.register_element('top',Navbar(u'皖声',View(u'主页','index'),View(u'让我懂你','readytoverify'),View(u'未完待续','KnowMore'),View(u'Me,I&Myself','about')))