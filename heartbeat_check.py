import datetime
import sys

max_heartbeat_reboot_interval = 2 # min

with open('heartbeat.txt', 'r') as f:
    last_heartbeat = datetime.datetime.fromisoformat(f.read().replace('\n', ''))

print((datetime.datetime.now() - last_heartbeat).total_seconds() < max_heartbeat_reboot_interval * 60)

if (datetime.datetime.now() - last_heartbeat).total_seconds() < max_heartbeat_reboot_interval * 60:
    sys.exit(0)
else:
    sys.exit(-1)