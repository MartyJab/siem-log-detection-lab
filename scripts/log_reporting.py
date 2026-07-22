import argparse
from datetime import datetime


# arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Log Analysis Reporting Tool")

    parser.add_argument(
        "--file",
        default="/var/log/apache2/access.log",
        help="Path to log file"
    )

    parser.add_argument(
        "--start",
        help="Start time (format: dd/Mon/YYYY:HH:MM:SS)"
    )

    parser.add_argument(
        "--end",
        help="End time (format: dd/Mon/YYYY:HH:MM:SS)"
    )

    parser.add_argument(
        "--ip",
        help="Filter by specific IP"
    )

    return parser.parse_args()


# time parsing
def parse_time(timestr):
    return datetime.strptime(timestr, "%d/%b/%Y:%H:%M:%S")


# analysis
def analyze_log(filepath, start_time=None, end_time=None, ip_filter=None):

    ip_count = {}
    ip_urls = {}
    status_codes = {}
    methods = {}

    first_time = None
    last_time = None

    with open(filepath, "r") as f:
        for line in f:
            parts = line.split()

            if len(parts) < 9:
                continue

            ip = parts[0]
            time_str = parts[3][1:]
            method = parts[5][1:]
            url = parts[6]
            status = parts[8]

            try:
                log_time = parse_time(time_str)
            except:
                continue

            # determine time period to be extra sure and to be able to analyze unsorted log files too
            if not first_time or log_time < first_time:
                first_time = log_time
            if not last_time or log_time > last_time:
                last_time = log_time

            # check filters
            if start_time and log_time < start_time:
                continue
            if end_time and log_time > end_time:
                continue
            if ip_filter and ip != ip_filter:
                continue

            # count IPs
            ip_count[ip] = ip_count.get(ip, 0) + 1

            # URLs per IP
            if ip not in ip_urls:
                ip_urls[ip] = {}

            ip_urls[ip][url] = ip_urls[ip].get(url, 0) + 1

            # status codes
            status_codes[status] = status_codes.get(status, 0) + 1

            # methods
            methods[method] = methods.get(method, 0) + 1

    return ip_count, ip_urls, status_codes, methods, first_time, last_time


# output
def print_results(ip_count, ip_urls, status_codes, methods, first_time, last_time):

    print("\nSummary")
    print("Total Requests:", sum(ip_count.values()))
    print("Unique IPs:", len(ip_count))

    if first_time and last_time:
        print("Time Range:", first_time, "-", last_time)

    print("\nRequests per IP")
    for ip, count in sorted(ip_count.items(), key=lambda x: x[1], reverse=True):
        print(f"{ip} - {count}")

    print("\nURLs per IP")
    for ip, urls in ip_urls.items():
        print(f"\nIP: {ip}")
        for url, count in sorted(urls.items(), key=lambda x: x[1], reverse=True):
            print(f"  {url} - {count}")

    print("\n=== Status Codes ===")
    for code, count in sorted(status_codes.items()):
        print(f"{code} - {count}")

    print("\n=== HTTP Methods ===")
    for method, count in sorted(methods.items()):
        print(f"{method} - {count}")


# main
def main():
    args = parse_args()

    start_time = parse_time(args.start) if args.start else None
    end_time = parse_time(args.end) if args.end else None

    results = analyze_log(
        args.file,
        start_time,
        end_time,
        args.ip
    )

    print_results(*results)


if __name__ == "__main__":
    main()
