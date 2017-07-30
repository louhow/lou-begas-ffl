import re

regex_filters = [
	{
		'pattern': '\d+\.	(.*) \(.* \- (.*)\)	\$(\d+)',
		'replace': '\\1	\\2	\\3'
	}
]
with open('input.txt', 'r') as file:
	data = file.read()

print data

for regex_filter in regex_filters:
	print regex_filter
	pattern = re.compile(regex_filter['pattern'])
	data = pattern.sub(regex_filter['replace'], data)

with open('output.txt', 'w') as file:
	file.write(data)
