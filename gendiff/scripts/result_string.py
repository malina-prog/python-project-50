def format_diff(diff, indent=0):
    """Форматирование различий в читаемый вид"""
    lines = []
    space = '  ' * indent
    
    for key, value in diff.items():
        if not isinstance(value, dict):
            continue
            
        status = value.get('status')
        
        if status == 'nested':
            lines.append(f"{space}  {key}: {{")
            lines.append(format_diff(value['children'], indent + 2))
            lines.append(f"{space}  }}")
        elif status == 'changed':
            lines.append(f"{space}- {key}: {format_value(value['old_value'], indent)}")
            lines.append(f"{space}+ {key}: {format_value(value['new_value'], indent)}")
        elif status == 'unchanged':
            lines.append(f"{space}  {key}: {format_value(value['value'], indent)}")
        elif status == 'removed':
            lines.append(f"{space}- {key}: {format_value(value['value'], indent)}")
        elif status == 'added':
            lines.append(f"{space}+ {key}: {format_value(value['value'], indent)}")
    
    return '\n'.join(lines)


def format_value(value, indent):
    """Форматирование значений для вывода"""
    if isinstance(value, dict):
        space = '  ' * (indent + 1)
        items = []
        for k, v in value.items():
            items.append(f"{space}{k}: {format_value(v, indent + 1)}")
        return '{\n' + '\n'.join(items) + '\n' + '  ' * indent + '}'
    elif isinstance(value, list):
        return str(value)
    else:
        return str(value)