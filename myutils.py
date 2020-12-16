from pyORM import orm
from functools import wraps



def updateAfterEvent(func):
	'''
	This decorator will detect the object-based table schema (PokemonClass, UserClass ...etc)
	 and will update the database after each return of the function or method
	'''
	@wraps(func)
	def wrapper(*args, **kw):
		dbSession = orm(object_= args[0])
		try:
			res = func(*args, **kw)
		finally:
			pKey = [k for k,v in res.__dict__.items() if k[0]!="_" and v[2]["PRIMARY KEY"]][0]
			updates_ = {k:v[0] for k, v in res.__dict__.items() if k[0]!="_" and '_protected' != k[-10:]}
			dbSession.update({pKey: getattr(res, pKey)[0]}, **updates_)
		return res
	return wrapper




def updateObj(obj_):
	dbSession = orm(obj_)
	pKey = [k for k,v in obj_.__dict__.items() if k[0]!="_" and v[2]["PRIMARY KEY"]][0]
	updates_ = {k:v[0] for k, v in obj_.__dict__.items() if k[0]!="_" and '_protected' != k[-10:]}
	dbSession.update({pKey: getattr(obj_, pKey)[0]}, **updates_)
