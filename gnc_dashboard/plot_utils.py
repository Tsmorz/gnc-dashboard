#!/usr/bin/env python

import threading
import serial

import numpy as np
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go

from data_utils import generate_data
from serial_utils import read_serial_data, find_serial_port_name
from definitions import BAUD_RATE, SERIAL_PORT_TIMEOUT

# Initialize Dash app
app = dash.Dash(__name__)

UPDATE_RATE = 1000

# Create a thread-safe list to hold incoming data
data_list = []
data_lock = threading.Lock()


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
        margin={"r": 10, "t": 10, "l": 10, "b": 0},
        showlegend=False,
        coloraxis_showscale=False,
    )
    return fig


def draw_orientation(fig, position, rotation):
    x, y, z = position
    for i in range(3):

        fig.add_trace(
            go.Scatter3d(
                x=[x, rotation[0, i] + x],
                y=[y, rotation[1, i] + y],
                z=[z, rotation[2, i] + z],
                mode="lines",
            )
        )
    return None


def create_3d_figure(time, x, y, z):
    fig = go.Figure()
    fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode="lines", marker=dict(size=4)))

    draw_orientation(fig, position=np.array([x[-1], y[-1], z[-1]]), rotation=np.eye(3))

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
    return fig


# Define callback to update figures
@app.callback(
    [Output("map-plot", "figure"), Output("3d-plot", "figure")],
    [Input("interval-component", "n_intervals")],
)
def update_plots(n_intervals):
    # if data_list:
    print(data_list)
    data_list = []
    with data_lock:
        # Generate new data
        map_data, time, x, y, z = generate_data()

        # Update figures with new data
        map_fig = create_map_figure(map_data)
        plot_3d_fig = create_3d_figure(time, x, y, z)

        return map_fig, plot_3d_fig
    # else:
    #     return px.scatter(), px.scatter()


def run_pipeline():
    serial_port_name = find_serial_port_name()
    serial_port = serial.Serial(
        serial_port_name, BAUD_RATE, timeout=SERIAL_PORT_TIMEOUT
    )

    threading.Thread(target=read_serial_data(serial_port), daemon=True).start()

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
