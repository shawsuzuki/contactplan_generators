import random
from itertools import combinations

def generate_contacts(total_time, data_rate_ranges, max_time_diff, total_contacts):
    contacts = []
    max_node = max(max(pair) for pair in data_rate_ranges.keys())
    
    while len(contacts) < total_contacts:
        from_node = random.randint(1, max_node)
        to_node = random.randint(1, max_node)
        
        if (from_node, to_node) not in data_rate_ranges and (to_node, from_node) not in data_rate_ranges:
            continue
        
        start_time = random.randint(0, total_time)
        end_time = random.randint(start_time, min(start_time + max_time_diff, total_time))
        
        rate_range, _ = data_rate_ranges.get((from_node, to_node), data_rate_ranges.get((to_node, from_node)))
        min_rate, max_rate = rate_range
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

def generate_scenario(num_bundles, max_bundle_number, max_start_time, destination_eids, max_size):
    bundles_number = [random.randint(1, max_bundle_number) for _ in range(num_bundles)]
    start_times = sorted([random.randint(0, max_start_time) for _ in range(num_bundles)])
    destinations = [random.choice(destination_eids) for _ in range(num_bundles)]
    sizes = [random.randint(1, max_size) for _ in range(num_bundles)]
    
    return bundles_number, start_times, destinations, sizes

# パラメータ
total_time = 1000  # 全体の時間（秒）
max_time_diff = 100 # startTimeとendTimeの差の最大値
total_contacts = 200  # 生成するコンタクトの総数

data_rate_ranges = {
    (1, 2): ((500, 1000), 10),
    (2, 3): ((500, 1000), 10),
    (1, 3): ((500, 1000), 10),
    (2, 4): ((1000, 2000), 20),
    (2, 5): ((1000, 2000), 20),
    (3, 4): ((1000, 2000), 20),
    (3, 5): ((1000, 2000), 20),
    (4, 5): ((500, 1000), 10),
    (4, 6): ((500, 1000), 10),
    (5, 6): ((500, 1000), 10),
}

# シナリオパラメータ
num_bundles = 100
max_bundle_number = 30
destination_eids = [6]
max_size = 40

max_start_time = total_time

# コンタクトデータの生成
contacts = generate_contacts(total_time, data_rate_ranges, max_time_diff, total_contacts)

# コンタクトファイルの出力
contact_file = "contacts.txt"
with open(contact_file, "w") as f:
    f.write(f"m horizon +0\n")
    
    # Contact行の出力
    for contact in contacts:
        f.write(f"a contact +{contact['startTime']} +{contact['endTime']} {contact['fromNode']} {contact['toNode']} {contact['dataRate']}\n")
    
    # Range行の出力
    nodes = set()
    for pair in data_rate_ranges.keys():
        nodes.update(pair)
    
    for nodeA, nodeB in combinations(sorted(nodes), 2):
        if (nodeA, nodeB) in data_rate_ranges:
            _, distance = data_rate_ranges[(nodeA, nodeB)]
        elif (nodeB, nodeA) in data_rate_ranges:
            _, distance = data_rate_ranges[(nodeB, nodeA)]
        else:
            continue
        f.write(f"a range +0 +{total_time} {nodeA} {nodeB} {distance}\n")

print(f"Total contacts generated: {len(contacts)}")
print(f"Contact file saved as: {contact_file}")

# シナリオデータの生成
bundles_number, start_times, destinations, sizes = generate_scenario(num_bundles, max_bundle_number, max_start_time, destination_eids, max_size)

# シナリオファイルの出力
scenario_file = "scenario.txt"
with open(scenario_file, "w") as f:
    f.write(f"dtnsim.node[1].app.bundlesNumber=\"{','.join(map(str, bundles_number))}\"\n")
    f.write(f"dtnsim.node[1].app.start=\"{','.join(map(str, start_times))}\"\n")
    f.write(f"dtnsim.node[1].app.destinationEid=\"{','.join(map(str, destinations))}\"\n")
    f.write(f"dtnsim.node[1].app.size=\"{','.join(map(str, sizes))}\"\n")

print(f"Scenario file saved as: {scenario_file}")

