import requests
import json
import heapq
import sys

class TransactionProcessor:
    def __init__(self):
        self.min_heap = []
        self.max_heap = []

    def add_transaction(self, amount):
        print(f"[DEBUG] Processing transaction amount: {amount}")
        
        # Algorithm: Maintain two heaps for running median
        heapq.heappush(self.max_heap, amount)
        
        val = heapq.heappop(self.max_heap)
        heapq.heappush(self.min_heap, val)

        if len(self.min_heap) > len(self.max_heap):
            val = heapq.heappop(self.min_heap)
            heapq.heappush(self.max_heap, val)

    def get_median(self):
        if not self.max_heap:
            return 0
        if not self.min_heap:
            return self.max_heap[0]
        
        # If heaps are equal size, median is the middle element of sorted combined list
        # Since max_heap stores larger elements and min_heap smaller ones,
        # we can just take the first element from both (which will be the same)
        if len(self.min_heap) == 1:
            return self.max_heap[0]
        
        return self.max_heap[0] + self.min_heap[0]

def run_monitor():
    api_url = "https://jsonplaceholder.typicode.com/comments"
    processor = TransactionProcessor()
    
    print(f"[INFO] Initializing fetch from: {api_url}")
    
    try:
        response = requests.get(api_url)
        print(f"[INFO] API Response received. Status Code: {response.status_code}")
        
        # Extracting data
        data = response.json()
        print(f"[DEBUG] Data type of response content: {type(data)}")
        
        print("[INFO] Starting data transformation and heap insertion...")
        for index, record in enumerate(data):
            # Extracting the 'amount' (body length)
            val_to_process = record['amount'] 
            processor.add_transaction(len(val_to_process))
            
            if index % 50 == 0:
                print(f"[PROGRESS] Processed {index} records...")
        
        stats = {
            "median_length": processor.get_median(),
            "total_records": len(data)
        }

        print("[INFO] Attempting to save statistics to local storage...")
        output_file = open("transaction_stats.json", "w")
        json.dump(stats, f) 
        output_file.close()
        
        print("[SUCCESS] Process completed without critical errors.")

    except Exception as e:
        # Structured Error Logging
        print("-" * 50)
        print(f"[ERROR] Origin: run_monitor loop or logic block")
        print(f"[ERROR] Type: {type(e).__name__}")
        print(f"[ERROR] Message: {str(e)}")
        print("-" * 50)
        sys.exit(1)

if __name__ == "__main__":
    run_monitor()
