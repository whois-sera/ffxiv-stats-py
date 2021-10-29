import json
import plotly
import plotly.express as px
import pandas as pandas


def oneStatAllJobsGraph(df, stat):
    """Return json datas for a graph that compare one given stat between each jobs"""

    # Build a sub dataFrame from the original dataFrame (df)
    data_subset = df.groupby(["Job", "Role"])[stat]\
        .mean().round().astype(int)\
        .sort_index(level=[1, 0], ascending=[True, True])

    # Build the graph
    fig = px.bar(data_subset,
                 x=data_subset.index.get_level_values(0),
                 y=stat,
                 text=stat,
                 color=data_subset.index.get_level_values(1),
                 labels={
                     "x": "Job",
                     stat: f"{stat} Moyen",
                     "color": "Role",
                 })

    # Return Json version of the graph
    return fig


def oneStatAllJobOfRoleGraph(df, stat):
    """Return json datas for a graph that compare one given stat between each job of a role"""

    # Build a sub dataFrame from the original dataFrame (df)
    data_subset = df.groupby("Job")[stat]\
        .mean().round().astype(int)\
        .sort_index(level=0, ascending=True)

    # Build the graph
    fig = px.bar(data_subset,
                 x=data_subset.index,
                 y=stat,
                 text=stat,
                 labels={
                     "x": "Job",
                     stat: f"{stat} Moyen",
                 })

    # Return Json version of the graph
    return fig


def oneStatOneJobGraph(df, stat):
    """"""

    # Build a sub dataFrame from the original dataFrame (df)
    data_subset = df[["EncId", stat]]

    # Build the graph
    fig = px.line(data_subset,
                  x="EncId",
                  y=stat,
                  text=stat,
                  labels={
                      "EncId": "Encounter",
                      stat: f"{stat}",
                  })

    # Return Json version of the graph
    return fig


def playerJobCompare(df, stat, player):
    """"""

    job_mean = df[stat].mean()
    df = df[df['Name'].str.contains(player, case=False, regex=False)]
    player_mean = df[stat].mean().round().astype(int)

    d = {stat: [job_mean, player_mean]}
    ndf = pandas.DataFrame(
        data=d, index=["Moyenne du job", "Moyenne du joueur"])

    fig = px.bar(ndf,
                 x=ndf.index,
                 y=stat,
                 text=stat,
                 labels={
                     "x": "Job",
                     stat: f"{stat} Moyen",
                 })

    # Return Json version of the graph
    return fig


def getJsonVersion(fig):
    """"""

    return json.dumps(fig,
                      cls=plotly.utils.PlotlyJSONEncoder)
