def doctor_explain(medicine, forecast, weather, outbreak):

    return f"""
As a clinical AI assistant:

The predicted demand for {medicine} has increased due to multiple factors:

- Weather condition impact: {weather}
- Disease outbreak pressure: {outbreak}
- Current forecast demand: {forecast:.2f}

Clinical interpretation:
This suggests higher patient inflow risk, especially for respiratory and infectious conditions.

Recommendation:
Ensure adequate stock and prepare emergency buffer supply.
"""