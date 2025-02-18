# Accept

Data ingest and pipeline solution for log ingestion and normalization as a Python based alternative to similar solutions such as FluentD. Accept being Python based hold several advantages when applied within the cybersecurity space given the prevalence of python skills and aims to simplify security log collection and normalization.

Architecturally Accept uses a main process to input data from inputs, whereby it is saved to a disk buffer. Once the buffer is ready to be flushed a processing process is executed whereby the events are processed. This concept addresses vertical scaling challenges and enables accept to process data across CPUs.

## Getting Started

[Setup Documentation](https://github.com/secureack/accept/wiki/Setup)

## Documentation

[Documentation](https://github.com/secureack/accept/wiki)
