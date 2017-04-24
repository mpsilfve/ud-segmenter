from random import randint

def get_init_split(s):
    return [0,len(s)]

def divide(split):
    assert(len(split) > 1)
    r = randint(1,len(split) - 1)
    if split[r - 1] < split[r] - 1:
        # Copy because insert modifies object.
        split = list(split)
        rr = randint(split[r-1] + 1, split[r] - 1)
        split.insert(r,rr)
    return split

def join(split):
    assert(len(split) > 2)
    r = randint(1, len(split) - 2)
    # Copy because pop modifies object.
    split = list(split)
    split.pop(r)
    return split

def move(split):
    assert(len(split) > 2)
    r = randint(1, len(split) - 2)
    d = randint(0,1)
    if d:
        if split[r - 1] < split[r] - 1:
            # Copy because we modify object.
            split = list(split)            
            split[r] -= 1
    else:
        if split[r] < split[r+1] - 1:
            # Copy because we modify object.
            split = list(split)            
            split[r] += 1
    return split

def sample_next(split,max_splits):
    r = randint(0,2)

    if r == 0 and len(split) - 1 < max_splits:
        split = divide(split)
    elif r == 1:
        if (len(split) > 2):
            split = join(split)
    else:
        if (len(split) > 2):
            split = move(split)
    return split

def sample_nth(n,split,max_splits):
    for i in range(n):
        split = sample_next(split,max_splits)
    return split

def get_str(i,split,wf):
#    assert(i < len(split) - 1)
    if i >= len(split) - 1:
        return ""
    return wf[split[i]:split[i+1]]
