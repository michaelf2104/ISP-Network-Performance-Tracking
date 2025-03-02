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
```

### **2️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3️⃣ Configure API Access**
replace the API key in config.json
```bash
{
  "api_key": "your_api_key_here",
  "influxdb_host": "localhost",
  "influxdb_port": 8086
}
```

### **4️⃣ Start the Application**
```bash
python src/main.py
```

---

## 📊 Grafana Dashboard Setup  

### ✅ Connect InfluxDB as a Data Source  
Configure it via the Grafana UI  

### ✅ Customize Visualizations  
Adjust panels to fit specific monitoring needs  

---

## 🛠️ Technologies Used  

- **Python** – Backend processing  
- **RIPE Atlas API** – Network measurements  
- **InfluxDB** – Time-series database  
- **Grafana** – Data visualization  

---

## 📜 License  

This project is licensed under the **MIT License**, allowing free use and modifications.  

---

## 👨‍💻 Author  

**Michael Faltermeier** 🎓 – _Bachelor’s Thesis Project, Ostbayerische Technische Hochschule Regensburg_  
📧 [michael.faltermeier.st@gmail.com](mailto:michael.faltermeier.st@gmail.com)  
📍 **Regensburg, Germany** 🇩🇪  
