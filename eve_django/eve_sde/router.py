class EveSdeRouter(object):
    """This router directs SDE queries to the correct db"""

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'eve_sde':
            return 'eve_sde'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'eve_sde':
            return 'eve_sde'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'eve_sde' or \
           obj2._meta.app_label == 'eve_sde':
           return True
        return None

    def allow_syncdb(self, db, model):
        if db == 'eve_sde':
            return model._meta.app_label == 'eve_sde'
        elif model._meta.app_label == 'eve_sde':
            return False
        return None