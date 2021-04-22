import json
import plotly.graph_objects as go
import numpy as np

def plot_path(fig, path_points, color='rgb(255, 0, 0)', mode='markers', text=''):
    if (path_points.size > 1):
        fig.add_trace(go.Scattermapbox(
                lat=path_points[0],
                lon=path_points[1],
                mode=mode,
                marker=go.scattermapbox.Marker(
                    size=10,
                    color=color,
                    opacity=0.7
                ),
                text=text,
                hoverinfo='text'
            ))

def update_layout(fig, title, center, zoom=13):
    mapbox_access_token = open("./.public").read()
    fig.update_layout(
        title=title,
        autosize=True,
        hovermode='closest',
        showlegend=False,
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=center[0],
                lon=center[1]
            ),
            pitch=0,
            zoom=13,
            style='light'
        ),
    )


if __name__ == '__main__':
    ride_no = 100

    with open('../gps-fluctuations/dump/dump_file_clean.json', 'r') as f:
        standard_points = np.transpose(np.array(json.load(f)[ride_no]))
    with open('../gps-fluctuations/dump/s2r_dump_file_clean.json', 'r') as f:
        s2r_points = np.transpose(np.array(json.load(f)[ride_no]))

    print(standard_points.shape, s2r_points.shape)
    print(standard_points.size, s2r_points.size)

    fig = go.Figure()

    plot_path(fig, standard_points)
    plot_path(fig, s2r_points, color='rgb(0, 0, 255)')

    update_layout(fig, 'Sample No. ' + str(ride_no), standard_points[:,int(standard_points.shape[1]/2)])
    
    fig.show()