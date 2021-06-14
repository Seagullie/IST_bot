#import extract_pair_data as extract
from .extract_pair_data import get_current_pair, extract_pair_parity
from .check_if_week_is_even import check_if_week_is_even

def report_pair_data():
    pair_data = get_current_pair()
    if type(pair_data) != dict:
        return pair_data
    corrected_pair_data = filter_by_parity(pair_data)
    return corrected_pair_data

def filter_by_parity(pair_data):
    parity = extract_pair_parity(pair_data)
    #breakpoint()
    if not parity:
        return pair_data
    
    if parity == "denominator" and check_if_week_is_even() == "even":
        return pair_data
    elif parity == "nominator" and check_if_week_is_even() == "odd":
        return pair_data
    return False

def report_pair_room():
    final_pair_data = report_pair_data()
    if type(final_pair_data) == dict:
        return final_pair_data["room"]
    return final_pair_data
    
    
    

