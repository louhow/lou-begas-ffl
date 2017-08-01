import re

class FileFilter(object):
  def __init__(self, file, filters):
    self.file = file
    self.filters = filters

  def get_input_file(self):
    return self.file + "_input.txt"

  def get_output_file(self):
    return self.file + "_output.txt"


class Filter(object):
  def __init__(self, pattern, replace):
    self.pattern = pattern
    self.replace = replace

file_filters = [
  # https://www.fantasypros.com/nfl/auction-values/calculator.php
  FileFilter(
    'fantasypros',
    [
      Filter(
        '\d+\.	(.*) \(.* \- (.*)\)	\$(\d+)',
        '\\1  \\2  \\3'
      )
    ]
  ),
  # https://football.fantasysports.yahoo.com/f1/91636/1/prerank_auction_costs
  FileFilter(
    'yahoo',
    [
      Filter(
        '\$\-',
        '$0.0'
      ),
      Filter(
        '.*layer Note.*\n'
        '(.*) .* \- (RB|WR|TE|QB|K|DEF) ?.*\n'
        '(.*\n)?'
        '.* \d+:\d+.*\n'
        '\$\n'
        '\d+\n'
        '-	\$(\d+)	\$(\d+)	\$(\d+\.\d+)	.*\n',
        '\\1	\\2	\\5	\\6'
      )
    ]
  ),
  # http://games.espn.com/ffl/livedraftresults?sort=aav
  FileFilter(
    'espn',
    [
      Filter(
        '\d+	(.*), ..(.?)	(RB|WR|TE|QB|K)	.*	.*	(.*)	.*	.*',
        '\\1	\\3	\\4'
      ),
      Filter(
        '.*(\+|\-).*\n', ''  # Remove defenses
      )
    ]
  ),
  # http://fantasy.nfl.com/research/rankings?leagueId=393651&statType=draftStatss
  FileFilter(
    'nfl',
    [
      Filter('View Videos\n', ''),
      Filter('DEF', 'DEF -'),  # Ugly, but insert the hyphen to match on for all other casess
      Filter(
        '\d+.*\n'
        '(.*)(RB|WR|QB|TE|DEF|K) \-.*	(\d+)',
        '\\1	\\2	\\3'
      )
    ]
  )
]

constant_filters = [
  Filter('(Jr\. )?', '')
]

def apply_filters(data, filters):
  for filt in filters:
    pattern = re.compile(filt.pattern)
    data = pattern.sub(filt.replace, data)

  return data

for file_filter in file_filters:
  with open(file_filter.get_input_file(), 'r') as file:
    data = file.read()

  data = apply_filters(data, file_filter.filters)
  data = apply_filters(data, constant_filters)

  with open(file_filter.get_output_file(), 'w') as file:
    file.write(data)
