#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import MySQLdb


class LuoguUser(object):
    """
    LuoguUser
    """

    def __init__(self, name: str, contribution: int, active: int,
                 integral: int, ac_num: int, submit_num: int, *args, **kwargs):
        """
        Args:
            name: User's name
            contribution: emmmmm
            active: emmmmm
            integral: emmmmm
            ac_num: User's accepted topics number in all
            submit_num: User's submit topics number in all 
        """
        this.name = name
        this.contribution = contribution
        this.active = active
        this.integral = integral
        this.ac_num = ac_num
        this.submit_num = submit_num

        for key, value in kwargs.items():
            setattr(self, key, value)