import random

# set parameters here
max_contacts = 300
num_nodes = 4
contact_time_range = (0, 60)
max_time = 10000
bandwidth_range = (50,100)

def generate_contact_plan(num_nodes, contact_time_range, max_time, bandwidth_range, max_contacts):
    contacts = []
    for _ in range(max_contacts):
        node1 = random.randint(1, num_nodes)
        node2 = random.randint(1, num_nodes)
        while node1 == node2:
            node2 = random.randint(1, num_nodes)
        start_time = random.randint(0, max_time - contact_time_range[1])
        duration = random.randint(contact_time_range[0], contact_time_range[1])
        end_time = start_time + duration
        bandwidth = random.randint(bandwidth_range[0], bandwidth_range[1])
        if end_time <= max_time:
            contacts.append((start_time, f"a contact +{start_time} +{end_time} {node1} {node2} {bandwidth}"))
    return sorted(contacts)

contact_plan = generate_contact_plan(num_nodes, contact_time_range, max_time, bandwidth_range, max_contacts)

for _, contact in contact_plan:
    print(contact)
