'''
A collection of utility methods
'''


def clamp(val, small, large):
    '''
    Clamp a value to a min and max
    '''
    if(val < small):
        return small
    return min(val, large)
