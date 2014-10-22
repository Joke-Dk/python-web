# db.py
import threading
# database engine object
class _Engine( object):
	def __init__(self, connect):
		self._connect = connect
	def connect(self):
		return self._connect()

engine = None

# threadlocal object
class _DbCtx( threading.local):
	def __init__(self):
		self.connection = None
		self.transactions = 0
	
	def is_init(self):
		return not self.connection is None

	def init(self):
		# until one request link to the database, this function run
		self.connection = _LasyConnection()	
		self.transactions = 0

	def cleanup(self):
		self.connection.cleanup()
		self.connection = None

	def cursor(self):
		return self.connection.cursor()

_dbctx = _DbCtx()

#define connection ctx
class _ConnectionCtx(object):
	def __enter__(self):
		global _dbctx
		self.should_cleanup = False
		if not _dbctx.is_init():
			_dbctx.init()
			self.should_cleanup = True
		return self
	
	def __exit__(self, exctype, exvalue, traceback):
		global _dbctx
		if self.should_cleanup:
			_dbctx.cleanup()

def connection():
	return _ConnectionCtx()

# decorator function
def with_connection(func):
	def wrapper(*args, **kw):
		with connection():
			func(*args, **kw)

@with_connection
def select(sql, *args):
	_dbctx.

@with_connection
def update(sql, *args):
	pass

#######################Transaction########################
class _TransactionCtx(object):
	def __enter__(self):
		global _dbctx
		self.should_close_conn = False
		if not _dbctx.is_init():
			_dbctx.init()
			self.should_close_conn = True
		_dbctx.transactions = _dbctx.transactions + 1
		return self

	def __exit__(self, exctype, excvalue, traceback):
		global _dbctx
		_dbctx.transactions = _dbctx.transactions - 1
		try:
			if _dbctx.transactions == 0:
				if exctype is None:
					self.commit()
				else:
					self.rollback()
		finally:
			if self.should_close_conn:
				_dbctx.cleanup()

	def commit(self):
		global _dbctx
		try:
			_dbctx.connection.commit()
		except:
			_dbctx.connection.rollback()
			raise()

	def rollback(self):
		global _dbctx
		_dbctx.connection.rollback()
		
if __name__ == "__main__":
	
