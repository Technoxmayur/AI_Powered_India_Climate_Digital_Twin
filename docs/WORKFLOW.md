# Workflow

```text
Problem definition
      |
National data acquisition (IMD + MOSDAC/INSAT)
      |
Quality checks + spatial/temporal harmonization
      |
Feature engineering / lag windows
      |
PyTorch forecasting model
      |
Digital-twin state update
      +------------------+
      |                  |
Forecast map       What-if scenarios
      |                  |
      +--------> Dashboard
```
