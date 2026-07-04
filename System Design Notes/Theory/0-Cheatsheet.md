Cheat Sheet
Here is a one-stop-shop for the numbers you need to know in 2026. These numbers represent typical values for well-tuned systems with specific workloads - your requirements may vary based on workload, hardware, and configuration. Use them as a starting point for capacity planning and system design discussions, not as hard limits. Remember that cloud providers regularly update their offerings, so while I'll try to keep this up to date, it should be treated more as a starting point than a hard limit.

Component	Key Metrics	Scale Triggers
Caching	- ~1 millisecond latency
- 100k+ operations/second
- Memory-bound (up to 1TB)	-

When to scale:
- When Hit rate is less than 80%
- Latency requirement is less than 1ms
- Memory usage is more than 80%
- Cache churn/thrashing

Databases	
- Up to 50k transactions/second
- Sub-5ms read latency (cached)
- 64 TiB+ storage capacity

When to scale:
- Write throughput  requirement is more than 10k TPS
- Read latency requirement is more than 5ms uncached
- Geographic distribution needs

App Servers	
- 100k+ concurrent connections
- 8-64 cores @ 2-4 GHz
- 64-512GB RAM standard, up to 2TB	

When to scale:
- CPU > 70% utilization
- Response latency > SLA
- Connections near 100k/instance
- Memory > 80%

Message Queues	
- Up to 1 million msgs/sec per broker
- Sub-5ms end-to-end latency
- Up to 50TB storage	

When to scale:
- Throughput near 800k msgs/sec
- Partition count ~200k per cluster
- Growing consumer lag