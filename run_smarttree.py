
import os
import requests
import threading
import time

import matplotlib.pyplot as plt
import matplotlib.patches as patches

from src import utils, parser
from src.smarttree import Tree, Instance


### Constants

# Data
data_path = 'data/Geolife Trajectories 1.3/Data'
maps_path = 'data/Maps/'
ranges = [(-180, 180), (-90, 90)]
num_users = 1000
num_samples_per_user = 100000
num_samples_total = 1000000

# Tree
min_range = 0.1                        # do not split when a dimension becomes smaler then x
split_k = 10                           # split when a node has x instances
neighbor_radius = 0.01                 # max distance for an instance to be a neighbor; in euclidean space

# Plotting
zoom = 50                              # percentage of zoom on the point of interest
refresh_rate = 3                       # time in seconds to wait between updates

### Functions

def get_events():
    total_count = 0
    user_counts = {}

    for file in utils.plt_files(data_path):
        user_id = utils.get_user(file)
        
        if user_counts.get(user_id, 0) >= num_samples_per_user:
            continue

        for lat, lon, _, d, t in parser.read_file(file):
            event = parser.parse(user_id, lat, lon, d, t)
            if not event or not (ranges[0][0] < event.location.lon < ranges[0][1] and \
                                 ranges[1][0] < event.location.lat < ranges[1][1]):
                continue

            yield event

            total_count += 1
            user_counts[event.user_id] = user_counts.get(event.user_id, 0) + 1

            if total_count % 10000 == 0:
                print(f'#events={total_count}, #users={len(user_counts)}, #nodes={tree.size}')

            if total_count >= num_samples_total:
                break
            if len(user_counts) >= num_users:
                break
        else:
            continue

        print(f'#events={total_count}, #users={len(user_counts)}, #nodes={tree.size}')
        break


def build_tree(tree):
    for event in get_events():
        tree.add(Instance(event.user_id, [event.location.lon, event.location.lat, event.timestamp]))
    print(f'Done building tree!')


def download_map(bbox):
    if not os.path.exists(maps_path):
        os.makedirs(maps_path)

    path = os.path.join(maps_path, f"{'-'.join(str(x) for x in bbox)}.png")
    if os.path.isfile(path):
        return path

    session = requests.session()
    session.get('https://www.openstreetmap.org/') # Load session cookies
    url = f'https://render.openstreetmap.org/cgi-bin/export?bbox={bbox[0]},{bbox[2]},{bbox[1]},{bbox[3]}&scale=125000&format=png'
    read = session.get(url, stream=True)
    with open(path, 'wb') as w:
        for chunk in read.iter_content(chunk_size=1024):
            if chunk:
                w.write(chunk)

    return path


def draw(instances):
    plt.clf()
    
    diff = neighbor_radius / (zoom / 100)
    lon, lat = event_of_interest.location.lon, event_of_interest.location.lat
    bbox = [lon - diff, lon + diff, lat - diff, lat + diff]

    path = download_map(bbox)
    plot = plt.imread(path)
    ax = plt.subplot()

    ax.set_title('Meetings')
    ax.set_xlim(bbox[0], bbox[1])
    ax.set_ylim(bbox[2], bbox[3])
    ax.imshow(plot, extent=bbox, aspect= 'equal')
    ax.add_patch(patches.Circle((lon, lat), neighbor_radius, linewidth=1, edgecolor='red', facecolor='none'))
    ax.scatter([i.value[0] for i in instances], [i.value[1] for i in instances], s=1, c=[i.id for i in instances])

    plt.draw()
    plt.pause(refresh_rate)


plt.show()

# Start building the tree
tree = Tree(ranges, min_range, split_k)
threading.Thread(target=build_tree, args=(tree,)).start()

# Keep checking the tree for meetings
event_of_interest = next(get_events())
instance = Instance(-1, [event_of_interest.location.lon, event_of_interest.location.lat])
meeting_count = 0

while True:
    meetings = tree.getNeigbors(instance, neighbor_radius, neighbor_radius, [0, 1])
    if len(meetings) != meeting_count:
        print(f'Found {len(meetings)} meetings!')
        draw(meetings)
        meeting_count = len(meetings)
    else:
        time.sleep(refresh_rate)
