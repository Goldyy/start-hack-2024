import requests
import json
import socket
import os
import matplotlib.pyplot as plt
from colorhash import ColorHash

def get_API_Key_and_auth():
    # Gets public key from spaces and places in correct format
    print("-- No API Key Found --")

    # Gets user to paste in generated token from app
    token = input('Enter provided API key here: ')

    # Writes activation key to file. This key can be used to open up Firehose connection
    f = open("API_KEY.txt", "a")
    f.write(token)
    f.close()
    return token


# work around to get IP address on hosts with non resolvable hostnames
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IP_ADRRESS = s.getsockname()[0]
s.close()
url = 'http://' + str(IP_ADRRESS) + '/update/'

# Tests to see if we already have an API Key
try:
    if os.stat("API_KEY.txt").st_size > 0:
        # If we do, lets use it
        f = open("API_KEY.txt")
        apiKey = f.read()
        f.close()
    else:
        # If not, lets get user to create one
        apiKey = get_API_Key_and_auth()
except:
    apiKey = get_API_Key_and_auth()

# overwrite previous log file
f = open("logs.json", 'r+')
f.truncate(0)

# Opens a new HTTP session that we can use to terminate firehose onto
s = requests.Session()
s.headers = {'X-API-Key': apiKey}
try:
  r = s.get(
      'https://partners.dnaspaces.io/api/partners/v1/firehose/events', stream=True)  # Change this to .io if needed

  # Jumps through every new event we have through firehose
  print("Starting Stream")
  track_device_id = None
  track_device_id = "device-dEE6LZOrnQ8N3xnl3Uv3"
  xarr = {}
  yarr = {}
  carr = {}
  c = 0
  for idx, line in enumerate(r.iter_lines()):
      if line:

          # decodes payload into useable format
          decoded_line = line.decode('utf-8')
          event = json.loads(decoded_line)

          if event["partnerTenantId"] == "Simulation-Retail":
            # writes every event to the logs.json in readible format
            #f.write(str(json.dumps(json.loads(line), indent=4, sort_keys=True)))

            # gets the event type out the JSON event and prints to screen
            eventType = event['eventType']
            #print(eventType)

            if eventType == "DEVICE_LOCATION_UPDATE":
              # Init device track if not seen
              """
              if not track_device_id:
                  try:
                    track_device_id = event["deviceLocationUpdate"]["device"]["deviceId"]
                  except:
                    pass
              """
              #if track_device_id != event["deviceLocationUpdate"]["device"]["deviceId"]:
              #  continue
              try:
                track_device_id = event["deviceLocationUpdate"]["device"]["deviceId"]
                c_hash = ColorHash(track_device_id)
              except:
                continue

              if track_device_id not in xarr:
                xarr[track_device_id] = []
                yarr[track_device_id] = []
                carr[track_device_id] = []

              xpos = event["deviceLocationUpdate"]["xPos"]
              ypos = event["deviceLocationUpdate"]["yPos"]
              xarr[track_device_id] += [xpos]
              yarr[track_device_id] += [ypos]
              carr[track_device_id] += [str(c_hash.hex) + "90"] # add alpha
              #f.write(str(json.dumps(json.loads(line), indent=4, sort_keys=True)))
              #f.write(str(json.dumps(json.loads(line), indent=4, sort_keys=True)))
              
              print(f"{c} - x: {xpos}, y: {ypos}")
              c += 1
              if c > 200000:
                break
except KeyboardInterrupt:
  pass    
        
# plot
plt.rcParams['lines.markersize'] = plt.rcParams['lines.markersize'] / 5
#plt.rcParams['figure.max_open_warning'] = False
ids_sorted = sorted(yarr, key=lambda k: len(yarr[k]))
print(f"len longest: {len(yarr[ids_sorted[-1]])}")
print(f"len shortest: {len(yarr[ids_sorted[0]])}")
for id in ids_sorted[-10:]:
   
  fig, ax = plt.subplots()
  ax = plt.gca()
  ax.set_xlim([0, 900])
  ax.set_ylim([0, 1300])

  ax.scatter(xarr[id], yarr[id], c=carr[id])

  plt.savefig(f"{id}.png", dpi=500)
  plt.clf()
  