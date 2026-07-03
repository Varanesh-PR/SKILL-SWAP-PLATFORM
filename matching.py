def find_match(current_user, users):
    matches = []

    for u1 in users:
        if u1['name'] == current_user:
            for u2 in users:
                if u1 != u2 and u1['learn'] == u2['teach']:
                    matches.append(u2['name'])

    return matches