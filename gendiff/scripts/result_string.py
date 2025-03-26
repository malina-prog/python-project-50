

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
        elif result_dict[i][1] == '+':
            result_string += (f'    {i}: {result_dict[i][0]}\n')
    result_string += '}'
    print(result_string)
    return result_string()