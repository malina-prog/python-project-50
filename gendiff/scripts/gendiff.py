import argparse
import json
#from gendiff.scripts import result_string

def main():
    parser = argparse.ArgumentParser(description="Compares two configuration files and shows a difference.")
    parser.add_argument('first_file', type=str,)
    parser.add_argument('second_file', type=str,)
    parser.add_argument("-f", "--format",help="Set format of output.",default="stylish",)

    args = parser.parse_args()
    diff = generate_diff(args.first_file, args.second_file)
    print(diff)
    
def generate_diff(file1_path, file2_path):
    try:
        with open(file1_path, 'r') as file:
            parsed_dict1 = json.load(file)
        with open(file2_path, 'r') as file:
            parsed_dict2 = json.load(file)
    except FileNotFoundError as e:
        return f"Error: {e}"
    
    result_dict={}

    for i in parsed_dict1:
        if i not in parsed_dict2:
            result_dict[i]=[parsed_dict1[i],'-']
        elif parsed_dict2[i] == parsed_dict1[i]:
            result_dict[i] = [parsed_dict1[i],None]
        elif parsed_dict2[i] != parsed_dict1[i]:
            result_dict[i] = {'old':parsed_dict1[i],'new':parsed_dict2[i]}

    for i in parsed_dict2:
        if i not in parsed_dict1:
            result_dict[i]=[parsed_dict2[i],'+']
    sorted_dict = {k: result_dict[k] for k in sorted(result_dict)}
    res_str=result_string(sorted_dict)
    return res_str

def result_string(result_dict):
    result_string = '{\n'
    for i in result_dict:
        if isinstance(result_dict[i], dict):
            result_string += (f'  - {i}: {result_dict[i]["old"]}\n')
            result_string += (f'  + {i}: {result_dict[i]["new"]}\n')
        elif result_dict[i][1] == '-':
            result_string += (f'  - {i}: {result_dict[i][0]}\n')
        elif result_dict[i][1] == '+':
            result_string += (f'  + {i}: {result_dict[i][0]}\n')
        elif result_dict[i][1] == None:
            result_string += (f'    {i}: {result_dict[i][0]}\n')
    result_string += '}'

    return result_string



if __name__ == "__main__":
    main()

