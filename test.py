from prometheus_client import start_http_server, Gauge
import time


class TimestampedGauge(Gauge):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def collect(self):
        metrics = super().collect()
        for metric in metrics:
            samples = []
            for sample in metric.samples:
                timestamp = sample.labels.pop("timestamp", None)
                sample_with_timestamp = type(sample)(sample.name, sample.labels,
                                                     sample.value, timestamp, sample.exemplar)
                samples.append(sample_with_timestamp)
            metric.samples = samples
        return metrics


def set_value_with_timestamp(metric, labels, value, timestamp):
    labels["timestamp"] = timestamp
    metric.labels(**labels).set(value)


frigate_events = TimestampedGauge("frigate_event", "Frigate Event Metric", ["camera", "label", "id", "timestamp"])
labels1 = {"camera": "test1", "label": "person", "id": "tytew"}
labels2 = {"camera": "test2", "label": "car", "id": "sdfadsasdff"}


if __name__ == '__main__':
    # Start the Prometheus exporter server on port 8000
    start_http_server(8000)
    while True:
        set_value_with_timestamp(frigate_events, labels1, 1, 17444362232)
        time.sleep(1)

        set_value_with_timestamp(frigate_events, labels2, 1, 17444362299)
        time.sleep(1)
