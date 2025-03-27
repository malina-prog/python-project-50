import pytest
import json
import os
from gendiff.scripts.gendiff import generate_diff

def create_test_file(path, content):
    with open(path, 'w') as f:
        json.dump(content, f)

@pytest.fixture(scope="module", autouse=True)
def setup_teardown():

    test_data = {
        'file1.json': {'key': 'value', 'unchanged': 'same', 'changed': 'old'},
        'file2.json': {'key': 'value', 'unchanged': 'same', 'changed': 'new', 'added': 'new_value'},
        'empty.json': {},
        'file1_nested.json': {'nested': {'key': 'value'}},
        'file2_nested.json': {'nested': {'key': 'changed'}}
    }
    
    for filename, content in test_data.items():
        create_test_file(filename, content)
    
    yield  
    

    for filename in test_data.keys():
        if os.path.exists(filename):
            os.remove(filename)


@pytest.mark.parametrize("file1, file2, expected", [

    ('file1.json', 'file2.json', 
     '{\n  + added: new_value\n  - changed: old\n  + changed: new\n    key: value\n    unchanged: same\n}'),
    

    ('empty.json', 'empty.json', '{\n}'),
    
    ('empty.json', 'file1.json', 
     '{\n  + key: value\n  + unchanged: same\n  + changed: old\n}'),
    

    ('file1_nested.json', 'file2_nested.json', 
     '{\n  - nested: {\'key\': \'value\'}\n  + nested: {\'key\': \'changed\'}\n}')
])
def test_generate_diff(file1, file2, expected):
    assert generate_diff(file1, file2) == expected


@pytest.mark.parametrize("file1, file2, expected_error", [
    ('nonexistent.json', 'file1.json', "Error: [Errno 2] No such file or directory: 'nonexistent.json'"),
    ('file1.json', 'nonexistent.json', "Error: [Errno 2] No such file or directory: 'nonexistent.json'")
])
def test_generate_diff_errors(file1, file2, expected_error):
    assert generate_diff(file1, file2) == expected_error