# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 01:59:48 2026

@author: alexm
"""

from collections import defaultdict
from dataclasses import dataclass
import time



class PrintAverageTimes:
    @dataclass
    class StageStats:
        label: str = ""
        total_time: float = 0.0
        count: int = 0

    def __init__(self, snooze=False):
        self.last_time = time.perf_counter()
        self.snooze = snooze
        # Use type(self) to safely reference the nested class dynamically
        self.stats = defaultdict(type(self).StageStats)
        self.table_width = 65
        self.label_length = 15
    
    @property
    def count(self):
        if self.snooze:
            return 0
        key = list(self.stats.keys())[0]
        return self.stats[key].count

    def __call__(self, stage_id: int, label: str):
        """Records time elapsed since the previous call."""
        if not self.snooze:
            now = time.perf_counter()
            elapsed = now - self.last_time
            self.last_time = now
    
            stat = self.stats[stage_id]
            stat.label = label
            stat.total_time += elapsed
            stat.count += 1
            self.label_length = max(len(label), self.label_length)

    def print_summary(self):
        """Prints a consolidated summary table and resets the timer baseline."""
        if not self.snooze:
            print("\n" + "=" * self.table_width)
            print(
                f"{'Stage':<7} | {'Label':<{self.label_length+2}} | {'Calls':<8} | {'Avg Time (ms)':<15}"
                f" | {'Total (s)':<10}"
            )
            print("-" * self.table_width)
            for stage_id in sorted(self.stats.keys()):
                data = self.stats[stage_id]
                count = data.count
                total = data.total_time
                avg_ms = (total / count * 1000) if count > 0 else 0.0
                print(
                    f"{stage_id:<7} | {data.label:<{self.label_length+2}} | {count:<8} | {avg_ms:<15.3f}"
                    f" | {total:<10.4f}"
                )
            print("=" * self.table_width)
            print('#Note:Timetaken is for the code between it and the previous statement' + "\n")
            self.last_time = time.perf_counter()
            
            
        
if __name__ == "__main__":

    # Initialize the timer
    timer = PrintAverageTimes()

    # Stage 1: Setup / Initialization (run once)
    time.sleep(0.05)
    timer(1, "Initialization")

    # Stage 2: Simulating a loop of data processing batches
    for batch in range(3):
        time.sleep(0.1)  # Simulate batch processing time
        timer(2, "Process Batch")

    # Stage 3: A different sub-task inside a loop
    for epoch in range(2):
        time.sleep(0.2)  # Simulate model training/step time
        timer(3, "Training Step")

    # Stage 4: Cleanup / Finalize (run once)
    time.sleep(0.02)
    timer(4, "Cleanup")

    # Print the final report
    timer.print_summary()        
        
    


    
    
    
    
    
    
    
    
        
        