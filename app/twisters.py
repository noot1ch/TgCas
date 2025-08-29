def get_roller_multiplier(num):
    if num == 1: #bar
        return 1.3
    elif num == 43: #лимоны
        return 1.5
    elif num == 22: #виноград
        return 1.8
    elif num == 64: #7
        return 2
    else:
        return False
    
def get_dice_multiplier(num):
    if num < 4:
        return None
    elif num == 4:
        return 1.4
    elif num == 5:
        return 1.7
    elif num == 6:
        return 2