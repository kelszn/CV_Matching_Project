def filter_metadata(profile_raw):
    return [
        l for l in profile_raw
        if ";" in l or "|" in l or "," in l
    ]