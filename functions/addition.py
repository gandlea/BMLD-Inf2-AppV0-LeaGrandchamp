def hct_rechner(rbc, mcv):
    hct_percent = (rbc * mcv) / 10
    hct_fraction = hct_percent / 100
    return hct_percent, hct_fraction