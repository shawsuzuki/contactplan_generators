import random

# パラメータ設定
max_contacts = 500
num_nodes = 10
contact_time_range = (0, 60)
max_time = 10000
bandwidth_range = (50, 100)

def generate_contact_plan(num_nodes, contact_time_range, max_time, bandwidth_range, max_contacts):
    contacts = []
    # コンタクト生成
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
    
    # 開始時間順にソート
    contacts_sorted = sorted(contacts)

    # range行を追加
    ranges = []
    for i in range(1, num_nodes):
        for j in range(i + 1, num_nodes + 1):
            ranges.append(f"a range +0 +{max_time} {i} {j} 0")

    return contacts_sorted, ranges

# コンタクトプラン生成
contact_plan, range_plan = generate_contact_plan(num_nodes, contact_time_range, max_time, bandwidth_range, max_contacts)

# 結果の出力（コンタクト）
for _, contact in contact_plan:
    print(contact)

# 結果の出力（range行）
for range_line in range_plan:
    print(range_line)
