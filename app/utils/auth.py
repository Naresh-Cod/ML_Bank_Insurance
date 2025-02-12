'''import os
from flask import request

def check_api_key(request):
    api_key = os.getenv("API_KEY")
    user_api_key = request.headers.get("x-api-key")
    return user_api_key == api_key
'''
import os
from flask import request

def check_api_key(request):
    api_key = os.getenv("API_KEY")  # _ Load API key from environment
    user_api_key = request.headers.get("x-api-key")  # _ Get API key from request headers

    if not user_api_key:
        return False  # ❌ No API key provided

    return user_api_key == api_key  # _ Check if API keys match
