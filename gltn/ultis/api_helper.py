from pprint import pprint

from rest_framework import status
from rest_framework.response import Response
from functools import wraps


def api_decorator(func):
    def show_error_to_client(msg='Undefined error', code=status.HTTP_400_BAD_REQUEST):
        pprint(msg)

        response_data = {
            "status_code": code,
            "message": msg,
            "data": {}
        }

        return Response(response_data, status=code)

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            data, msg, code = func(*args, **kwargs)

            if msg == "The user does not exist, OTP was sent successful":
                response = {
                    'status_code': 204,
                    'message': msg,
                    'data': data
                }
            else:
                response = {
                    'status_code': code,
                    'message': msg,
                    'data': data
                }
            pprint(response)
            return Response(data=response, status=code)
        except Exception as e:
            try:
                if len(e.args) > 0:
                    error_value = e.args[0]

                    if isinstance(error_value, dict):
                        first_key = next(iter(error_value))
                        error_message = error_value[first_key]

                        if isinstance(error_message, list):
                            error_message = error_message[0]

                    else:
                        error_message = error_value
                else:
                    error_message = str(e)
                return show_error_to_client(msg=error_message.capitalize())

            except:
                return show_error_to_client(msg=str(e))

    return wrapper


def format_time_difference(start_datetime, end_datetime):
    time_difference = end_datetime - start_datetime

    years = time_difference.days // 365
    remaining_days = time_difference.days % 365
    months = remaining_days // 30
    remaining_days %= 30
    days = remaining_days
    hours, remainder = divmod(time_difference.seconds, 3600)
    minutes = remainder // 60

    if years > 0:
        return f"Đăng {years} năm trước"
    elif months > 0:
        return f"Đăng {months} tháng trước"
    elif days > 0:
        return f"Đăng {days} ngày trước"
    elif hours > 0:
        return f"Đăng {hours} giờ trước"
    elif minutes > 0:
        return f"Đăng {minutes} phút trước"
    else:
        return "Vừa đăng"
