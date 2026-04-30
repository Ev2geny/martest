import marimo

__generated_with = "0.23.3"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return


@app.cell
def _():
    import os

    def runtime_environment() -> str:
        return os.environ.get("NOTEBOOK_RUNTIME", "local")

    return (runtime_environment,)


@app.cell
def _(runtime_environment):
    runtime = runtime_environment()

    runtime
    return


if __name__ == "__main__":
    app.run()
