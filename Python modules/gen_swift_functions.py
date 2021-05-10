'''
History
=======
2017-12-11      CHNG0005220511  Manan Gosh	DIS go-live
'''

import acm, re

def get_block(message, block_nr):
    '''
    returns the whole of the first found block nr specified
    '''
    block_pattern = '\{%d:(.*)\}' % block_nr
    block_m = re.search(block_pattern, message, re.DOTALL)
    return block_m.group(1)

def get_msg_function(message):
    '''
    Returns the function F01, or F21 of the message in block 1
    '''
    block_1 = get_block(message, 1)
    return block_1[:3]

def get_msg_type(message):
    '''
    Returns message type and subtype e.g. 598-155 or 598-154
    '''
    type_pattern = '\{2:[OI](\d{3}).*\}'
    sub_type_pattern = '{4:.*:12:(\d{3}).*}'
    type_m = re.search(type_pattern, message, re.DOTALL)
    sub_type_m = re.search(sub_type_pattern, message, re.DOTALL)
    if not sub_type_m is None:
        return '%s-%s' % (type_m.group(1), sub_type_m.group(1))
    else:
        return '%s' % type_m.group(1)
        

def get_trans_ref(message):
    isin_mgmt_trans_ref_pattern = '.*:20:([0-9]{0,15})-?([0-9]{0,15})[:\r\n]'
    trans_ref_m = re.search(isin_mgmt_trans_ref_pattern, message)
    if not trans_ref_m is None:
        return trans_ref_m.group(1), trans_ref_m.group(2)
    else:
        gen_trans_ref_pattern = '.*:20:(.*)[:\n(-\})]'
        trans_ref_m = re.search(gen_trans_ref_pattern, message)
        if not trans_ref_m is None:
            return trans_ref_m.group(1), None
        else:
            return None, None

def get_trans_ref_from_tag(tag, message):
    '''
        below modified 2020-08-12 - production fix 
        fix for field 20c being longer than 16 characters
    '''
    isin_mgmt_trans_ref_pattern = '.*%sISM-([0-9]{0,15})[:\r\n]' % tag
    trans_ref_m = re.search(isin_mgmt_trans_ref_pattern, message)
    if not trans_ref_m is None:
        bp = acm.FBusinessProcess[trans_ref_m.group(1)]
        return bp.Subject().Oid(), bp.Steps().Last().Oid()
    else:
        gen_trans_ref_pattern = '.*%s(.*)[:\n]' % tag
        trans_ref_m = re.search(gen_trans_ref_pattern, message)
        if not trans_ref_m is None:
            return trans_ref_m.group(1), None
        else:
            return None, None
            
def get_value_from_tag(tag, message):
    '''
    Returns 0-15 digits
    '''
    pattern = '.*%s([,0-9]{0,15})[:\r\n]' % tag
    m = re.search(pattern, message)
    if not m is None:
        return m.group(1)
    else:
        return None
        
def get_text_from_tag(tag, message):
    '''
    Returns 1-inf characters
    '''
    pattern = '.*%s(.+)[:\r\n]' % tag
    m = re.search(pattern, message)
    if not m is None:
        return m.group(1).strip()
    else:
        return None
        
def get_multiline_text_from_tag(tag, message):
    '''
    Returns chars across lines
    '''
    pattern = '.*%s([^:]+):' % tag
    m = re.search(pattern, message, re.DOTALL)
    if not m is None:
        return m.group(1)
    else:
        return None

def get_isin(message):
    trans_ref_pattern = '.*:35B:ISIN (.{12}).*[:\n]'
    trans_ref_m = re.search(trans_ref_pattern, message)
    return trans_ref_m and trans_ref_m.group(1) or ''

def get_external_id(message):
    trans_ref_pattern = '.*:35B:ISIN .{12} (.{9})[:\n]'
    trans_ref_m = re.search(trans_ref_pattern, message)
    if trans_ref_m is None:
        trans_ref_pattern = '.*:35B:ISIN (.{12}).*[\n](.*)[:\n]' 
    else:
        return  trans_ref_m.group(2)  

    trans_ref_m = re.search(trans_ref_pattern, message)
    if not trans_ref_m is None:
        return trans_ref_m.group(2)
    else:
        return None
