import sys

with open(sys.argv[2]) as f2:
  kept_lines = [line for line in f2.read().split('\n') if line]
  with open(sys.argv[1]) as f1:
    for line in f1:
      stripped = line.strip('\n')
      if stripped in kept_lines:
        print(stripped)