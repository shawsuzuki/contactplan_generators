import json
import random

def generate_contacts(num_nodes, total_time, max_data_rate, max_time_diff, excluded_pairs, total_contacts):
    contacts = []
    while len(contacts) < total_contacts:
        from_node = random.randint(1, num_nodes)
        to_node = random.randint(1, num_nodes)
        while to_node == from_node or (from_node, to_node) in excluded_pairs or (to_node, from_node) in excluded_pairs:
            to_node = random.randint(1, num_nodes)

        start_time = random.randint(0, total_time)
        end_time = random.randint(start_time, min(start_time + max_time_diff, total_time))

        data_rate = random.randint(1, max_data_rate)

        contacts.append({
            "fromNode": from_node,
            "toNode": to_node,
            "startTime": start_time,
            "endTime": end_time,
            "dataRate": data_rate
        })

    # 開始時間でソート
    contacts.sort(key=lambda x: x['startTime'])
    return contacts

# パラメータ
num_nodes = 6 # ノードの数
total_time = 1000  # 全体の時間（秒）
max_data_rate = 100  # 最大データレート
max_time_diff = 30 # startTimeとendTimeの差の最大値
excluded_pairs = [(1, 4), (1, 5), (1, 6), (2, 6), (3, 6)]  # コンタクトを作成しないノードのペア
total_contacts = 100  # 生成するコンタクトの総数

# コンタクトデータの生成
contacts = generate_contacts(num_nodes, total_time, max_data_rate, max_time_diff, excluded_pairs, total_contacts)

# JSONファイルの出力
json_output_file = "contacts.json"
with open(json_output_file, "w") as f:
    json.dump({"contacts": contacts}, f, indent=2)

# txtファイルの出力
txt_output_file = "contacts.txt"
with open(txt_output_file, "w") as f:
    for contact in contacts:
        f.write(f"a contact +{contact['startTime']} +{contact['endTime']} {contact['fromNode']} {contact['toNode']} {contact['dataRate']}\n")

# 生成されたデータの表示
print(json.dumps({"contacts": contacts}, indent=2))
print(f"Total contacts generated: {len(contacts)}")
print(f"JSON file saved as: {json_output_file}")
print(f"TXT file saved as: {txt_output_file}")

