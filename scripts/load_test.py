import argparse
import json
import statistics
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import requests


DEFAULT_PAYLOAD = {
    "V1": -1.3598071336738,
    "V2": -0.0727811733098497,
    "V3": 2.53634673796914,
    "V4": 1.37815522427443,
    "V5": -0.338320769942518,
    "V6": 0.462387777762292,
    "V7": 0.239598554061257,
    "V8": 0.0986979012610507,
    "V9": 0.363786969611213,
    "V10": 0.0907941719789316,
    "V11": -0.551599533260813,
    "V12": -0.617800855762348,
    "V13": -0.991389847235408,
    "V14": -0.311169353699879,
    "V15": 1.46817697209427,
    "V16": -0.470400525259478,
    "V17": 0.207971241929242,
    "V18": 0.0257905801985591,
    "V19": 0.403992960255733,
    "V20": 0.251412098239705,
    "V21": -0.018306777944153,
    "V22": 0.277837575558899,
    "V23": -0.110473910188767,
    "V24": 0.0669280749146731,
    "V25": 0.128539358273528,
    "V26": -0.189114843888824,
    "V27": 0.133558376740387,
    "V28": -0.0210530534538215,
    "Amount": 149.62,
}

thread_local = threading.local()


def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def percentile(values, fraction):
    if not values:
        return 0.0
    ordered = sorted(values)
    index = int(round((len(ordered) - 1) * fraction))
    return ordered[index]


def worker(url, payload, timeout_seconds):
    session = get_session()
    started = time.perf_counter()
    status_code = None
    is_success = False

    try:
        response = session.post(url, json=payload, timeout=timeout_seconds)
        status_code = response.status_code
        is_success = status_code == 200
    except requests.RequestException:
        is_success = False

    latency_ms = (time.perf_counter() - started) * 1000
    return is_success, latency_ms, status_code


def run_load_test(url, payload, duration_seconds, concurrency, timeout_seconds):
    started = time.perf_counter()
    latencies_ms = []
    success_count = 0
    failure_count = 0
    status_counts = {}

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = set()
        while time.perf_counter() - started < duration_seconds:
            while len(futures) < concurrency:
                futures.add(executor.submit(worker, url, payload, timeout_seconds))

            completed = []
            for future in as_completed(futures, timeout=1):
                completed.append(future)
                is_success, latency_ms, status_code = future.result()
                latencies_ms.append(latency_ms)
                if is_success:
                    success_count += 1
                else:
                    failure_count += 1
                key = str(status_code) if status_code is not None else "request_exception"
                status_counts[key] = status_counts.get(key, 0) + 1
                break

            for future in completed:
                futures.remove(future)

    elapsed_seconds = max(time.perf_counter() - started, 1e-9)
    total_requests = success_count + failure_count
    throughput_rps = total_requests / elapsed_seconds
    throughput_rph = throughput_rps * 3600
    error_rate = (failure_count / total_requests) if total_requests else 1.0

    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "target_url": url,
        "duration_seconds": round(elapsed_seconds, 2),
        "concurrency": concurrency,
        "total_requests": total_requests,
        "success_count": success_count,
        "failure_count": failure_count,
        "error_rate_percent": round(error_rate * 100, 3),
        "requests_per_second": round(throughput_rps, 3),
        "requests_per_hour": round(throughput_rph, 2),
        "latency_ms_avg": round(statistics.mean(latencies_ms), 2) if latencies_ms else 0.0,
        "latency_ms_p95": round(percentile(latencies_ms, 0.95), 2) if latencies_ms else 0.0,
        "latency_ms_p99": round(percentile(latencies_ms, 0.99), 2) if latencies_ms else 0.0,
        "status_code_distribution": status_counts,
    }


def main():
    parser = argparse.ArgumentParser(description="Simple sustained load test for /predict endpoint")
    parser.add_argument("--base-url", default="http://127.0.0.1:5000", help="Base API URL")
    parser.add_argument("--endpoint", default="/predict", help="Prediction endpoint path")
    parser.add_argument("--duration", type=int, default=300, help="Test duration in seconds")
    parser.add_argument("--concurrency", type=int, default=8, help="Number of concurrent workers")
    parser.add_argument("--timeout", type=float, default=5.0, help="Request timeout in seconds")
    parser.add_argument("--output", default="reports/load_test_result.json", help="Result output JSON file")
    args = parser.parse_args()

    endpoint = args.endpoint if args.endpoint.startswith("/") else f"/{args.endpoint}"
    url = f"{args.base_url.rstrip('/')}{endpoint}"

    result = run_load_test(
        url=url,
        payload=DEFAULT_PAYLOAD,
        duration_seconds=args.duration,
        concurrency=args.concurrency,
        timeout_seconds=args.timeout,
    )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(json.dumps(result, indent=2))
    print(f"\nSaved report to: {output_path}")


if __name__ == "__main__":
    main()
