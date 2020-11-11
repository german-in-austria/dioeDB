from http import cookies
cookies.Morsel._reserved["samesite"] = "SameSite"

class SameSiteMiddleware:
  def process_response(self, request, response):
    for name, value in response.cookies.items():
      if not value.get("samesite"):
          value["samesite"] = "None"
          value["secure"] = True  # fixes plain set_cookie(name, value)
    return response
