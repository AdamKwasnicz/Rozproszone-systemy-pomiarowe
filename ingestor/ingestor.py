import json
import paho.mqtt.client as mqtt
from db import get_connection

MQTT_HOST = "broker"
MQTT_PORT = 1883
MQTT_TOPIC = "lab/+/+/+"

REQUIRED_FIELDS = ["device_id", "sensor", "value", "ts_ms"]

def is_valid(data):
    return all(field in data for field in REQUIRED_FIELDS)

def save_measurement(topic, data):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO measurements
        (group_id, device_id, sensor, value, unit, ts_ms, seq, topic)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data.get("group_id"),
        data["device_id"],
        data["sensor"],
        data["value"],
        data.get("unit"),
        data["ts_ms"],
        data.get("seq"),
        topic
    ))
    conn.commit()
    cur.close()
    conn.close()

def on_connect(client, userdata, flags, rc):
    print(f"[MQTT] Polaczono z brokerem, rc={rc}")
    client.subscribe(MQTT_TOPIC)
    print(f"[MQTT] Subskrypcja: {MQTT_TOPIC}")

def on_message(client, userdata, msg):
    topic = msg.topic
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)
        if not is_valid(data):
            print(f"[SKIP] Brak wymaganych pol: {payload}")
            return
        save_measurement(topic, data)
        print(f"[OK] Zapisano z topicu: {topic}")
    except Exception as e:
        print(f"[ERR] {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_HOST, MQTT_PORT, 60)
client.loop_forever()