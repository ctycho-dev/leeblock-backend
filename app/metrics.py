from aioprometheus import Counter, Histogram


request_counter = Counter(name="requests_total", doc="Total number of requests received")
response_counter = Counter("responses_total", doc="Total number of responses sent")
response_histogram = Histogram(
    name="response_time_seconds",
    doc="Histogram for response time of requests",
    buckets=[0.1, 0.5, 1, 1.5, 2]
)