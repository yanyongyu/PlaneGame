# -*- coding: utf-8 -*-
"""
This is the sql part of the game.
Author: yanyongyu
"""

__author__ = "yanyongyu"
__all__ = ["Sql"]

import sqlite3
import os


class Sql():
    path = os.getcwd()

    @classmethod
    def __connect(cls):
        if "record.db" not in os.listdir(cls.path):
            conn = sqlite3.connect("record.db")
            cursor = conn.cursor()
            cursor.execute("create table record (score int primary key)")
            cursor.execute("insert into record (score) values (0)")
            cursor.close()
            conn.commit()
            conn.close()

        conn = sqlite3.connect("record.db")
        cursor = conn.cursor()
        return cursor, conn

    @classmethod
    def __close(cls, cursor, conn, commit=False):
        cursor.close()
        if commit:
            conn.commit()
        conn.close()

    @classmethod
    def get_score(cls):
        cursor, conn = cls.__connect()
        cursor.execute("select * from record")
        value = cursor.fetchone()
        cls.__close(cursor, conn)
        return value[0]

    @classmethod
    def set_score(cls, score):
        cursor, conn = cls.__connect()
        cursor.execute("update record set `score` = '%s'" % str(score))
        cls.__close(cursor, conn, commit=True)
