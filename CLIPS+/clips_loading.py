#####################Loading clips files
import os
from pathlib import Path
import re

from utils import read_file, text_output_clear, text_output_write


def load_clips_file(environment, filename, text_widget):
    if (len(list(environment.facts())) == 0 and
            len(list(environment.rules())) == 0 and
            len(list(environment.templates())) == 0 and
            len(list(environment.defined_facts())) == 0):
        environment.load(filename)
    else:
        handle_multiple_files(environment, filename)
    filetemp = 'temp.clp'
    environment.save(filetemp)
    text = read_file(filetemp)
    text_output_clear(text_widget)
    text_output_write(text_widget, text)
    os.remove(filetemp)
    environment.reset()


def handle_multiple_files(environment, filename):
    basename = Path(filename).stem
    with open(filename, encoding='utf-8-sig', errors='ignore') as f:
        construct_lines = []
        for line in f:
            if line == '\n':
                if len(construct_lines) == 0: continue
                construct = find_construct(environment, construct_lines)
                if construct is not None:
                    if not compare_constructs(construct_lines, construct):
                        rename_construct(construct_lines, basename)
                    else:
                        construct_lines = []
                        continue
                insert_construct(environment, construct_lines)
                construct_lines = []
            else:
                construct_lines.append(line)


def find_construct(environment, construct_lines):
    construct_type, construct_name = construct_lines[0].split()
    construct_type = construct_type[1:]
    try:
        if construct_type == 'deftemplate':
            return re.sub("MAIN::", "", str(environment.find_template(construct_name)))
        elif construct_type == 'deffacts':
            return re.sub("MAIN::", "", str(environment.find_defined_facts(construct_name)))
        elif construct_type == 'defrule':
            return re.sub("MAIN::", "", str(environment.find_rule(construct_name)))
    except Exception:
        return None


def compare_constructs(construct_lines, construct2):
    construct1 = re.sub("\n", "", " ".join(construct_lines))
    return "".join(construct1.split()) == "".join(construct2.split())


def rename_construct(construct_lines, postfix):
    construct_type, construct_name = construct_lines[0].split()
    construct_lines[0] = construct_type + " " + construct_name + postfix


def insert_construct(environment, construct_lines):
    construct = " ".join(construct_lines)
    environment.build(construct)
