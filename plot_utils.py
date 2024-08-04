import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import time

# Initialize Dash app
app = dash.Dash(__name__)

boston_lat_lon = (42 + 19.5617980957031250 / 60, -71 - 7.4340000152587891 / 60)

UPDATE_RATE = 1000


# Sample data for the map and 3D plot
def generate_data():
    # Generate random data for the map
    num = 100
    map_data = pd.DataFrame(
        {
            "latitude": np.random.normal(loc=boston_lat_lon[0], scale=0.0001, size=num),
            "longitude": np.random.normal(
                loc=boston_lat_lon[1], scale=0.0001, size=num
            ),
            "color": np.linspace(0, 1, num),
        }
    )

    # Generate random data for the 3D plot
    # time = pd.date_range(start="2024-01-01", periods=num, freq="S")
    x = 5 * np.sin(np.linspace(time.time(), 4 * np.pi + time.time(), num))
    y = 5 * np.cos(np.linspace(time.time(), 4 * np.pi + time.time(), num))
    z = np.linspace(0, 10, num)
    return map_data, time, x, y, z


# Create initial figures
def create_map_figure(data):
    fig = px.scatter_mapbox(
        data,
        lat="latitude",
        lon="longitude",
        mapbox_style="carto-positron",
        center={
            "lat": data["latitude"].values[-1],
            "lon": data["longitude"].values[-1],
        },
        zoom=17,
        color="color",
        color_continuous_scale=px.colors.sequential.thermal,
    )
    fig.update_layout(
        margin={"r": 20, "t": 20, "l": 20, "b": 0},
        showlegend=False,
        coloraxis_showscale=False,
    )
    return fig


def create_3d_figure(time, x, y, z):
    fig = go.Figure()
    fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode="lines", marker=dict(size=4)))

    for i in range(3):
        axes = np.zeros((2, 3))
        axes[1, i] = 1
        fig.add_trace(
            go.Scatter3d(
                x=axes[:, 0] + x[-1],
                y=axes[:, 1] + y[-1],
                z=axes[:, 2] + z[-1],
                mode="lines",
            )
        )

    fig.update_layout(
        scene=dict(
            xaxis=dict(
                title="X Axis",
                # scaleanchor="y",  # Link x and y axis scaling
            ),
            yaxis=dict(
                title="Y Axis",
                # scaleanchor="z",  # Link y and z axis scaling
            ),
            zaxis=dict(
                title="Z Axis",
                # scaleanchor="x",  # Link z and x axis scaling
            ),
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        # title="3D Scatter Plot with Equal Aspect Ratio",
    )
    fig.update_layout(showlegend=False)
    # fig.update_traces(marker=dict(colorbar=dict(visible=False)))
    return fig


# Define callback to update figures
@app.callback(
    [Output("map-plot", "figure"), Output("3d-plot", "figure")],
    [Input("interval-component", "n_intervals")],
)
def update_plots(n_intervals):
    # Generate new data
    map_data, time, x, y, z = generate_data()

    # Update figures with new data
    map_fig = create_map_figure(map_data)
    plot_3d_fig = create_3d_figure(time, x, y, z)

    return map_fig, plot_3d_fig


def run_pipeline():
    # Initial data
    map_data, time, x, y, z = generate_data()

    # Create initial figures
    map_fig = create_map_figure(map_data)
    plot_3d_fig = create_3d_figure(time, x, y, z)

    # Define the layout of the app
    app.layout = html.Div(
        [
            html.Div(
                [
                    # html.H1("Dash Dashboard with Map and 3D Plot"),
                    # Map plot
                    html.Div(
                        dcc.Graph(
                            id="map-plot",
                            figure=map_fig,
                        ),
                        style={"flex": "1", "padding": "5px"},
                    ),
                    html.Div(
                        # 3D plot
                        dcc.Graph(
                            id="3d-plot",
                            figure=plot_3d_fig.update_layout(showlegend=False),
                        ),
                        style={"flex": "1", "padding": "5px"},
                    ),
                    # Interval component to trigger updates every second
                    dcc.Interval(
                        id="interval-component",
                        interval=UPDATE_RATE,  # Update every 1000 milliseconds (1 second)
                        n_intervals=0,
                    ),
                ],
                style={
                    "display": "flex",
                    "flex-direction": "row",
                },  # Use flexbox to align plots side by side
            )
        ]
    )

    app.run_server(debug=True)
    return


if __name__ == "__main__":
    run_pipeline()
