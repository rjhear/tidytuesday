"""Oregon Spotted Frog
https://github.com/rfordatascience/tidytuesday/tree/master/data/2022/2022-08-02
"""
import networkx as nx
import pandas as pd
import plotly.graph_objects as go


def main():
    dataset: str = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2022/2022-08-02/frogs.csv"
    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=dataset, low_memory=False, encoding="utf-8")
    df["Female"] = df["Female"].replace({0: "Male", 1: "Female"})
    df["Female_count"] = df["Female"].replace((df["Female"].value_counts().to_dict()))

    G = nx.from_pandas_edgelist(df=df, source=SOURCE, target=TARGET, edge_attr=True)
    print(G)
    # ['__class__', '__contains__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__',
    #  '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__',
    #  '__len__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__',
    #  '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_adj', '_node', 'add_edge', 'add_edges_from',
    #  'add_node', 'add_nodes_from', 'add_weighted_edges_from', 'adj', 'adjacency', 'adjlist_inner_dict_factory',
    #  'adjlist_outer_dict_factory', 'clear', 'clear_edges', 'copy', 'degree', 'edge_attr_dict_factory', 'edge_subgraph',
    #  'edges', 'get_edge_data', 'graph', 'graph_attr_dict_factory', 'has_edge', 'has_node', 'is_directed',
    #  'is_multigraph', 'name', 'nbunch_iter', 'neighbors', 'node_attr_dict_factory', 'node_dict_factory', 'nodes',
    #  'number_of_edges', 'number_of_nodes', 'order', 'remove_edge', 'remove_edges_from', 'remove_node',
    #  'remove_nodes_from', 'size', 'subgraph', 'to_directed', 'to_directed_class', 'to_undirected',
    #  'to_undirected_class', 'update']
    pos = nx.spring_layout(G, k=0.5, iterations=50)
    print(pos)

    for n, p in pos.items():
        G.nodes[n]["pos"] = p
    edge_trace = go.Scatter(x=[], y=[], line=dict(width=0.5, color="#888"), hoverinfo="none", mode="lines")

    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]["pos"]
        x1, y1 = G.nodes[edge[1]]["pos"]
        edge_trace["x"] += (x0, x1, None)
        edge_trace["y"] += (y0, y1, None)
    labels = [name for name in pos]
    node_trace = go.Scatter(x=[], y=[], text=[], textposition="top center", mode="lines+markers+text", hoverinfo="text",
                            marker=dict(showscale=True, colorscale="Blackbody", color=[], reversescale=True,
                                        size=[],
                                        colorbar=dict(thickness=10, title="Node Connections", xanchor="left",
                                                      titleside="right"), line=dict(width=0)))
    levels_female: set = set(df[SOURCE].unique())
    size: dict = {**df[SOURCE].value_counts().to_dict(), **df[TARGET].value_counts().to_dict()}
    for node in G.nodes():
        x, y = G.nodes[node]["pos"]
        node_trace["x"] += (x,)
        node_trace["y"] += (y,)
        node_trace["marker"]["color"] += ("red",) if node in levels_female else ("blue",)
        node_trace["marker"]["size"] += (size[node],)
        node_trace["text"] += (node,)
        print(node)
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(title="<br>Oregon Spotted Frog", titlefont=dict(size=16), showlegend=False,
                                     hovermode='closest', margin=dict(b=20, l=5, r=5, t=40),
                                     annotations=[dict(text="", showarrow=False, xref="paper", yref="paper")],
                                     xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                     yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
    # for i, e in pos.items():
    #     fig.add_annotation(x=e[0], y=e[1], text=f"<b>{i}</b>", showarrow=False, yshift=0)
    fig.show()


if __name__ == "__main__":
    # ['Site', 'Subsite', 'HabType', 'SurveyDate', 'Ordinal', 'Frequency', 'UTME_83', 'UTMN_83', 'Interval', 'Female',
    #  'Water', 'Type', 'Structure', 'Substrate', 'Beaver', 'Detection']
    SOURCE: str = "Detection"
    TARGET: str = "Substrate"
    main()
