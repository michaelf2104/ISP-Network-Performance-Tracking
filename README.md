# ISP-Network-Performance-Tracking 🚀  

### **Data-Driven Monitoring of ISP Network Performance**  
A **Python-based tool** for continuously evaluating **latency and packet loss from RIPE Atlas measurements**. The software integrates **InfluxDB** for efficient long-term data storage and provides **Grafana dashboards** for clear visualization of measured values. Additionally, it supports **peering & transit cost optimization**, enabling ISPs to assess cost-effective routing strategies.  

---

## **🌟 Key Features**  
✅ **Continuous Latency & Packet Loss Evaluation** – Automates RIPE Atlas data collection for real-time insights  
✅ **InfluxDB Integration** – Efficiently stores data points for long-term analysis  
✅ **Grafana Dashboards** – Visualizes network performance trends for better insights  
✅ **Peering & Transit Cost Optimization** – Helps ISPs evaluate cost-effective routing strategies  

---

## **📌 Use Cases**  
📍 **Network Performance Monitoring** – Track latency and packet loss trends over time  
📍 **Bottleneck Identification** – Detect inefficient routing paths and high-latency connections  
📍 **Peering & Transit Cost Evaluation** – Assess interconnection strategies for cost and performance benefits  
📍 **Routing Optimization** – Compare peering and transit performance for data-driven decision-making  

---

## **📦 Installation**  

### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/michaelf2104/ISP-Network-Performance-Tracking.git
cd ISP-Network-Performance-Tracking

pip install -r requirements.txt

{
  "api_key": "your_api_key_here",
  "influxdb_host": "localhost",
  "influxdb_port": 8086
}

python src/main.py

