def success(message: str, data: dict = None):
    resp = {"success": True, "message": message}
    if data:
        resp.update(data)
    return resp

def error(message: str, code: int = 400):
    return {"success": False, "error": message, "code": code}
