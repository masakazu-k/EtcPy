#!/usr/bin/pythonw
#--*-- encoding:utf-8 --*--

import re,sys,os

reinput = re.compile('\\\\input\{(.+?)\}')
relabel = re.compile('\\\\label\{(.+?)\}')
reref = re.compile('\\\\ref\{(.+?)\}')

def search_lm(s,m):
	l = len(s)
	i = 0
	c = 0
	r = []
	while i < l:
		t = s.find(m,i)
		if t == -1:
			break
		for g in range(i,t):
			if s[g] == '\n':
				c = c+1
				lm = g
		r = r + [[c,t-lm]]
		i = t + len(m)+1
	return r

def inputfiles(dr,texfile):
	fl = []
	f = open(dr+texfile,'r').read()
	il = reinput.findall(f)
	for i in il:
		if i[-4:] != '.tex':
			continue
		fl.append(i)
		tfl = inputfiles(dr,i)
		fl = list(set(fl)|set(tfl))
	return fl

def labelsfileslist(dr,texfiles):
	ll = []
	for texfile in texfiles:
		f = open(dr+texfile,'r').read()
		il = relabel.findall(f)
		ll = list(set(ll)|set(il))
	return ll

def labelsfiles(dr,texfiles):
	ll = {}
	for texfile in texfiles:
		f = open(dr+texfile,'r').read()
		il = relabel.findall(f)
		ll[texfile] = {}
		for i in il:
			ll[texfile][i] = search_lm(f,i)
	return ll

def refsfiles(dr,texfiles):
	ll = {}
	for texfile in texfiles:
		f = open(dr+texfile,'r').read()
		il = reref.findall(f)
		ll[texfile] = {}
		for i in il:
			ll[texfile][i] = search_lm(f,i)
	return ll

def labelslist(dr,texfile):
	e = inputfiles(dr,texfile)
	e = list(set(e)|set([texfile]))
	alllabels = labelsfileslist(dr,e)
	labels = labelsfiles(dr,e)
	refs = refsfiles(dr,e)
	ret = {}
	ret['alllabels'] = alllabels
	ret['labels'] = labels
	ret['refs'] = refs
	return ret