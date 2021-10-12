import json
import plotly
import plotly.express as px


def oneStatAllJobsGraph(df, stat):
    """Return json datas for a graph that compare one given stat between each jobs"""

    # Build a sub dataFrame from the original dataFrame (df)
    data_subset = df.groupby(["Job", "Role"])[stat]\
        .mean()\
        .sort_index(level=[1, 0], ascending=[True, True])

    # Build the graph
    fig = px.bar(data_subset,
                 x=data_subset.index.get_level_values(0),
                 y=stat,
                 color=data_subset.index.get_level_values(1),
                 labels={
                     "x": "Job",
                     stat: f"{stat} Moyen",
                     "color": "Role"
                 })

    # Return Json version of the graph
    return json.dumps(fig,
                      cls=plotly.utils.PlotlyJSONEncoder)


def oneStatAllJobOfRoleGraph(df, stat):
    """Return json datas for a graph that compare one given stat between each job of a role"""

    # Build a sub dataFrame from the original dataFrame (df)
    data_subset = df.groupby("Job")[stat]\
        .mean()\
        .sort_index(level=0, ascending=True)

    # Build the graph
    fig = px.bar(data_subset,
                 x=data_subset.index,
                 y=stat,
                 labels={
                     "x": "Job",
                     stat: f"{stat} Moyen",
                 })

    # Return Json version of the graph
    return json.dumps(fig,
                      cls=plotly.utils.PlotlyJSONEncoder)


def oneStatOneJobGraph(df, stat):
    """"""

    # Build a sub dataFrame from the original dataFrame (df)
    data_subset = df[["EncId", stat]]

    # Build the graph
    fig = px.line(data_subset,
                  x="EncId",
                  y=stat,
                  labels={
                      "EncId": "Encounter",
                      stat: f"{stat}",
                  })

    # Return Json version of the graph
    return json.dumps(fig,
                      cls=plotly.utils.PlotlyJSONEncoder)
