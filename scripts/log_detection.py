import argparse


# Arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Detection Tool")

    parser.add_argument(
        "--file",
        default="/var/log/apache2/access.log",
        help="Log file path"
    )

    parser.add_argument(
        "--threshold",
        type=int,
        default=30,
        help="HTTP request error rate threshold"
    )

    return parser.parse_args()


def analyze_and_detect(filepath, threshold):

    ip_count = {}
    ip_errors = {}
    suspicious_hits = {}

    suspicious_paths = [
        "/admin",
        "/login",
        "/.env",
        "/wp-admin",
        "/config",
        "/database"
    ]

    with open(filepath, "r") as f:
        for line in f:
            parts = line.split()

            if len(parts) < 9:
                continue

            ip = parts[0]
            url = parts[6]
            status = parts[8]

            # counting requests
            ip_count[ip] = ip_count.get(ip, 0) + 1

            # counting errors
            if status.startswith("4") or status.startswith("5"):
                ip_errors[ip] = ip_errors.get(ip, 0) + 1

            # suspicious URLs
            for path in suspicious_paths:
                if path in url:
                    if ip not in suspicious_hits:
                        suspicious_hits[ip] = []
                    suspicious_hits[ip].append(url)

    return ip_count, ip_errors, suspicious_hits


# Output
def run_detection(ip_count, ip_errors, suspicious_hits, threshold):

    print("\nDetection results:")

    # High traffic
    print("\nHigh traffic:")

    for ip, count in ip_count.items():
        if count > threshold:
            print(f"High traffic from {ip} - {count} requests")

    # Error Rate
    print("\nHTTP request error rate")

    for ip, total in ip_count.items():
        errors = ip_errors.get(ip, 0)

        if total > 0:
            error_rate = (errors / total) * 100

            if error_rate > 50:
                print(f"High error rate from {ip} - {error_rate:.2f}%")

    # Suspicious URLs
    print("\nSuspicious Activity")

    for ip, urls in suspicious_hits.items():
        print(f"Suspicious requests from {ip}:")
        for u in urls:
            print(f"  {u}")


def main():
    args = parse_args()

    ip_count, ip_errors, suspicious_hits = analyze_and_detect(
        args.file,
        args.threshold
    )

    run_detection(ip_count, ip_errors, suspicious_hits, args.threshold)


if __name__ == "__main__":
    main()