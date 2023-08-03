'''
# test reference : https://github.com/agronholm/apscheduler/blob/master/tests/test_schedulers.py
apscheduler jobs
1. put laundrybag(state == READY) into machine(state == READY)
2. reclaim clothes from machine(state == DONE)
3. check if order(state == RECLAIMING) is fully reclaimed(clothes == RECLAIMED in clothes_list), and change Orderstate = SHIP_READY
4. ship order(state == SHIP_READY) == SHIP
'''

##################################################################
# 1. put laundrybag(state == READY) into machine(state == READY) #
##################################################################
def test_NO_laundrybag_is_ready_for_laundry() :
    pass

def test_laundrybag_ready_for_laundry_put_in_machine() :
    ''' 
    check
    1. laundrybag state 
    2. machine state
    3. order state
    4. clothes state
    '''
    pass

##################################################
# 2. reclaim clothes from machine(state == DONE) #
##################################################
def test_NO_machine_is_finished() :
    pass

def test_machine_finished_time_match_the_expect_time() :
    pass

def test_clothes_state_changes_as_machine_finished_laundry() :
    pass

def test_laundrybag_state_changes_as_machine_finished_laundry() :
    pass

def test_order_state_changes_as_machine_finished_laundry() :
    pass

###################################################################################################
# 3. check if order(state == RECLAIMING) is fully reclaimed(clothes == RECLAIMED in clothes_list) #
###################################################################################################
def test_NO_order_is_fully_reclaimed() :
    pass

def test_clothes_state_changes_as_order_is_fully_reclaimed() :
    pass

def test_order_state_changes_as_order_is_fully_reclaimed() :
    pass

##############################################
# 4. ship order(state == SHIP_READY) == SHIP #
##############################################
def test_NO_order_is_ready_to_be_shipped() :
    pass

def test_order_state_changes_as_ready_to_be_shipped() :
    pass

