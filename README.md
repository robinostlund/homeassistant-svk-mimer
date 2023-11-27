[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)
![Version](https://img.shields.io/github/v/release/robinostlund/homeassistant-svk-mimer)
![PyPi](https://img.shields.io/pypi/v/aiosvkmimer?label=latest%20pypi)
![Downloads](https://img.shields.io/github/downloads/robinostlund/homeassistant-svk-mimer/total)
![CodeStyle](https://img.shields.io/badge/code%20style-black-black)
![Known Vulnerabilities](https://snyk.io/test/github/robinostlund/homeassistant-svk-mimer/badge.svg)
[![CodeQL](https://github.com/robinostlund/homeassistant-svk-mimer/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/robinostlund/homeassistant-svk-mimer/actions/workflows/codeql-analysis.yml)

# homeassistant-svk-mimer
Home assistant custom component for SVK Mimer

## HACS Installation
Go to the hacs store and use the repo url https://github.com/robinostlund/homeassistant-svk-mimer and add this as a custom repository under settings.

## Apex Charts
### FCR-D Forecast
Example configuration to show FCR-D 24h forecast
![Alt text](assets/example-fcr-d-forecast.png?raw=true "FCR-D Forecast")
```bash
type: custom:apexcharts-card
now:
  show: true
  label: NOW
graph_span: 2d
stacked: true
update_interval: 5min
apex_config:
  chart:
    height: 350px
  yaxis:
    forceNiceScale: true
    decimalsInFloat: 2
    min: 0
    title:
      text: SEK
      offsetX: 10
      offsetY: 0
      rotate: -90
  xaxis:
    tooltip:
      enabled: false
all_series_config:
  type: column
  show:
    extremas: false
    in_header: true
    legend_value: false
    offset_in_name: false
header:
  title: FCR-D Forecast - 24 hours
  show: true
  show_states: true
  colorize_states: true
  standard_format: true
  disable_actions: true
span:
  start: day
  offset: '-0h'
series:
  - entity: sensor.svk_mimer_price_fcr_d_down
    color: YellowGreen
    name: FCR-D Down
    data_generator: |
      return (entity.attributes.today_raw.map((start, index) => {
        return [new Date(start["start"]).getTime(), entity.attributes.today_raw[index]["value"]];
      })).concat(entity.attributes.tomorrow_raw.map((start, index) => {
        return [new Date(start["start"]).getTime(), entity.attributes.tomorrow_raw[index]["value"]];
      }));
  - entity: sensor.svk_mimer_price_fcr_d_up
    color: turquoise
    name: FCR-D Up
    data_generator: |
      return (entity.attributes.today_raw.map((start, index) => {
        return [new Date(start["start"]).getTime(), entity.attributes.today_raw[index]["value"]];
      })).concat(entity.attributes.tomorrow_raw.map((start, index) => {
        return [new Date(start["start"]).getTime(), entity.attributes.tomorrow_raw[index]["value"]];
      }));
```

### FCR-D History
Example configuration to show FCR-D 12 months earnings history
![Alt text](assets/example-fcr-d-history.png?raw=true "FCR-D History")
```bash
type: custom:apexcharts-card
now:
  show: false
  label: NOW
graph_span: 12month
stacked: true
update_interval: 5min
apex_config:
  chart:
    height: 350px
  yaxis:
    forceNiceScale: true
    decimalsInFloat: 2
    min: 0
    title:
      text: SEK
      offsetX: 10
      offsetY: 0
      rotate: -90
  xaxis:
    tooltip:
      enabled: false
all_series_config:
  type: column
  group_by:
    func: sum
    duration: 1month
    fill: zero
    start_with_last: false
  show:
    extremas: false
    in_header: true
    legend_value: false
    offset_in_name: false
header:
  title: FCR-D History - 12 months
  show: true
  show_states: false
  colorize_states: true
  standard_format: true
  disable_actions: true
span:
  start: month
  offset: '-11month'
series:
  - entity: sensor.svk_mimer_earnings_today_fcr_d_down
    color: YellowGreen
    name: FCR-D Down
    statistics:
      type: state
      period: day
      align: start
  - entity: sensor.svk_mimer_earnings_today_fcr_d_up
    color: turquoise
    name: FCR-D Up
    statistics:
      type: state
      period: day
      align: start
```