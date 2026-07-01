import marimo

__generated_with = "0.23.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    return mo, np, plt


@app.cell
def _(a, np):
    x  = np.arange(0, 10, 0.01)
    y1 = np.sin(a.value * x)
    y2 = np.cos(a.value * x)
    return x, y1, y2


@app.cell
def _(mo):
    a = mo.ui.slider(start = 1, stop = 20, step = 1)
    return (a,)


@app.cell
def _(a, mo):
    mo.md(f"$a$ : {a} {a.value}")
    return


@app.cell
def _(a, plt, x, y1, y2):
    def plot(): 
    
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(x, y1, label = f'$\\sin({a.value}x)$', color=(0.5, 0.2, 0))
        ax.plot(x, y2, label = f'$\\cos({a.value}x)$', color=(0.2, 0.2, 0.7))
        ax.set_xlabel('$x$')
        ax.set_ylabel('y')
        ax.legend(loc = 'upper right')
        ax.grid()

        return fig

    return (plot,)


@app.cell
def _(plot):
    plot()
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
