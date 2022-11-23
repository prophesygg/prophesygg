import datetime


def generate_payload(service, runtime, payload_data):
    timezone = datetime.timezone.utc
    time_format = "%Y-%m-%dT%H:%M:%S%z"
    payload = {
        "service": service,
        "timestamp": datetime.datetime.now(tz=timezone).strftime(time_format),
        "runtime": runtime,
        "data": payload_data,
    }
    return payload
