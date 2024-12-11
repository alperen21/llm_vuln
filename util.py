import json
import os

def create_session(cwe_number):
    # session_data = {"cwe_number": cwe_number}
    call_graph_file = f"benchmark/{cwe_number}_mapping.json"
    benchmark_file = f"benchmark/{cwe_number}.jsonl"
    session_data = {
        "cwe_number": cwe_number,
        "call_graph_file": call_graph_file,
        "benchmark_file": benchmark_file
    }
    with open("current_session.json", "w") as file:
        json.dump(session_data, file)
        
        
def get_all_jsonl_files(directory):
    jsonl_files = [f for f in os.listdir(directory) if f.endswith('.jsonl')]
    return jsonl_files


def get_file_name(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]

def get_cwe(file_path):
    return get_file_name(file_path)

def get_corresponding_mapping_file(file_path):
    file_name = get_file_name(file_path)
    return f"./benchmark/{file_name}_mapping.json"