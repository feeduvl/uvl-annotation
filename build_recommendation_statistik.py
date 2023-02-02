from collections import Counter

class Code:
    def __init__(self, codename, torecode):
        if not isinstance(codename, str) or not isinstance(torecode, str) or len(codename) == 0 or len(torecode) == 0:
            raise ValueError("invalid argument!")
        self.codename = codename
        self.torecode = torecode

class Recommendation:
    def __init__(self, codename, torecodes):
        self.codename = codename
        self.torecodes = torecodes

def build(codes):
    dic = {}
    for code in codes:
        dic.setdefault(code.codename, []).append(code.torecode)

    for codename in dic:
        dic[codename] = Counter(dic[codename]).most_common(3)

    recommendations = []
    for codename in dic:
        recommendations.append(Recommendation(codename, list(dict(dic[codename]).keys())))

    return recommendations