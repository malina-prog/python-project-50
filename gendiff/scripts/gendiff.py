import argparse
import json
import yaml
from gendiff.scripts.result_string import format_diff


def main():
    parser = argparse.ArgumentParser(description="Compares two configuration files and shows a difference.")
    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)
    parser.add_argument("-f", "--format", help="Set format of output", default="stylish")

    args = parser.parse_args()
    diff = generate_diff(args.first_file, args.second_file)
    print(diff)


def has_json_extension(filename):
    return filename.lower().endswith('.json')


def generate_diff(file1_path, file2_path):
    try:
        if has_json_extension(file1_path):
            with open(file1_path, 'r') as file:
                parsed_dict1 = json.load(file)
            with open(file2_path, 'r') as file:
                parsed_dict2 = json.load(file)
        else:
            with open(file1_path, 'r') as file:
                parsed_dict1 = yaml.safe_load(file) or {}
            with open(file2_path, 'r') as file:
                parsed_dict2 = yaml.safe_load(file) or {}
    except FileNotFoundError as e:
        return f"Error: {e}"
    except (json.JSONDecodeError, yaml.YAMLError) as e:
        return f"Error parsing file: {e}"

    diff = compare_dicts(parsed_dict1, parsed_dict2)
    return format_diff(diff)


def compare_dicts(dict1, dict2, path=""):
    result = {}
    all_keys = sorted(set(dict1.keys()) | set(dict2.keys()))
    
    for key in all_keys:
        if key in dict1 and key in dict2:
            val1 = dict1[key]
            val2 = dict2[key]
            
            if isinstance(val1, dict) and isinstance(val2, dict):
                nested_diff = compare_dicts(val1, val2, path)
                if nested_diff:
                    result[key] = {'status': 'nested', 'children': nested_diff}
            elif val1 != val2:
                result[key] = {
                    'status': 'changed',
                    'old_value': val1,
                    'new_value': val2
                }
            else:
                result[key] = {'status': 'unchanged', 'value': val1}
        elif key in dict1:
            result[key] = {'status': 'removed', 'value': dict1[key]}
        else:
            result[key] = {'status': 'added', 'value': dict2[key]}
    
    return result


if __name__ == "__main__":
    main()