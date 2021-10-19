#!/usr/bin/env python                                                           
# -*- coding: utf-8 -*-                                                         
#                                                                               
# author: Lou Viannay <lou@islandtechph.com>                                    


# noinspection PyUnusedLocal,PyProtectedMember
class DBRouterBase(object):
    APP_LABEL = __name__.split('.')[0]
    DB_NAME = 'nds'

    def db_for_read(self, model, **hints):
        if model._meta.app_label == self.APP_LABEL:
            return self.DB_NAME
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == self.APP_LABEL:
            return self.DB_NAME
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == self.APP_LABEL or \
                obj2._meta.app_label == self.APP_LABEL:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # print "app_label ==> '{}'".format(app_label)
        # print "external_dbs ==> '{}'".format(self.EXTERNAL_DBs)
        if (app_label == self.APP_LABEL) or (db == self.DB_NAME):
            # raise Exception("inside allow_migrate, return false db =?'{}'".format(db))
            return False

        return None
