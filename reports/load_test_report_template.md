# Load Test Report Template

## Test Metadata
- Date:
- Environment:
- Server command:
- Client command:
- Endpoint tested:

## Results
- Duration (s):
- Concurrency:
- Total requests:
- Requests/sec:
- Requests/hour:
- Avg latency (ms):
- P95 latency (ms):
- P99 latency (ms):
- Error rate (%):
- Status code distribution:

## Claim Check
- Passes 10K+/hour threshold (>= 2.78 req/s): YES/NO
- Passes sub-200ms avg latency: YES/NO
- Near-zero failures (<1%): YES/NO

## Resume statement (use only if metrics above pass)
- Benchmarked the Flask fraud-scoring API at 10K+ requests/hour under sustained load with sub-200ms average latency and under 1% failed requests.
