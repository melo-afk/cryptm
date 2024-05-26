import argparse
import importlib.util
import os
import sys
import re
from types import ModuleType

EXCLUDE_FOLDER = 'graveyard'
SCRIPTS_FOLDER = 'modules'
DEBUG = False


def load_script(script_name: str) -> ModuleType:
    """
    load the script 
    """
    script_path = os.path.join(SCRIPTS_FOLDER, script_name + '.py')
    if not os.path.exists(script_path):
        print(f"Script '{script_name}' not found.")
        sys.exit(1)

    if DEBUG:
        print(f"Loading script from {script_path}")

    module_name = os.path.splitext(os.path.basename(script_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load the script")
    script_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(script_module)
    return script_module


def parse_md_file(md_file_path: str) -> str:
    """
    parse .md file
    """
    if not os.path.exists(md_file_path):
        return ""
    with open(md_file_path, 'r', encoding="utf-8") as f:
        content = f.read()
    match = re.search(r'\[info\]: <> \((.*?)\)', content)
    if match:
        return match.group(1).strip()
    return ""


def list_scripts(directory: str=SCRIPTS_FOLDER) -> list[tuple[str,str]]:
    """
    Get all scripts from a folder
    """
    scripts = []
    for root, dirs, files in os.walk(directory):

        if EXCLUDE_FOLDER in dirs:
            dirs.remove(EXCLUDE_FOLDER)
        for file in files:
            if file.endswith('.py') and not file.startswith("__"):
                script_path = os.path.join(root, file)
                with open(script_path, 'r', encoding="utf-8") as f:
                    content = f.readlines()
                docstring = ""
                in_docstring = False
                for line in content:
                    if line.strip() == '"""':
                        in_docstring = not in_docstring
                        continue
                    if in_docstring and "[" in line and "]" in line and ("+" in line or "-" in line):
                        docstring = line.strip()
                        break
                    in_docstring = False
                relative_script_name = os.path.relpath(script_path, SCRIPTS_FOLDER)
                script_name = os.path.splitext(relative_script_name)[0]
                scripts.append((script_name, docstring))

        for dir in dirs:
            md_file_path = os.path.join(root, dir, "README.md")
            md_content = parse_md_file(md_file_path)
            if md_content:
                relative_dir_name = os.path.relpath(os.path.join(root, dir), SCRIPTS_FOLDER)
                scripts.append((f"{relative_dir_name}/", md_content))
                
    return scripts


def print_aligned_table(scripts: list[tuple[str,str]]) -> None:
    """"
    pretty print a nice table
    """
    # Split descriptions into main part, bracketed part, and symbols
    split_descriptions = []
    for name, desc in scripts:
        if '[' in desc and ']' in desc:
            main_desc, remainder = desc.split('[')
            bracketed_desc, symbols = remainder.split(']')
            bracketed_desc = '[' + bracketed_desc + ']'
            symbols = symbols.strip()
        else:
            main_desc, bracketed_desc, symbols = desc, '', ''
        split_descriptions.append(
            (name.replace('\\','/'), main_desc.strip(), bracketed_desc.strip(), symbols))

    # Sort scripts by category
    split_descriptions.sort(key=lambda x: x[2].lower())

    # Calculate the maximum length for each column
    max_name_len = max(len(name) for name, _, _, _ in split_descriptions)
    max_desc_len = max(len(desc) for _, desc, _, _ in split_descriptions)
    max_bracket_len = max(len(bracket)
                          for _, _, bracket, _ in split_descriptions)
    max_symbols_len = max(len(symbols)
                          for _, _, _, symbols in split_descriptions)

    # Print the headers
    header = f"   {'Script Name'.ljust(max_name_len)} : {'Description'.ljust(max_desc_len)} {'Category'.ljust(max_bracket_len)} {'Rating'.ljust(max_symbols_len)}"
    print(header)
    print('-' * len(header))  # Print a separator line

    for name, desc, bracket, symbols in split_descriptions:
        print(f" - {name.ljust(max_name_len)} : {desc.ljust(max_desc_len)} {bracket.ljust(max_bracket_len)} {symbols.ljust(max_symbols_len)}")


def main() -> None:
    """
    Main entrypoint
    """
    parser = argparse.ArgumentParser(
        description='CLI to run some (crypto) math scripts')
    parser.add_argument('method', nargs='?', help='Name of the script to run')
    parser.add_argument(
        'script_args',
        nargs=argparse.REMAINDER,
        help='Arguments to pass to the script')
    parser.add_argument(
        '-l',
        '--list',
        action='store_true',
        help='list available methods/scripts')

    args = parser.parse_args()
    if args.list or any(x in ('--list', '-l') for x in args.script_args):
        directory = f"{SCRIPTS_FOLDER}/{args.method}" if args.method else SCRIPTS_FOLDER
        if not os.path.exists(directory):
            print(f"Directory '{directory}' not found.")
            sys.exit(1)
        scripts = list_scripts(directory)
        print_aligned_table(scripts)
        sys.exit(0)

    if not args.method:
        parser.print_help()
        sys.exit(1)

    sys.path.insert(0, os.path.abspath(SCRIPTS_FOLDER))
    script_module = load_script(args.method)
    script_module.main(sys.argv[0], args.method, args.script_args)


if __name__ == '__main__':
    main()
