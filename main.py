from agent import Agent
from benchmark import Benchmark
from tools import REACT_TOOLS 
from util import create_session, get_all_jsonl_files, get_corresponding_mapping_file, get_cwe
import json
import os
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from prompt import construct_prompt


LLM = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def write_results(cwe, results):
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)
    results_file = os.path.join(results_dir, "cwe_results.json")

    if os.path.exists(results_file):
        with open(results_file, "r") as f:
            all_results = json.load(f)
    else:
        all_results = {}

    all_results[cwe] = results

    with open(results_file, "w") as f:
        json.dump(all_results, f, indent=4)

def experiment(cwe, benchmark):
    agent = Agent(
        llm=LLM,
        tools=REACT_TOOLS
    )
    
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    
    correct_cwe = 0
    false_cwe = 0
    
    for item in benchmark:
        file_path = item['file_path']
        function_signature = item['function_signature']
        function_body = item['function_body']
        cwe = item['cwe']
        vulnerable = item['vulnerable']
        
        prompt = construct_prompt(function_body)
        vulnerability_prediction, cwe_prediction = agent.predict(prompt)
        
        if vulnerability_prediction == 1 and vulnerable == 1:
            tp += 1
        elif vulnerability_prediction == 0 and vulnerable == 0:
            tn += 1
        elif vulnerability_prediction == 1 and vulnerable == 0:
            fp += 1
        elif vulnerability_prediction == 0 and vulnerable == 1:
            fn += 1
        
        if cwe_prediction.lower() == cwe.lower():
            correct_cwe += 1
        else:
            false_cwe += 1
            
    
    return {
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "correct_cwe": correct_cwe,
        "false_cwe": false_cwe
    }
        

def main():
    jsonl_files = get_all_jsonl_files("./benchmark")
    
    for jsonl_file in jsonl_files:
        cwe_number = get_cwe(jsonl_file)
        create_session(cwe_number)
        
        benchmark = Benchmark(f"./benchmark/{jsonl_file}")
        
        results = experiment(
            cwe=cwe_number,
            benchmark=benchmark
        )
        
        write_results(cwe_number, results)
        
    
    print("Experiments completed.")
        

if __name__ == "__main__":
    main()