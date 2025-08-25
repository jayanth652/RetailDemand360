import argparse, time, json, random, uuid, datetime
try:
    from kafka import KafkaProducer
    HAVE_KAFKA = True
except Exception:
    HAVE_KAFKA = False

PRODUCTS = [{"product_id": f"P{i:04d}", "category": random.choice(["Grocery","Electronics","Apparel","Household"]), "price": round(random.uniform(2, 400), 2)} for i in range(1, 301)]
STORES = [f"S{i:03d}" for i in range(1, 51)]

def txn_event():
    p = random.choice(PRODUCTS); qty = random.randint(1, 5)
    return {"event_id": str(uuid.uuid4()), "ts": datetime.datetime.utcnow().isoformat(), "store_id": random.choice(STORES),
            "product_id": p["product_id"], "category": p["category"], "unit_price": p["price"], "qty": qty,
            "amount": round(p["price"]*qty, 2), "promotion": random.choice([0,0,10,15,20])}

def main(rate, minutes, kafka_broker, topic):
    end = time.time() + minutes*60
    prod = None
    if HAVE_KAFKA and kafka_broker:
        prod = KafkaProducer(bootstrap_servers=kafka_broker, value_serializer=lambda v: json.dumps(v).encode("utf-8"))
        print(f"Producing to Kafka {kafka_broker} topic {topic}")
    else:
        print("Kafka not available; writing to local ndjson file data/generator/out.ndjson")
        f = open("data/generator/out.ndjson","a", encoding="utf-8")

    while time.time() < end:
        for _ in range(rate):
            ev = txn_event()
            if prod:
                prod.send(topic, ev)
            else:
                f.write(json.dumps(ev)+"\n")
        time.sleep(1.0)

    if not prod:
        f.close()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--rate", type=int, default=5)
    ap.add_argument("--minutes", type=int, default=1)
    ap.add_argument("--kafka-broker", type=str, default="localhost:9092")
    ap.add_argument("--topic", type=str, default="transactions")
    args = ap.parse_args()
    main(args.rate, args.minutes, args.kafka_broker, args.topic)
