[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)
![Version](https://img.shields.io/github/v/release/robinostlund/homeassistant-svk-mimer)
![PyPi](https://img.shields.io/pypi/v/aiosvkmimer?label=latest%20pypi)
![Downloads](https://img.shields.io/github/downloads/robinostlund/homeassistant-svk-mimer/total)
![CodeStyle](https://img.shields.io/badge/code%20style-black-black)
![Known Vulnerabilities](https://snyk.io/test/github/robinostlund/homeassistant-svk-mimer/badge.svg)
[![CodeQL](https://github.com/robinostlund/homeassistant-svk-mimer/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/robinostlund/homeassistant-svk-mimer/actions/workflows/codeql-analysis.yml)

# homeassistant-svk-mimer
Home assistant custom component for SVK Mimer

# IN DEVELOPMENT


## HACS Installation
Go to the hacs store and use the repo url https://github.com/robinostlund/homeassistant-svk-mimer and add this as a custom repository under settings.


## Apex Charts
### FCR-N
Example configuration to show my expecting earnings per hour
```bash
type: custom:apexcharts-card
graph_span: 24h
header:
  title: FCR-N (SEK)
  show: true
span:
  start: day
now:
  show: true
  label: Now
series:
  - entity: sensor.svk_mimer_price_fcr_n
    type: column
    float_precision: 3
    data_generator: |
      return entity.attributes.today_raw.map((start, index) => {
        return [new Date(start["start"]).getTime(), entity.attributes.today_raw[index]["value"]];
      });
```

### FCR-D
Example configuration to show my expecting earnings per hour
```bash
type: custom:apexcharts-card
graph_span: 24h
header:
  title: FCR-D (SEK)
  show: true
span:
  start: day
now:
  show: true
  label: Now
series:
  - entity: sensor.svk_mimer_price_fcr_d
    type: column
    float_precision: 3
    data_generator: |
      return entity.attributes.today_raw.map((start, index) => {
        return [new Date(start["start"]).getTime(), entity.attributes.today_raw[index]["value"]];
      });
```

### FCR-D Down
Example configuration to show my expecting earnings per hour
```bash
type: custom:apexcharts-card
graph_span: 24h
header:
  title: FCR-D DOWN (SEK)
  show: true
span:
  start: day
now:
  show: true
  label: Now
series:
  - entity: sensor.svk_mimer_price_fcr_d_down
    type: column
    float_precision: 3
    data_generator: |
      return entity.attributes.today_raw.map((start, index) => {
        return [new Date(start["start"]).getTime(), entity.attributes.today_raw[index]["value"]];
      });
```

### FCR-D Up
Example configuration to show my expecting earnings per hour
```bash
type: custom:apexcharts-card
graph_span: 24h
header:
  title: FCR-D UP (SEK)
  show: true
span:
  start: day
now:
  show: true
  label: Now
series:
  - entity: sensor.svk_mimer_price_fcr_d_up
    type: column
    float_precision: 3
    data_generator: |
      return entity.attributes.today_raw.map((start, index) => {
        return [new Date(start["start"]).getTime(), entity.attributes.today_raw[index]["value"]];
      });
```