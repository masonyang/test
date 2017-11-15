#!/usr/bin/env python
# coding: utf-8

import os, subprocess
class Tesseract:
    def run_eng(self, filename):
        self.filename = filename
        base,ext = os.path.splitext(filename)
        command = '/usr/local/bin/tesseract '+self.filename+' stdout -l eng --psm 6'
        p = os.popen(command).readlines()
        return self.print_s(p)
    def run_jpn(self, filename):
        self.filename = filename
        base,ext = os.path.splitext(filename)
        command = '/usr/local/bin/tesseract '+self.filename+' stdout -l jpn --psm 6'
        p = os.popen(command).readlines()
        return self.print_s(p)
    def run_chi_en(self,filename):
        self.filename = filename
        base,ext = os.path.splitext(filename)
        command = '/usr/local/bin/tesseract '+self.filename+' stdout -l eng+chi_sim --psm 6'
        p = os.popen(command).readlines()
        return self.print_s(p)
    def print_s(self,p):
        s=''
        for i in p:
            s+=i
        return s