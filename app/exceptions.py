class AppError(Exception):
    """앱 공통 에러 기반 클래스"""
    status_code: int = 500

    def __init__(self, message: str):
        self.message = message


class InvalidParameterError(AppError):
    """잘못된 파라미터 (400)"""
    status_code = 400


class NotFoundError(AppError):
    """리소스를 찾을 수 없음 (404)"""
    status_code = 404


class ExternalAPIError(AppError):
    """외부 API 호출 실패 (502)"""
    status_code = 502
