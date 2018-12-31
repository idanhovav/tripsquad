APIListSeparator = ","

def hasExpectedParams(expectedParams, request):
    for param in expectedParams:
        if not param in request.values:
            return False

    return True

# Returns required and optional params
# If optional param not present, default value is None
def parseParams(expectedParams, request):

    return [request.values[param] if param in request.values else None for param in expectedParams]

def parseAPIList(APIListStr):
    return APIListStr.split(APIListSeparator)
