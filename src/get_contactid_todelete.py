import random

def permutation_of_contact(contact_plan, permutations=None, deleteSpecificNumberofContacts=None, celestialA_nodes=None, celestialB_nodes=None):
    contact_ids_to_delete = set()
    contact_ids_from_celestialA = set()
    contact_ids_from_celestialB = set()
    deleted_contacts = []

    if deleteSpecificNumberofContacts is not None:
        all_contact_ids = [(idx // 2) +1 for idx, line in enumerate(contact_plan) if line.startswith("a contact")]
        
        if len(all_contact_ids) < deleteSpecificNumberofContacts:
            raise ValueError(f"削除するコンタクトが足りません。要求: {deleteSpecificNumberofContacts}, 利用可能: {len(all_contact_ids)}")
        
        contact_ids_to_delete = set(random.sample(all_contact_ids, deleteSpecificNumberofContacts))
        
        for contact_id in contact_ids_to_delete:
            parts = contact_plan[contact_id*2-1].split()
            src = int(parts[4])
            dst = int(parts[5])
            start_time = parts[2]
            end_time = parts[3]
        
            deleted_contacts.append({
                'id': contact_id,
                'source': src,
                'destination': dst,
                'start': start_time,
                'end': end_time
            })

            if src in celestialA_nodes:
                contact_ids_from_celestialA.add(contact_id)
            elif src in celestialB_nodes:
                contact_ids_from_celestialB.add(contact_id)

    elif permutations is not None:
        for source, destination, delete_count in permutations:
            matching_contacts = []
            for idx, line in enumerate(contact_plan):
                if line.startswith("a contact"):
                    parts = line.split()
                    src = int(parts[4])
                    dst = int(parts[5])
                    if src == source and dst == destination:
                        contact_id = idx // 2 + 1
                        matching_contacts.append(contact_id)

            if len(matching_contacts) < delete_count:
                raise ValueError(f"ソース {source} と宛先 {destination} のコンタクトが足りません。要求: {delete_count}, 利用可能: {len(matching_contacts)}")

            selected_contacts = matching_contacts[:delete_count]
            contact_ids_to_delete.update(selected_contacts)

            for contact_id in selected_contacts:
                parts = contact_plan[contact_id * 2].split()
                start_time = parts[2]
                end_time = parts[3]
                deleted_contacts.append({
                    'id': contact_id,
                    'source': source,
                    'destination': destination,
                    'start': start_time,
                    'end': end_time
                })

            if celestialA_nodes and source in celestialA_nodes:
                contact_ids_from_celestialA.update(selected_contacts)
            elif celestialB_nodes and destination in celestialB_nodes:
                contact_ids_from_celestialB.update(selected_contacts)

    else:
        raise ValueError("deleteSpecificNumberofContactsまたはpermutationsのいずれかを指定する必要があります。")

    result = {
        "dtnsim.central.contactIdsToDelete": " ".join(map(str, sorted(contact_ids_to_delete))),
        "dtnsim.central.contactIdsToDelete_from_celestialA": " ".join(map(str, sorted(contact_ids_from_celestialA))),
        "dtnsim.central.contactIdsToDelete_from_celestialB": " ".join(map(str, sorted(contact_ids_from_celestialB)))
    }

    return result, deleted_contacts

# コンタクトプランの読み込み
with open("results/contacts.txt", "r") as file:
    contact_plan = file.readlines()

# パラメータの設定
permutations = [(1, 2, 10), (4, 5, 5)]
celestialA_nodes = [1, 2, 3]
celestialB_nodes = [4, 5, 6]
deleteSpecificNumberofContacts = 500 # または整数値を指定

try:
    result, deleted_contacts = permutation_of_contact(contact_plan, permutations, deleteSpecificNumberofContacts, celestialA_nodes, celestialB_nodes)
    
    # 結果をファイルに書き込み
    with open("results/idOfContactToDelete.txt", "w") as file:
        for key, value in result.items():
            file.write(f"{key}=\"{value}\"\n")
    
    print("結果がresults/idOfContactToDelete.txtに書き込まれました")

    # 削除されたコンタクトを出力
    print("\n削除されたコンタクト:")
    for contact in deleted_contacts:
        print(f"ID: {contact['id']}, 送信元: {contact['source']}, 宛先: {contact['destination']}, 開始: {contact['start']}, 終了: {contact['end']}")

except ValueError as e:
    print(f"エラー: {e}")

