"""
types:
create => save list
resize => save element and id
delete => save list
clear => save list

"""

class action:
	def __init__ (self,typeAction,element):
		self.type = typeAction
		self.elementOriginal = element