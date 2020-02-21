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


def format_time(input_tuple):
    '''
    Format an input_tuple of (hr: int, min: int) to a string of hh:mm
    '''
    hour, minute = str(input_tuple[0]), str(input_tuple[1])
    if(len(hour) == 1):
        hour = '0' + str(input_tuple[0])
    if(len(minute) == 1):
        minute = '0' + str(input_tuple[1])
    return hour + ':' + minute
