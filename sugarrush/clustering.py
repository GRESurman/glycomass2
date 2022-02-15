from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA
import pandas as pd
from bokeh.models import ColumnDataSource
from bokeh.transform import factor_cmap
from bokeh import plotting

def cluster(df, mass_list, distance_threshold=0.1):
    train_cols = list(mass_list.keys())
    train_data = df[train_cols]

    agglo = AgglomerativeClustering(distance_threshold=distance_threshold, n_clusters=None)
    agglo.fit(train_data)
    labels = agglo.labels_
    labels = [str(l) for l in labels]
    df['labels'] = labels
    print(f"{len(df['labels'].unique())} clusters at distance {distance_threshold}")
    return df

def pca(df, mass_list):
    train_cols = list(mass_list.keys())
    train_data = df[train_cols]
    pca = PCA(n_components=2)
    crds = pca.fit_transform(train_data )
    pca_df = pd.DataFrame(crds, columns=["x", "y"])
    df[['x', 'y']] = pca_df[['x', 'y']]
    return df

def plot(df, title="PCA with clustering"):
    p = plotting.figure(plot_width=600, plot_height=500,
                            tools=['reset,box_zoom,wheel_zoom,zoom_in,zoom_out,pan,tap'],
                            title=title)

    source = ColumnDataSource(df)

    p.circle(x='x', y='y', size=10, source=source,
             color=factor_cmap('labels', 'Category10_10', df['labels'].unique()))

    return p

if __name__ == '__main__':
    from pathlib import Path
    from sugarrush.mass_list import load_mass_list
    from sugarrush.process_data import process_data
    from bokeh.plotting import output_file, save

    # load and process
    mass_list = load_mass_list()
    filepath = str(Path(__file__).parents[0]) + '/data/test_data.xlsx'
    df = process_data(filepath, mass_list)

    # cluster and plot
    distance_threshold = 0.05
    df = cluster(df, mass_list, distance_threshold=distance_threshold)
    df = pca(df, mass_list)
    p = plot(df, title=f"PCA with clustering at distance {distance_threshold}")

    # output plot to html file
    output_file(str(Path(__file__).parents[0]) + '/data/test_plot.html')
    save(p)

