# -*- coding: utf-8 -*-
"""Created on Thu Jun 26 02:44:22 2025@author: Alexm"""


# script.py

if False:
    ## do not change anything below
    if 'live_variable_outputs' not in globals().keys():
        from debugging_tools import live_variable_outputs
    import time
    
    print('Start')
    foo = [1, 2, 3]
    
    list_ui = live_variable_outputs()
    
    for n in range(10):
        foo.append(n)
        list_ui.insert(n)
        time.sleep(0.5)
    
    print('Finished')
    
    


from multiprocessing import Process, Pipe
import time

def worker(conn):
    while True:
        if conn.poll():
            msg = conn.recv()
            print(f"[Worker] Received: {msg}")
            if msg == "exit":
                break
            conn.send(f"ACK: {msg}")
        time.sleep(0.1)

def main():
    parent_conn, child_conn = Pipe()
    p = Process(target=worker, args=(child_conn,))
    p.start()

    print("Main process doing stuff...")
    for i in range(5):
        time.sleep(1)
        parent_conn.send(f"Hello {i}")
        if parent_conn.poll():
            response = parent_conn.recv()
            print(f"[Main] Got back: {response}")

    parent_conn.send("exit")
    p.join()
    print("Finished.")

if __name__ == "__main__":
    main()
    
    
    
if False:# ui 
    from PyQt5.QtWidgets import QApplication, QInputDialog
    import sys
    
    def input_ui(prompt="Enter something:"):
        app = QApplication.instance() or QApplication(sys.argv)
        text, ok = QInputDialog.getText(None, "Input", prompt)
        if ok and text:
            return text
        return None
    
    # Example use
    z = input_ui("What's your name?")
    print(f"You entered: {z}")   
        
        
    
    
    
    
    
