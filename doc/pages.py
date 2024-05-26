#!/usr/bin/env python

import datetime
import jinja2
import sys
import os

numreleases = 3

srcdirs = sys.argv[1].split(":")

env = jinja2.Environment(
	loader = jinja2.FileSystemLoader(srcdirs),
	autoescape = jinja2.select_autoescape()
)

stuff = {}
news = []

def nextline(n):
	return n.readline().rstrip()

def skipblank(l, n):
	while l == "":
		l = n.readline().rstrip()
	return l

# this is extremely stupid
def parserel(l, news):
	summary = []
	issues = []
	merges = []
	translations = []

	# Overview of changes in Rhythmbox x.y.z
	# =====
	#
	l = skipblank(l, news)
	release = l.split(" ")[-1]
	news.readline()
	news.readline()

	l = nextline(news)
	while l != "":
		# * change summary item
		if l.startswith("* "):
			summary.append(l[2:])
		else:
			summary[-1] = summary[-1] + " " + l.lstrip()
		l = nextline(news)

	l = skipblank(l, news)

	if l.startswith("Issues fixed"):
		l = skipblank(nextline(news), news)

		while l != "":
			# nnn - issue title
			[number, _, title] = l.split(" ", 2)
			issues.append({ "number": number, "title": title})
			l = nextline(news)

	l = skipblank(l, news)

	if l.startswith("Merge requests"):
		l = skipblank(nextline(news), news)

		while l != "":
			# mmm - merge request title
			[number, _, title] = l.split(" ", 2)
			merges.append({ "number": number, "title": title})
			l = news.readline().rstrip()

		l = skipblank(l, news)

	if l.startswith("Translation"):
		l = skipblank(nextline(news), news)

		while l.startswith("- "):
			# - xx, courtesy of name
			translations.append(l[2:])
			l = nextline(news)

		l = skipblank(l, news)

	r = {
		"version": release,
		"date": "???????",
		"summary": summary,
		"issues": issues,
		"merges": merges,
		"translations": translations
	}
	return (l, r)

news = []
with open(os.path.join(srcdirs[0], "NEWS")) as n:
	l = n.readline().rstrip()
	while len(news) < numreleases:
		(l, r) = parserel(l, n)
		news.append(r)

stuff['news'] = news
# get plugin files, load into a list

for p in sys.argv[2:]:
	with open(p, 'w') as f:
		f.write(env.get_template(p).render(stuff))

