from flask import Flask, request, jsonify

# OpenTelemetry SDK
from opentelemetry.sdk.metrics import MeterProvider, Meter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry import metrics,trace, _logs
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.semconv.resource import ResourceAttributes
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
    OTLPLogExporter,
)
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
import logging

# Create a Resource with the service.name attribute
resource = Resource.create({ResourceAttributes.SERVICE_NAME: "python-service"})


# Initialize OpenTelemetry SDK

# Metrics
meter = metrics.get_meter(__name__)
compute_request_count = meter.create_counter(name='app_compute_request_count', description="Counts the requests to compute-service",unit='1')

# Traces
tracer = trace.get_tracer(__name__)

# Logs
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = Flask(__name__)

@app.route('/compute_average_age', methods=['POST'])
def compute_average_age():        
    # Increment compute counter
    compute_request_count.add(1)

    # Start a new span
    with tracer.start_as_current_span("ComputeSpan"):
        logger.info("Average compute in progress")
        # Process the request data
        data = request.json['data']
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract ages from the data
        ages = [item['age'] for item in data if 'age' in item]
        if not ages:
            return jsonify({'error': 'No age data available'}), 400
        
        # Compute the average age
        average_age = round(sum(ages) / len(ages), 1)

        return jsonify({'average_age': average_age})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)