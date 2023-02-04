from collections import Counter


class Code:
    def __init__(self, codename, torecode):
        if not isinstance(codename, str) or not isinstance(torecode, str) or len(codename) == 0 or len(torecode) == 0:
            raise ValueError("invalid argument!")
        self.codename = codename
        self.torecode = torecode


class Recommendation:
    MAX_TORE_CODES = 3
    def __init__(self, codename, torecodes):
        if not isinstance(codename, str) or len(codename) == 0 \
                or not type(torecodes) == list or len(torecodes) == 0 or len(torecodes) > self.MAX_TORE_CODES:
            raise ValueError("invalid argument!")
        self.codename = codename
        self.torecodes = torecodes


def build(codes):
    dic = {}
    for code in codes:
        dic.setdefault(code.codename, []).append(code.torecode)

    for codename in dic:
        dic[codename] = Counter(dic[codename]).most_common(Recommendation.MAX_TORE_CODES)

    recommendations = []
    for codename in dic:
        recommendations.append(Recommendation(codename, list(dict(dic[codename]).keys())))

    return recommendations