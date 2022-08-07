"""Oregon Spotted Frog
https://github.com/rfordatascience/tidytuesday/tree/master/data/2022/2022-08-02
"""
import pandas as pd
import plotly.express as px

pandas_options: dict = {"display.max_rows": None, "display.max_columns": None}
for option, value in pandas_options.items():
    pd.set_option(option, value)


def main(data_path: str) -> None:
    df: pd.DataFrame = read_and_prep(url=data_path)

    # WEEKDAY COMPARISONS
    comparison_vars: dict = {"Female": None, "HabType": None, "Water": None, "Type": None, "Detection": None}
    comparison_mapping: dict = {var: compare_weekday(frame=df, to=var) for var in comparison_vars}

    for var, frame in comparison_mapping.items():
        make_bar_plot(frame=frame, var=var)


def read_and_prep(url: str) -> pd.DataFrame:
    """"""
    frame: pd.DataFrame = pd.read_csv(filepath_or_buffer=url, low_memory=False, encoding="utf-8",
                                      parse_dates=["SurveyDate"])
    frame["weekday"] = frame["SurveyDate"].dt.day_name()
    frame["Female"] = frame["Female"].replace({0.0: "Male", 1.0: "Female"})
    return frame


def compare_weekday(frame: pd.DataFrame, to: str) -> pd.DataFrame:
    """"""
    return frame.groupby(["weekday", to])[to].count().to_frame("count").reset_index()


def make_bar_plot(frame: pd.DataFrame, var: str) -> None:
    """"""
    fig = px.bar(frame, x="weekday", y="count", color=var, barmode="group",
                 title=f"Comparison of Weekday to {var.title()}",
                 labels={"weekday": "Weekday", "count": f"Count of {var}"}, text_auto=True, color_discrete_sequence= px.colors.sequential.Plasma_r)
    fig.show()


if __name__ == "__main__":
    csv_path: str = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2022/2022-08-02/frogs.csv"
    main(data_path=csv_path)
