#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 01:33:42 2018

@author: v
"""
__version__="0.0.0"

__required__={}
__optional__={}

try:
    import cv2 as cv
    cv_available=True
except:
    cv_available=False
    
    