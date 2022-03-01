from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA
import pandas as pd
from bokeh.models import ColumnDataSource
from bokeh.transform import factor_cmap
from bokeh import plotting

def cluster(df, cols, distance_threshold=0.2, linkage='ward'):
    train_data = df[cols]
    agglo = AgglomerativeClustering(distance_threshold=distance_threshold, n_clusters=None, linkage=linkage)
    agglo.fit(train_data)
    df['labels'] = [str(l) for l in agglo.labels_]
    print(f"{len(df['labels'].unique())} clusters at distance {distance_threshold}")
    return df

def pca(df, cols):
    train_data = df[cols]
    pca = PCA(n_components=2)
    crds = pca.fit_transform(train_data)
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
    from sugarrush.process_data import process_data, process_folder

    mass_list = load_mass_list()
    folder_path = str(Path(__file__).parents[1]) + '/data/01Mar22'
    cols = list(mass_list.keys())  # ['1', '2', '3', '4', '5', '6', '7', '8']
    distance_threshold = 0.2
    linkage = 'ward'

    prefix = ""
    df = process_folder(folder_path, mass_list, remove_prefix=prefix)
    df = cluster(df, cols, distance_threshold=distance_threshold, linkage=linkage)

    Path(f"{folder_path}/result").mkdir(parents=True, exist_ok=True)
    df.to_excel(f"{folder_path}/result/processed_results.xlsx")
