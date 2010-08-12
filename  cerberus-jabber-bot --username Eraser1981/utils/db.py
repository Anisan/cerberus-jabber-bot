#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import time

__author__ = "Eraser"

def execNonQuery(dbpath,command):
    fail = 1
    while(fail): 
        con=sqlite3.connect(dbpath,timeout=5) 
        c=con.cursor() 
        try: 
            c.execute(command) 
            con.commit()
            fail = 0
        except sqlite3.OperationalError,e: 
            print(str(e)) 
            fail = 0
            if str(e)=="database is locked":
                fail = 1 
                time.sleep(5)
        con.close()
        
def execQuery(dbpath,command):
    fail = 1
    while(fail): 
        con=sqlite3.connect(dbpath,timeout=5) 
        c=con.cursor() 
        try: 
            c.execute(command) 
            ret = c.fetchall()
            fail = 0
        except sqlite3.OperationalError,e: 
            print(str(e)) 
            fail = 0
            if str(e)=="database is locked":
                fail = 1 
                time.sleep(5)
        con.commit()
        con.close()
    return ret