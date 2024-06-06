import filecmp
import os
import datetime as dt
import shutil

INPUT_FOLDER = "inputs"
OUTPUT_FOLDER = "outputs"
PRESC_FOLDER = "outputs/presc"
NON_PRESC_FOLDER = "outputs/non-presc"

def main():
  output_dir = get_output_dir()
  input_scans = filter_input_scans()
  copy_files(input_scans, output_dir)


def get_output_dir():
  now = dt.datetime.now()
  dir = now.strftime("%b_%d")
  output_dir = f"{OUTPUT_FOLDER}/{dir}"
  ensure_dir_exists(output_dir)
  return output_dir


def ensure_dir_exists(dir_name):
  if not os.path.exists(dir_name):
    os.makedirs(dir_name)


def filter_input_scans():
  inputs = set(os.listdir(INPUT_FOLDER))
  prescs = set(os.listdir(PRESC_FOLDER))
  non_presc = set(os.listdir(NON_PRESC_FOLDER))
  latest = (inputs - prescs) - non_presc

  dups_presc = get_duplicates(INPUT_FOLDER, PRESC_FOLDER)
  dups_non = get_duplicates(INPUT_FOLDER, NON_PRESC_FOLDER)

  print(f"Total new scans: {len(inputs)}")
  print(f"Duplicate prescriptions: {len(dups_presc)}")
  print(f"Duplicate non-presc scans: {len(dups_non)}")
  print(f"Latest (unique) new scans: {len(latest)}")

  return list(latest)


def get_duplicates(input_folder, old_folder):
  inputs = set(os.listdir(input_folder))
  old = set(os.listdir(old_folder))

  pot_dups = inputs & old
#  print(f"Potential duplicates: {len(pot_dups)}")

  dups = set()
  for file in pot_dups:
    one = f"{input_folder}/{file}"
    two = f"{old_folder}/{file}"
    if filecmp.cmp(one, two, shallow=False):
      dups.add(file)
    else:
      print(f"Not the same? one: {one}, two: {two}")

  return dups


def copy_files(docs, dir):
  for doc in docs:
    shutil.copy(f"{INPUT_FOLDER}/{doc}", f"{dir}/{doc}")

if __name__ == "__main__":
  main()