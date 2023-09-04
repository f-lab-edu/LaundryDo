from src.domain.clothes import LaundryLabel
from datetime import timedelta

LAUNDRYBAG_MAXVOLUME = MACHINE_MAXVOLUME = 25
LAUNDRY_MINVOLUME = 24
LAUNDRYBAG_MAX_WAITINGTIME = timedelta(minutes = 30)

LaundryTimeTable = {LaundryLabel.WASH: 60, LaundryLabel.DRY: 80, LaundryLabel.HAND: 100}


def time_required_for_volume(time, volume):
    if 0 < volume <= 10:
        time *= 1
    elif 10 < volume < 20:
        time *= 1.5
    elif 20 <= volume < 25:
        time *= 2
    else:
        raise ValueError(f"{volume} is not valid unit.")
    return int(time)