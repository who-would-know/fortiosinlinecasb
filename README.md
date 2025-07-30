# FortiOS API get inline-casb application list

## Requirements

This script requires the following Python libraries:

- `requests`
- `urllib3` (usually installed as a dependency of `requests`)
- `json` (built-in, no installation needed)
- `csv` (built-in, no installation needed)

- `FortiOS 7.4`
- `FortiOS API User` [Fortinet FortiGate REST API Administrator Guide](https://docs.fortinet.com/document/fortigate/7.4.8/administration-guide/399023/rest-api-administrator)

## Installation

To install the required external libraries, run:

```bash
pip install requests urllib3
```

## Run

```bash
python fos_inline-casb_app_list.py
```

## Output

Default csv file created
`casb_output.csv`
