def backtracker(iterable, flat):
    for item in iterable:
        if isinstance(item, list):
            backtracker(item, flat)
            continue
        if item is not None: 
            flat.append(item)

def flatten(iterable):
    flat = []
    backtracker(iterable, flat)
    
    return flat
