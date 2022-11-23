import logging
import time
import google.cloud.logging

from prophesygg.utils import generate_payload
from prophesygg.scrape.scraper import scrape_url
from prophesygg.storage import (
    PROPHESY_STORAGE_CLIENT,
    GCSObjectStreamUpload,
    check_object_exists,
)


def scrape_to_storage(request):
    """Downloads a URL and puts its content into the specified bucket.

    Args:
        request (flask.Request): HTTP request object.

    Returns:
        Returns a blank string. Writes to bucket/blob.
    """

    client = google.cloud.logging.Client()
    client.setup_logging()

    start_time = time.perf_counter()
    success = False
    error_string = ""

    try:
        # Parse download inputs
        args = request.get_json(force=True)

        # Create streaming response
        resp = scrape_url(args["url"], stream=True)

        # Iterate through request, upload to bucket
        with GCSObjectStreamUpload(
            client=PROPHESY_STORAGE_CLIENT,
            bucket=args["bucket"],
            blob=args["blob"],
            content_type=args["content-type"],
        ) as su:
            for chunk in resp.iter_content(chunk_size=1024 * 1024):
                su.write(chunk)

        # If content_type is .rar or .gz, check size and fix name if under a certain size.
        # This is from .zips or .tar.gz that are downloaded that may become corrupted in the process.
        if args["content-type"] == "application/x-rar-compressed":
            target_bucket = PROPHESY_STORAGE_CLIENT.get_bucket(args["bucket"])
            target_blob = target_bucket.get_blob(blob)
            if target_blob.size < 1000000:
                # Rename to have "failed_" to indicate a failed write procedure
                new_blob = target_bucket.rename_blob(
                    target_blob, "failed_" + target_blob.name
                )
                blob = new_blob.name
    except Exception as e:
        error_string = str(repr(e))
        logging.error(
            "Error downloading {} to {}/{} as {}. Saw error {}".format(
                args["url"],
                args["bucket"],
                args["blob"],
                args["content-type"],
                error_string,
            )
        )

    # Check to see content exists
    target_blob_exists = check_object_exists(args["bucket"], args["blob"])
    if target_blob_exists:
        success = True

    # Stop timer calculate time
    end_time = time.perf_counter()
    total_time = round(end_time - start_time, 2)

    # Generate the payload, return any errors
    payload = {
        "url": args["url"],
        "bucket": args["bucket"],
        "blob": args["blob"],
        "content-type": args["content-type"],
    }

    if success:
        payload["status"] = "success"
    else:
        payload["status"] = "failure"
        payload["error"] = error_string

    return generate_payload("download", total_time, payload), 200
