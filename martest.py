import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    slider = mo.ui.slider(
        start=0,
        stop=100,
        step=1,
        value=50,
    )

    slider
    return (slider,)


@app.cell
def _(slider):
    slider.value
    return


if __name__ == "__main__":
    app.run()
