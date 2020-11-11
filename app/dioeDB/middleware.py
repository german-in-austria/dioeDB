from http import cookies
cookies.Morsel._reserved["samesite"] = "SameSite"

class SameSiteMiddleware:
  def process_response(self, request, response):
    if request.get_host() != '127.0.0.1:8000':
      for name, value in response.cookies.items():
        if not value.get("samesite"):
            value["samesite"] = "None"
            value["secure"] = True  # fixes plain set_cookie(name, value)
    return response
