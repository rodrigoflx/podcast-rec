# Podcast Transcription System
The Podcast Transcription System is a distributed Python-based application that leverages the iTunes API to consume podcast information, parse RSS feeds, download podcast episodes, and transcribe the content using the Whisper library. This system is designed to efficiently transcribe podcast episodes by distributing tasks across multiple workers using Redis Queue (RQ) for message broking. Docker Swarm is used to orchestrate and coordinate the deployment of individual modules.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Docker Deployment](#docker-deployment)
- [Dependencies](#dependencies)
- [License](#license)

## Overview

Podcast Transcription System is composed of several modules, each handling a specific aspect of the transcription process:

- **Itunes API Consumer**: Fetches podcast information from the iTunes API, retrieves RSS feed links, and enqueues jobs for the RSS Parser.

- **RSS Parser**: Parses RSS feeds, extracts episode details, and enqueues jobs for the Downloader.

- **Downloader**: Downloads podcast episodes directly from URLs and enqueues jobs for the Transcriber.

- **Transcriber**: Utilizes the Whisper library to transcribe downloaded podcast episodes and saves the transcriptions to a database.

The message broking and communication between these modules are facilitated by Redis Queue (RQ), and Docker Swarm is used to deploy and orchestrate the system.

## Architecture

The architecture of the Podcast Transcription System follows a distributed approach using Redis Queue for inter-module communication. Docker Swarm coordinates the deployment of individual modules within separate Docker containers. Here's an overview:

```
+------------------------+
|   Itunes API Consumer  |
+------------------------+
           |
           v
+------------------------+
|       RSS Parser       |
+------------------------+
           |
           v
+------------------------+
|       Downloader       |
+------------------------+
           |
           v
+------------------------+
|       Transcriber       |
+------------------------+
```

## Getting Started

To get started with the Podcast Transcription System using Docker Swarm, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/podcast-transcription-system.git
    ```

2. Build Docker images:

    ```bash
    docker-compose build
    ```

3. Deploy the stack using Docker Swarm:

    ```bash
    docker stack deploy -c docker-compose.yml podcast-rec
    ```

4. Monitor the stack:

    ```bash
    docker stack ps podcast-rec
    ```

## Usage

The Podcast Transcription System is designed to be flexible and customizable. You can adapt it to your specific use case by extending or modifying the existing modules. To enqueue jobs for specific tasks, use the appropriate module based on your workflow.

You can also scale up the amount of workers based on your infrastructure

```bash
docker service scale downloader=10
```

## Docker Deployment

Docker Swarm is used to orchestrate the deployment of individual modules. Each module has its own Dockerfile and dependencies specified in a separate requirements file.

## Dependencies

The Podcast Transcription System relies on the following key dependencies:

- [Redis](https://redis.io/): Message broking and task queue management.
- [Whisper](https://github.com/HawkAaron/wav2vec2-wrapping): Speech-to-text transcription library.

## License
This project is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/).

You are free to:

- Share: Copy and redistribute the material in any medium or format.
- Adapt: Remix, transform, and build upon the material for any purpose, even commercially.

Under the following terms:

- Attribution: You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
- ShareAlike: If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.

See the [LICENSE](LICENSE) file for more details.
