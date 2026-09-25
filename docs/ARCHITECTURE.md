# Architecture

National observations -> adapters -> validation -> temporal/spatial harmonization
-> feature engineering -> PyTorch predictor -> digital-twin state
-> forecast + what-if scenario -> Streamlit geospatial dashboard.

The PoC uses a compact point/grid-cell forecasting baseline so it is feasible on
a laptop. National deployment can replace this with ConvLSTM, Fourier Neural
Operator, graph neural network, or diffusion/super-resolution models and a
distributed object store/feature store.
