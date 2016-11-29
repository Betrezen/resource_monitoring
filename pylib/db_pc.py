# -*- python -*-
# author: krozin@gmail.com, kskonovalov100@gmail.com
# db: created 2016/11/05
# db_pc: created 2016/11/21
# copyright

import datetime
import hashlib
import os
import random

from sqlalchemy import Column, Boolean, Integer, String, Date, Time
from sqlalchemy import create_engine
from sqlalchemy import desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from settings import DBPATH

Base = declarative_base()

class PC_resource(Base):
    __tablename__ = 'pc_results'
    id = Column(Integer, primary_key=True)
    ip = Column(Integer)
    name = Column(String(10))
    turnon = Column(Boolean) # ON / OFF
    status = Column(String) # OK / NOK / NA
    date = Column(Date) # last_data_update
    time = Column(Time) # last_time_update
    uptime = Column(Integer)
    disk_free = Column(Integer)
    disk_all = Column(Integer)
    cpu_u = Column(Integer)
    memory_u = Column(Integer)
    memory_a = Column(Integer)
    network = Column(Integer)


    def __init__(self,
                 ip=0,  
                 name='name',
                 turnon=True,
                 status='NA',
                 d=datetime.datetime.now(),
                 t=datetime.datetime.now().time(),
                 uptime=0,
                 disk_free=0,
                 disk_all=0,
                 cpu_u=0,
                 memory_u=0,
                 memory_a=0,
                 network=0,
                 network_traffic=0,
                 prosecces=0):
        self.ip = ip
        self.name = name
        self.turnon = turnon
        self.status = status
        self.date = d
        self.time = t
        self.uptime = uptime
        self.disk_free = disk_free
        self.disk_all = disk_all
        self.cpu_u = cpu_u
        self.memory_u = memory_u
        self.memory_a =memory_a
        self.network = network

    def __repr__(self):
        return "<Resource({} {} {}__{}__{} {}|{}|{} {}/{} {}% {}/{})>".format(
            self.id, self.ip, self.name, self.turnon, self.status,
            self.date, self.time, self.uptime, self.disk_free,
            self.disk_all, self.cpu_u, self.memory_u, self.memory_a,
            self.network)


class PC_DbProxy(object):

    def __init__(self):
        if not os.path.exists(DBPATH):
            with open(DBPATH, 'a'):
                os.utime(DBPATH, None)

        self._init_engine(uri='sqlite:///{}'.format(DBPATH), echo=True)
        self._init_db()

    def _init_engine(self, uri, **kwards):
        self.engine = create_engine(uri, **kwards)

    def _init_db(self):
        self.session = scoped_session(sessionmaker(bind=self.engine))
        Base.metadata.create_all(self.engine)

    def add_pc_resource(self, **kwargs):
        print "add_pc_resource"
        res = PC_resource(
            ip =kwargs.get('ip'),
            name=kwargs.get('name'),
            turnon=kwargs.get('turnon'),
            status=kwargs.get('status'),
            disk_free=kwargs.get('disk_free'),
            cpu_u=kwargs.get('cpu_u'))
            #date=kwargs.get('date'),
            #time=kwargs.get('time'))
        self.session.add(res)
        self.session.commit()
        return res.id

    def get_pc_resource(self, rid):
        return self.session.query(PC_resource).filter(PC_resource.id == rid).first()

    def update_pc_resource(self, rid, **kwargs):
        #name = kwargs.get('name')
        #href = kwargs.get('href')
        #turnon = kwargs.get('turnon')
        #status = kwargs.get('status')
        #d = kwargs.get('date')
        #t = kwargs.get('time')
        #uptime = kwargs.get('uptime')
        self.session.query(PC_resource).filter(PC_resource.id == rid).update(kwargs)
        self.session.commit()

    def delete_pc_resource(self, rid):
        self.session.query(PC_resource).filter(PC_resource.id == rid).delete()
        self.session.commit()


    def get_pc_all(self, order1=PC_resource.date, order2=PC_resource.time, order3=PC_resource.disk_free, order4=PC_resource.cpu_u):
        return self.session.query(PC_resource).order_by(desc(order1), desc(order2), desc(order3), desc(order4)).all()
