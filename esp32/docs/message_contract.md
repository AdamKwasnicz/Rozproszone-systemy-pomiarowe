# Message Contract v1

## Struktura topicu
```
lab/<group_id>/<device_id>/<sensor>
```

Przykład:
```
lab/g01/esp32-F88DAB004F8C/temperature
```

## Format wiadomości JSON
```json
{
  "schema_version": 1,
  "group_id": "g01",
  "device_id": "esp32-F88DAB004F8C",
  "sensor": "temperature",
  "value": 24.5,
  "unit": "C",
  "ts_ms": 1774285098907,
  "seq": 0
}
```

## Pola wymagane

| Pole | Typ | Opis |
|---|---|---|
| device_id | string | Unikalny identyfikator urządzenia |
| sensor | string | Rodzaj sensora |
| value | number | Wartość pomiaru |
| ts_ms | integer | Czas pomiaru (Unix epoch, ms) |

## Pola opcjonalne

| Pole | Typ | Opis |
|---|---|---|
| schema_version | integer | Wersja kontraktu |
| group_id | string | Identyfikator grupy |
| unit | string | Jednostka fizyczna |
| seq | integer | Numer sekwencyjny wiadomości |

## Reguły walidacji

- `device_id` - niepusty string
- `sensor` - niepusty string
- `value` - liczba
- `ts_ms` - dodatnia liczba całkowita
- `unit` - jeśli podana, musi odpowiadać typowi sensora
- `seq` - jeśli podany, nieujemna liczba całkowita

## Przykład wiadomości poprawnej
```json
{
  "schema_version": 1,
  "group_id": "g01",
  "device_id": "esp32-F88DAB004F8C",
  "sensor": "temperature",
  "value": 24.5,
  "unit": "C",
  "ts_ms": 1774285098907,
  "seq": 1
}
```

## Przykłady wiadomości błędnych

### Brak pola ts_ms
```json
{
  "device_id": "esp32-F88DAB004F8C",
  "sensor": "temperature",
  "value": 24.5,
  "unit": "C"
}
```

### value zapisane jako string
```json
{
  "device_id": "esp32-F88DAB004F8C",
  "sensor": "temperature",
  "value": "24.5",
  "unit": "C",
  "ts_ms": 1774285098907
}
```