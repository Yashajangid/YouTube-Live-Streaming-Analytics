# Large Scale Real-Time YouTube Analytics using Kafka, Spark & Hadoop
## Distributed Streaming Pipeline with Master-Worker Architecture

## ABSTRACT

In the era of Big Data, real-time analytics on streaming platforms like YouTube has become critical for business intelligence and trend analysis. Traditional databases fail to handle the *Volume, Velocity, and Variety* of YouTube's streaming data (5B+ daily views, 300+ hours uploaded/minute).

This *Advanced Databases Project* implements a *complete distributed streaming pipeline* using *Kafka (message broker), **Spark (stream processing), and **Hadoop ecosystem* across *Master + 2 Worker nodes. We analyzed **400K+ real YouTube videos* from Kaggle dataset, achieving *real-time analytics* with *live dashboard visualization*.

*Key Achievements:*
- ✅ *Master Node*: Kafka broker + data ingestion
- ✅ *Worker Nodes*: Spark processing + distributed analytics  
- ✅ *Live UI*: Filterable dashboard (1M+ views, engagement %)
- ✅ *Scalable*: Ready for Hadoop cluster deployment

---

## INTRODUCTION

*Big Data Characteristics: YouTube generates **Petabytes daily* across videos, metadata, and user interactions. Traditional RDBMS cannot handle this *3V challenge* (Volume: 600MB+ dataset, Velocity: real-time streams, Variety: JSON/CSV formats).

*Our Solution: **Distributed streaming architecture* simulating production Hadoop clusters:
