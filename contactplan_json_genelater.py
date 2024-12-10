import json
import random

def generate_contacts(num_nodes, total_time, max_data_rate, max_time_diff):
    contacts = []
    for _ in range(num_nodes * 2):  # ノードの数の2倍のコネクションを生成
        from_node = random.randint(1, num_nodes)
        to_node = random.randint(1, num_nodes)
        while to_node == from_node:  # fromNodeとtoNodeが異なるようにする
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

    return {"contacts": contacts}

# パラメータ
num_nodes = 3  # ノードの数
total_time = 30  # 全体の時間（秒）
max_data_rate = 100  # 最大データレート
max_time_diff = 10  # startTimeとendTimeの差の最大値

# JSONデータの生成
contacts_data = generate_contacts(num_nodes, total_time, max_data_rate, max_time_diff)

# JSONファイルの出力
output_file = "contacts.json"
with open(output_file, "w") as f:
    json.dump(contacts_data, f, indent=2)

# 生成されたJSONデータの表示
print(json.dumps(contacts_data, indent=2))
