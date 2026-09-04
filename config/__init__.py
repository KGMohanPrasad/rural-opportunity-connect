# Rural Opportunity Connect — Configuration & Compatibility Initialization

# 1. Initialize PyMySQL driver as MySQLdb
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

# 2. Python 3.14+ Compatibility Patch for Django 4.2 Template Context Copying
# Under Python 3.14, copy(super()) returns a super object, causing AttributeError in BaseContext.__copy__
try:
    from django.template import context as _dc
    def _safe_base_context_copy(self):
        duplicate = self.__class__.__new__(self.__class__)
        duplicate.__dict__.update(self.__dict__)
        if hasattr(self, 'dicts'):
            duplicate.dicts = self.dicts[:]
        return duplicate
    _dc.BaseContext.__copy__ = _safe_base_context_copy
except Exception:
    pass
