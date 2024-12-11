import json
import random

class Benchmark:
    def __init__(self, path):
        data = self.__load_jsonl(path)
        
        vulnerable_data = [item for item in data if item.get('vulnerable') == 1]
        non_vulnerable_sample = random.sample([item for item in data if item.get('vulnerable') == 0], 10)
        
        self.data = vulnerable_data + non_vulnerable_sample
        random.shuffle(self.data)
        
    def __load_jsonl(self, path):
        with open(path, 'r') as file:
            data = [json.loads(line) for line in file]
        return data
    
    def __iter__(self):
        return iter(self.data)
    

    

        
