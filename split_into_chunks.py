import os
import re

INPUT_PATH = "./data/words.txt"
OUTPUT_DIR = "./data/chunks"
CHUNK_SIZE = 20

def generate_sentences(chunk, start_index):
  filename = f"{start_index}_{start_index + len(chunk) - 1}.txt"
  output_path = os.path.join(OUTPUT_DIR, filename)
  with open(output_path, "w") as output_file:
    output_file.write("\n".join(chunk))

def build_chunks(text):
  raw_words = re.split("\n", text)
  words = [word for word in raw_words if word]
  return [words[i:i + CHUNK_SIZE] for i in range(0, len(words), CHUNK_SIZE)]

def main():
  with open(INPUT_PATH, "r") as input_file:
    chunks = build_chunks(input_file.read())
    start_index = 0
    for chunk in chunks:
      generate_sentences(chunk, start_index)
      start_index += len(chunk)

main()
