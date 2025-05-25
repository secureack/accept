# Accept

[![Accept Test](https://github.com/secureack/accept/actions/workflows/accept_test.yml/badge.svg)](https://github.com/secureack/accept/actions/workflows/accept_test.yml)

Data ingest and pipeline solution for log ingestion and normalization as a Python based alternative to similar solutions such as FluentD. Accept being Python based hold several advantages when applied within the cybersecurity space given the prevalence of python skills and aims to simplify security log collection and normalization.

Architecturally Accept uses a main process to input data from inputs, whereby it is saved to a disk buffer. Once the buffer is ready to be flushed a processing process is executed whereby the events are processed. This concept addresses vertical scaling challenges and enables accept to process data across CPUs.

## Pipelines

Pipelines are defined in simple YAML format consisting of inputs, processors, and outputs; chaining together multiple processors allows us to build out the data pipeline to manipulate the initial event received on the input and processed on the output.

```
input:
  id: 1
  name: <some_input_name>
  type: <plugin>
  ...
    extra properties
  ...
  next: [2]

processor:
  id: 2
  type: <plugin>
  ...
    extra properties
  ...
  next: [3]

output:
  id: 3
  type: <plugin>
  ...
    extra properties
  ...
```

For config examples see [Samples](https://github.com/secureack/accept/tree/main/samples)

## Getting Started

[Setup Documentation](https://github.com/secureack/accept/wiki/Setup)

## Documentation

[Documentation](https://github.com/secureack/accept/wiki)
