from datetime import datetime
import pytz

# Beispiel-Referenzbereiche (bitte mit euren Werten ersetzen!)
REF = {
    "weiblich": [(18, 120, 36.0, 46.0)],
    "männlich": [(18, 120, 41.0, 53.0)],
}

def get_ref(sex: str, age: int):
    for a_min, a_max, lo, hi in REF.get(sex, []):
        if a_min <= age <= a_max:
            return lo, hi
    return None, None

def hct_rechner(rbc, mcv):
    hct_percent = (rbc * mcv) / 10
    hct_fraction = hct_percent / 100
    
    return {
        "timestamp": datetime.now(pytz.timezone('Europe/Zurich')),  # Current swiss time
        "rbc": rbc,
        "mcv": mcv,
        "hct_fraction": hct_fraction,
        "hct_percent": hct_percent,
    } 