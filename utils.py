def hasExpectedParams(expectedParams, request):
    for param in expectedParams:
        if not param in request.values:
            return False

    return True
