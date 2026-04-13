# Ingestor v1 - dokumentacja

## Opis
Serwis odbierający wiadomości z brokera MQTT, walidujący ich format
i zapisujący poprawne dane do bazy PostgreSQL.

## Uruchomienie

```bash
docker compose up -d --build
```

## Struktura plików

```
ingestor/
├── ingestor.py     # główna logika serwisu
├── db.py           # połączenie z PostgreSQL
├── requirements.txt
└── Dockerfile
```

## Subskrybowany topic

```
lab/+/+/+
```

## Pola wymagane w wiadomości

- `device_id` - identyfikator urządzenia
- `sensor` - typ sensora
- `value` - wartość pomiaru (liczba)
- `ts_ms` - czas pomiaru w milisekundach od epoki Unix

## Pola opcjonalne

- `schema_version`, `group_id`, `unit`, `seq`

## Przykład wiadomości poprawnej

```json
{
  "schema_version": 1,
  "group_id": "g01",
  "device_id": "esp32-F88DAB004F8C",
  "sensor": "temperature",
  "value": 24.5,
  "unit": "C",
  "ts_ms": 1742030400000,
  "seq": 1
}
```

## Przykład wiadomości błędnej

```json
{
  "device_id": "esp32-F88DAB004F8C",
  "sensor": "temperature",
  "value": 24.5,
  "unit": "C"
}
```

Brak pola `ts_ms` - wiadomość zostanie odrzucona z logiem `[SKIP]`.

## Weryfikacja działania

Sprawdzenie logów ingestora:
```bash
docker compose logs ingestor
```

Sprawdzenie rekordów w bazie:
```bash
docker exec -it postgres psql -U admin -d abcd_db \
  -c "SELECT id, device_id, sensor, value, unit, ts_ms, received_at FROM measurements ORDER BY id DESC;"
```