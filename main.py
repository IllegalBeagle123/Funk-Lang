import re

file = "input"

with open(file + '.fl') as f:
  input = iter([re.sub(r'\s+(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)','',line) for line in f.read().split(';')])

def run(code, *args):
  matches = re.finditer(r'[a-zA-Z]+(?!\s*([\(\"a-zA-Z]))',code)
  for var in matches:
    code = re.sub(r'(?<![\w])'+var.group(0)+'(?![\w])',vars[var.group(0)],code)
  while not re.match(r'^((\(*(-?\d+|\".+\")(\.\d+)?\)*[+\-*\/]?)+)$',code):
    matches = re.finditer(r'([a-zA-Z]+)\(((-?\d+)(,-?\d+)*)\)',code)
    for var in matches:
      if var.group(1) == 'args':
        code = code.replace(var.group(0),args[int(var.group(2))])
      else:
        newargs = var.group(2).split(',')
        code = code.replace(var.group(0),run(var.group(1),*newargs))
  return str(eval(code))

vars = {}
for line in input:
  match = re.match(r'([a-zA-Z]+)\s*(\S?)=(.+)', line)
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
    elif match.group(2) == '$':
      vars[match.group(1)] = f"\"{str(run(match.group(3)))}\""
    if match.group(1) == 'out':
      print(vars["out"])