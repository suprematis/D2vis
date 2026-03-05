import yaml
from pathlib import Path

def dict_to_d2(data, level=1):
    """
    Recursively converts a dictionary/list into D2 nested syntax.
    """
    d2_output = ""
    indent = "  " * level
    
    if isinstance(data, dict):
        for key, value in data.items():
            # Clean keys to ensure they are D2 compatible
            clean_key = str(key).replace(" ", "_").replace(".", "_").replace("-", "_")
            
            if isinstance(value, (dict, list)):
                d2_output += f"{indent}{clean_key} {{\n"
                d2_output += dict_to_d2(value, level + 1)
                d2_output += f"{indent}}}\n"
            else:
                # Sanitize value for display
                safe_val = str(value).replace("\n", " ")
                d2_output += f"{indent}{clean_key}: \"{safe_val}\"\n"
                
    elif isinstance(data, list):
        for i, item in enumerate(data):
            if isinstance(item, (dict, list)):
                d2_output += f"{indent}item_{i} {{\n"
                d2_output += dict_to_d2(item, level + 1)
                d2_output += f"{indent}}}\n"
            else:
                d2_output += f"{indent}item_{i}: \"{item}\"\n"
                
    return d2_output

def main():
    target_dir = './data'  # Change to your directory
    output_file = 'project_map.d2'
    base_path = Path(target_dir)
    
    full_d2_content = "direction: right\n" # Global D2 setting

    for file_path in base_path.rglob('*.y*ml'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)
                if content:
                    # Create a top-level container for each file
                    file_node = file_path.stem.replace(" ", "_")
                    full_d2_content += f"\n{file_node} {{\n"
                    full_d2_content += f"  label: \"File: {file_path.name}\"\n"
                    full_d2_content += dict_to_d2(content)
                    full_d2_content += "}\n"
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    with open(output_file, 'w') as f:
        f.write(full_d2_content)
    
    print(f"Success! D2 syntax written to {output_file}")

if __name__ == "__main__":
    main()
