import random
from itertools import combinations

# Parameters
params = {
    "total_time": 10000,     # Simulation time (seconds)
    "total_contacts": 1000,  # Total number of contacts
    "link_params": {
        ## (nodeA, nodeB):
        ## (data rate base (Mbps), data rate variation%, 
        ## distance (light seconds), distance variation%,
        ## avg contact duration (seconds), duration variation%)
        (1, 2): (100, 10, 0.12, 0, 15, 20), 
        (2, 3): (100, 10, 0.12, 0, 15, 20),
        (1, 3): (100, 10, 0.12, 0, 15, 20),
        (2, 4): (1000, 10, 1.2, 15, 20, 25),
        (2, 5): (1000, 10, 1.2, 15, 20, 25),
        (3, 4): (1000, 10, 1.2, 15, 20, 25),
        (3, 5): (1000, 10, 1.2, 15, 20, 25),
        (4, 5): (100, 10, 0.13, 0, 15, 20),
        (4, 6): (100, 10, 0.13, 0, 15, 20),
        (5, 6): (100, 10, 0.13, 0, 15, 20),
    },
}

def count_contacts(contacts, link_params):
    contact_counts = {pair: 0 for pair in link_params.keys()}
    for contact in contacts:
        from_node, to_node = contact['fromNode'], contact['toNode']
        if (from_node, to_node) in contact_counts:
            contact_counts[(from_node, to_node)] += 1
        elif (to_node, from_node) in contact_counts:
            contact_counts[(to_node, from_node)] += 1
    return contact_counts

def generate_contacts(total_time, link_params, total_contacts):
    contacts = []
    max_node = max(max(pair) for pair in link_params.keys())
    
    while len(contacts) < total_contacts:
        from_node = random.randint(1, max_node)
        to_node = random.randint(1, max_node)
        
        if (from_node, to_node) not in link_params and (to_node, from_node) not in link_params:
            continue
        
        start_time = random.randint(0, total_time)
        
        base_rate, rate_variation, _, _, avg_duration, duration_variation = link_params.get((from_node, to_node), link_params.get((to_node, from_node)))
        
        duration = random.uniform(avg_duration * (1 - duration_variation/100), avg_duration * (1 + duration_variation/100))
        end_time = min(start_time + int(duration), total_time)
        modified_base_rate = base_rate * 1000000 

        min_rate = int(modified_base_rate * (1 - rate_variation / 100))
        max_rate = int(modified_base_rate * (1 + rate_variation / 100))
        data_rate = random.randint(min_rate, max_rate)
        
        contacts.append({
            "fromNode": from_node,
            "toNode": to_node,
            "startTime": start_time,
            "endTime": end_time,
            "dataRate": data_rate
        })
    
    contacts.sort(key=lambda x: x['startTime'])
    return contacts

def generate_ranges(contacts, link_params):
    ranges = []
    for contact in contacts:
        from_node = contact['fromNode']
        to_node = contact['toNode']
        start_time = contact['startTime']
        end_time = contact['endTime']

        if (from_node, to_node) in link_params:
            _, _, base_distance, distance_variation, _, _ = link_params[(from_node, to_node)]
        elif (to_node, from_node) in link_params:
            _, _, base_distance, distance_variation, _, _ = link_params[(to_node, from_node)]
        else:
            continue

        variation = base_distance * distance_variation / 100
        random_distance = random.uniform(base_distance - variation, base_distance + variation)

        ranges.append({
            "fromNode": from_node,
            "toNode": to_node,
            "startTime": start_time,
            "endTime": end_time,
            "distance": round(random_distance, 2)
        })

    return ranges

# Generate contact data
contacts = generate_contacts(params['total_time'], params['link_params'], params['total_contacts'])

# Generate range data
ranges = generate_ranges(contacts, params['link_params'])

# Count contacts for each node pair
contact_counts = count_contacts(contacts, params['link_params'])

# Output contact file
contact_file = "results/contacts.txt"
with open(contact_file, "w") as f:
    f.write(f"m horizon +0\n")
    
    # Output Contact and Range lines
    for contact, range_item in zip(contacts, ranges):
        f.write(f"a contact +{contact['startTime']} +{contact['endTime']} {contact['fromNode']} {contact['toNode']} {contact['dataRate']}\n")
        f.write(f"a range +{range_item['startTime']} +{range_item['endTime']} {range_item['fromNode']} {range_item['toNode']} {range_item['distance']}\n")

print(f"Total contacts and ranges generated: {len(contacts)}")
print(f"Contact file saved as: {contact_file}")

# Display contact counts for each node pair
print("\nContact counts for each node pair:")
for pair, count in contact_counts.items():
    print(f"Nodes {pair[0]} and {pair[1]}: {count} contacts")
