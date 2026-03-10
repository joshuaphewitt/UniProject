from UniProject.app import call_api


def test_api_call():
    url = "http://api.getthedata.com/postcode/wa"  # any test API
    headers = {}  # or add your headers if needed
    result = call_api(url, headers=headers, method="GET")

    # simple check: make sure it didn't return an error string
    if result.startswith("Error:"):
        print("Test FAILED! API returned an error.")
    else:
        print("Test PASSED! API call succeeded.")
