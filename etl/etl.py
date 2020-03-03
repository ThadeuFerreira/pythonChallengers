def transform(legacy_data):
    data = {}
    for x in legacy_data:
        for index in legacy_data[x]:
            data[index.lower()] = x
    return data