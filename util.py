def clamp(val, small, large):
    if(val < small):
        return small
    else:
        return min(val, large)
