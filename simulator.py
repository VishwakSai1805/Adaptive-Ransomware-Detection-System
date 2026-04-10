import time
import random

def generate_logs():
    # The normal background noise
    normal_events = [
        ("FILE_SYS", "read"), 
        ("FILE_SYS", "write"), 
        ("NETWORK", "dns_query"), 
        ("NETWORK", "http_get")
    ]
    
    # The specific WannaCry behavior we want to catch
    attack_sequence = [
        ("FILE_SYS", "rapid_rename"), 
        ("NETWORK", "port_scan_445"), 
        ("FILE_SYS", "encrypt_call"), 
        ("NETWORK", "smb_exploit")
    ]

    print("--- INITIATING TRAFFIC SIMULATOR ---\n")
    
    # Open a text file to save the logs
    with open("system_logs.txt", "w") as file:
        
        # 1. Generate 5 random normal events
        print("[STATUS] Generating Benign Traffic...")
        for _ in range(5):
            domain, event = random.choice(normal_events)
            file.write(f"{domain},{event}\n")
            print(f"Logged: [{domain}] -> {event}")
            time.sleep(0.5) # Pauses for half a second to look real

        # 2. Inject the WannaCry Attack
        print("\n[WARNING] INJECTING WANNACRY MALWARE TRACE...")
        for domain, event in attack_sequence:
            file.write(f"{domain},{event}\n")
            print(f"Logged: [{domain}] -> {event}")
            time.sleep(1)

    print("\n--- SIMULATION COMPLETE. 'system_logs.txt' SAVED. ---")

if __name__ == "__main__":
    generate_logs()