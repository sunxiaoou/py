#! /usr/bin/python3
import json
import os
import sys


def replace_rules_values(path: str, mapping_json: str):
    with open(mapping_json, 'r') as f:
        value_mapping = json.load(f)
    for filename in os.listdir(path):
        if filename.endswith('.json'):
            rule_file = os.path.join(path, filename)
            with open(rule_file, 'r') as f:
                data = json.load(f)
            for key in ['node_uuid', 'tgt_file_path', 'src_db_uuid', 'tgt_db_uuid']:
                if key in data:
                    origin_value = data[key]
                    if origin_value in value_mapping:
                        data[key] = value_mapping[origin_value]
                        print(f"replace '{origin_value}' to '{value_mapping[origin_value]}'")
            with open(rule_file, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"{rule_file} replaced")


def main():
    if len(sys.argv) < 3:
        print('Usage: {} rule_path mapping_json'.format(sys.argv[0]))
        sys.exit(1)
    replace_rules_values(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
