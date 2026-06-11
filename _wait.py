import time, sys
print("Waiting 90 seconds for Docker build...", flush=True)
for i in range(90, 0, -10):
    time.sleep(10)
    print(f"  {i}s remaining...", flush=True)
print("Done waiting.", flush=True)
