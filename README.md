# Snowflake

The Snowflake generator done right.

See [here](https://en.wikipedia.org/wiki/Snowflake_ID) for additional information.

### Requirements

Python 3.7 and above. No additional dependencies.

### Installation

`pip install snowflake-id`

## Usage

### Using generator

```python
from snowflake import SnowflakeGenerator

gen = SnowflakeGenerator(42)

for i in range(100):
    val = next(gen)
    print(val)
```
#### Output:

```text
6820698575169822721
6820698575169822722
6820698575169822723
6820698575174017024
6820698575174017025
...
```

### Parse snowflake id

```python
from snowflake import Snowflake

sf = Snowflake.parse(856165981072306191, 1288834974657)

print(f"{sf.timestamp = }")
print(f"{sf.instance = }")
print(f"{sf.epoch = }")
print(f"{sf.seq = }")
print(f"{sf.seconds = }")
print(f"{sf.milliseconds = }")
print(f"{sf.datetime = }")
```

#### Output:

```text
sf.timestamp = 204125876682
sf.instance = 363
sf.epoch = 1288834974657
sf.seq = 15
sf.seconds = 1492960851.339
sf.milliseconds = 1492960851339
sf.datetime = datetime.datetime(2017, 4, 23, 15, 20, 51, 339000)
```

### Load generator state

```python
from snowflake import SnowflakeGenerator, Snowflake

sf = Snowflake.parse(856165981072306191, 1288834974657)
gen = SnowflakeGenerator.from_snowflake(sf)

for i in range(100):
    val = next(gen)
    print(val)
```

#### Output:

```text
1414934653136449536
1414934653136449537
1414934653136449538
1414934653136449539
1414934653136449540
...
```
