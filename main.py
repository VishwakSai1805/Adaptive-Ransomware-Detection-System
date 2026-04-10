import time

class AutomataEngine:
    def __init__(self):
        # Initial states
        self.file_state = 'SAFE'
        self.net_state = 'SAFE'
        self.alarm_triggered = False

        # File System DFA (M1) Transition Table
        self.file_transitions = {
            'SAFE': {'read': 'SAFE', 'write': 'SAFE', 'rapid_rename': 'SUSPICIOUS'},
            'SUSPICIOUS': {'read': 'SAFE', 'encrypt_call': 'COMPROMISED'},
            'COMPROMISED': {'read': 'COMPROMISED', 'rapid_rename': 'COMPROMISED', 'ANY': 'COMPROMISED'} 
        }

        # Network DFA (M2) Transition Table
        self.net_transitions = {
            'SAFE': {'dns_query': 'SAFE', 'http_get': 'SAFE', 'port_scan_445': 'SUSPICIOUS'},
            'SUSPICIOUS': {'http_get': 'SAFE', 'smb_exploit': 'COMPROMISED'},
            'COMPROMISED': {'dns_query': 'COMPROMISED', 'smb_exploit': 'COMPROMISED', 'ANY': 'COMPROMISED'} 
        }

    def process_event(self, domain, event):
        # Update the respective state machine based on the domain
        if domain == 'FILE_SYS' and event in self.file_transitions[self.file_state]:
            self.file_state = self.file_transitions[self.file_state][event]
            
        elif domain == 'NETWORK' and event in self.net_transitions[self.net_state]:
            self.net_state = self.net_transitions[self.net_state][event]

        # Evaluate the Cartesian product after every transition
        self.check_supervisor()

    def check_supervisor(self):
        # Global alarm triggers only when both DFAs hit the trap state
        if self.file_state == 'COMPROMISED' and self.net_state == 'COMPROMISED':
            if not self.alarm_triggered:
                print("\n[!!!] CRITICAL: WANNACRY RANSOMWARE BEHAVIOR DETECTED [!!!]")
                print("-> Intersection of Malicious File and Network states reached.\n")
                self.alarm_triggered = True

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    engine = AutomataEngine()
    print("--- INITIALIZING HIERARCHICAL AUTOMATA ENGINE ---\n")
    
    try:
        with open('system_logs.txt', 'r') as file:
            for line in file:
                # Expected format: DOMAIN,event
                domain, event = line.strip().split(',')
                
                # Process the log token
                engine.process_event(domain, event)
                
                # Real-time state tracing output
                print(f"Read: {event.ljust(15)} | Tuple State -> ({engine.file_state}, {engine.net_state})")
                time.sleep(0.5) 
                
    except FileNotFoundError:
        print("Error: 'system_logs.txt' missing. Please run the simulator first.")