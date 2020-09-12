import re

file = "input"

with open(file + '.fl') as f:
  input = iter([''.join(line.split()) for line in f.read().split(';')])

def run(code, *args):
  matches = re.finditer('[a-zA-Z]+(?!(\(|[a-zA-Z]))',code)
  for var in matches:
    code = re.sub('(?<![\w])'+var.group(0)+'(?![\w])',vars[var.group(0)],code)
  while not re.match('^(\(*-?\d+(\.\d+)?\)*[+\-*\/]?)+$',code):
    matches = re.finditer('([a-zA-Z]+)\(((-?\d+)(,-?\d+)*)\)',code)
    for var in matches:
      if var.group(1) == 'args':
        code = code.replace(var.group(0),args[int(var.group(2))])
      else:
        newargs = var.group(2).split(',')
        code = code.replace(var.group(0),run(var.group(1),*newargs))
  return str(eval(code))

vars = {}
for line in input:
  match = re.match('([a-zA-Z]+)(\S?)=(\S+)', line)
  if match:
    if not match.group(2):
      vars[match.group(1)] = match.group(3)
    elif match.group(2) == '&':
      vars[match.group(1)] = run(match.group(3))
    elif match.group(2) == '?':
      if not run(vars[match.group(1)]) == run(match.group(3)):
        next(input)
    elif match.group(2) == '!':
      if run(vars[match.group(1)]) == run(match.group(3)):
        next(input)
    elif match.group(2) == '>':
      if not run(vars[match.group(1)]) >= run(match.group(3)):
        next(input)
    elif match.group(2) == '<':
      if not run(vars[match.group(1)]) <= run(match.group(3)):
        next(input)
    if match.group(1) == 'out':
      print(vars["out"])