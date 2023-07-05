import glob
import openai
from config import settings
import os
import pathlib
import re
import string

INPUT_DIR = "./data/chunks"
OUTPUT_DIR = "./data/csv"
CHAT_MESSAGE_TEMPLATE_RAW = "Generate a CSV with $line_count lines. Each line uses exactly one sequence of double-quoted words from this list: '$word_list'. The columns of the CSV are: \"words in indonesian, words in english, sentence in indonesian using the words, english translation, part of speech of the words\". The delimiter is \";\""
CHAT_MESSAGE_TEMPLATE = string.Template(CHAT_MESSAGE_TEMPLATE_RAW)

FIRST_CHUNK = 0

openai.api_key = settings["OPENAI_KEY"]

def make_openai_request(chunk):
  expressions = chunk.split("\n")
  content = CHAT_MESSAGE_TEMPLATE.substitute(
    line_count=len(expressions),
    word_list=", ".join([f"\"{expression}\"" for expression in expressions])
  )
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": content}]
  )
  return response["choices"][0]["message"]["content"]

def main():
  filenames = sorted(
    glob.glob("*", root_dir=INPUT_DIR),
    key=lambda filename: int(re.search(r'^(\d+)', filename).group(1))
  )
  for filename in filenames[FIRST_CHUNK:]:
    input_path = os.path.join(INPUT_DIR, filename)
    with open(input_path , "r") as input_file:
      output_filename = f"{pathlib.Path(filename).with_suffix('')}_output.csv"
      output_path = os.path.join(OUTPUT_DIR, output_filename)
      with open(output_path, "w") as output_file:
        csv = make_openai_request(input_file.read())
        output_file.write(csv)
        output_file.write(input_file.read())

main()
