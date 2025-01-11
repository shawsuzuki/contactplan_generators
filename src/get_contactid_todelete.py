def permutation_of_contact(contact_plan, permutations):
    contact_ids_to_delete = []

    for source, destination, delete_count in permutations:
        matching_contacts = []
        for idx, line in enumerate(contact_plan):
            if line.startswith("a contact"):
                parts = line.split()
                src = int(parts[4])
                dst = int(parts[5])
                if src == source and dst == destination:
                    matching_contacts.append(idx + 1)  # Line numbers are 1-based

        if len(matching_contacts) < delete_count:
            raise ValueError(f"Not enough contacts for source {source} and destination {destination}. Required: {delete_count}, Found: {len(matching_contacts)}")

        contact_ids_to_delete.extend(matching_contacts[:delete_count])

    contact_ids_to_delete.sort()
    return "dtnsim.central.contactIdsToDelete=\"" + " ".join(map(str, contact_ids_to_delete)) + "\""

# Read the contact plan from file
with open("results/contacts.txt", "r") as file:
    contact_plan = file.readlines()

# Define the permutations
permutations = [(1, 2, 10), (4, 5, 5)]

try:
    result = permutation_of_contact(contact_plan, permutations)
    
    # Write the result to file
    with open("results/idOfContactToDelete.txt", "w") as file:
        file.write(result)
    
    print("Result written to reults/idOfContactToDelete.txt")
except ValueError as e:
    print(f"Error: {e}")

