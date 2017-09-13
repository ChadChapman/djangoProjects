import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

declBase = declarative_base()
#end config code

class Restr(declBase):
	__tablename__ = 'restr'
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)


class MenuItem(declBase):
	__tablename__ = 'menu_item'
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	course = Column(String(250))
	description = Column(String(250))
	price = Column(String(8))
	restr_id = Column(Integer, ForeignKey('restr.id'))
	restr = relationship(Restr)




















###end of file code###

engine = create_engine('sqlite:///restmenu.db') #which db engine to bind to

declBase.metadata.create_all(engine)


