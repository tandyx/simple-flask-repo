import io
import base64
import sqlite3

import pandas as pd
import matplotlib.pyplot as mpl
from flask import Flask, render_template, request

# given a manager_id, find the manager first and last name

app = Flask(__name__)


@app.route("/")
def index() -> None:
    """this is the homepage route"""
    return render_template("index.html")


@app.route("/report")
def report() -> None:
    """report route, access by going to localhost:5000/report"""
    dataframe = get_df("SELECT * FROM product")
    summary = dataframe[["product_price", "product_inventory"]].describe()
    return render_template(
        "report.html", data=dataframe.to_html(index=False), summary=summary.to_html()
    )


@app.route("/chart")
def chart():
    """chart route, access by going to localhost:5000/chart"""
    dataframe = get_df("SELECT product_name, product_price FROM product")
    plot = dataframe.plot(
        kind="bar",
        x="product_name",
        xlabel="product_name",
        title="product prices",
        ylabel="product prices",
    )
    plot_decoded = fig_to_base64(plot.figure).decode("utf-8")
    return render_template("chart.html", plot_img=plot_decoded)


def get_df(query: str, db_path: str = "retail_app.db") -> pd.DataFrame:
    """gets a dataframe from sqlite database

    args:
        - query (str)
        - db_path (str): relative path to db, default is 'retail_app.db'
    returns:
        DataFrame
    """
    conn = sqlite3.connect(db_path)
    dataframe = pd.read_sql_query(query, con=conn)
    conn.close()
    return dataframe


def fig_to_base64(fig: mpl.Figure) -> bytes:
    """converts a `Figure` to a base64 bytes (array?)

    args:
        - fig (Figure)
    returns:
    """
    img = io.BytesIO()
    fig.savefig(img, format="png", bbox_inches="tight")
    img.seek(0)
    return base64.b64encode(img.getvalue())


if __name__ == "__main__":
    app.run(debug=True)
