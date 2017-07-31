from arquivo.models import TobToken


def tobToken(username, token, server, is_active):
    return TobToken(username=username, token=token, server=server, is_active=is_active)


def findAllValidTokens(limit : int = 0):
    return TobToken.objects.filter(is_active=True) if not limit else TobToken.objects.filter(is_active=True)[:limit]

def findAll(limit : int = 0):
    return TobToken.objects.all() if not limit else TobToken.objects.all()[:limit]