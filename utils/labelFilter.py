def labelFilter(labels):
    exclude_list = ["Canine", "Mammal", "Puppy", "Kitten", "Rodent"]

    for label in labels:
        if len(labels) <= 4:
            break

        if label['Name'] in exclude_list:
            labels.remove(label)
        
    labels = labels[:4]

    return labels
