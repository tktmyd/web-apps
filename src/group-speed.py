import marimo

__generated_with = "0.23.11"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 群速度と位相速度
    """)
    return


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    return mo, np, plt


@app.cell
def _(np):
    π = np.pi

    T = 10
    f = 1/T
    ω = 2 * π * f
    λ = 40
    k = 2 * π / λ
    U = 3
    df = 1 / 25 / 2 
    dω = 2 * π * df
    dk = dω / U
    return dk, dω, k, ω


@app.cell
def _(dk, dω, k, np, plt, ω):
    def plot(x): 

        t = np.linspace(0, 300, 801)
        u0 = np.cos((k+dk/2) * x - (ω + dω/2) * t)
        u1 = np.cos((k-dk/2) * x - (ω - dω/2) * t)
        env = 2 * np.cos(dk/2 * x - dω/2 * t)

        fig = plt.figure(figsize=(12, 8))
        ax1 = fig.add_subplot(211)

        ax1.plot(t, u0, label=r"$u_1 = \sin [(k+\Delta k/2)x-(\omega+\Delta \omega/2) t]$", 
                 color=(68/255, 119/255, 170/255))
        ax1.plot(t, u1, label=r"$u_2 = \sin [(k-\Delta k/2)x-(\omega-\Delta \omega/2) t]$", 
                 color=(238/255, 102/255, 119/255))
        ax1.set_xlabel("time [s]")
        ax1.set_ylabel("amplitude")
        ax1.set_yticks(np.arange(-1., 1.01, 0.5))
        ax1.set_ylim(-1.2, 1.2)
        ax1.set_title(f"x = {x} km")
        ax1.legend(loc = 'upper right')

        ax2 = fig.add_subplot(212)
        ax2.plot(t, u0+u1, label=r"$u_1 + u_2$", color=(0, 153/255,136/255))
        ax2.plot(t, env, color='black')
        ax2.plot(t, -env, color='black')
        ax2.set_yticks(np.arange(-2, 2.01, 1))
        ax2.legend(loc="upper right")
        ax2.set_xlabel("time [s]")

        return fig

    return (plot,)


@app.cell
def _(mo):
    slider_x = mo.ui.slider(start=0, stop=1000, step=2, full_width=True)
    return (slider_x,)


@app.cell
def _(mo, slider_x):
    mo.md(f"x [km] {slider_x}")
    return


@app.cell
def _(plot, slider_x):
    plot(slider_x.value)
    return


@app.cell
def _(dk, dω, k, np, ω):
    z = np.zeros([1000, 800])
    x = np.linspace(0, 1000, 1001)
    t = np.linspace(0, 200, 801)

    for n in range(len(t)-1):
        for i in range(len(x)-1):
            u0 = np.cos((k+dk/2) * x[i] - (ω + dω/2) * t[n])
            u1 = np.cos((k-dk/2) * x[i] - (ω - dω/2) * t[n])
            z[i,n] = u0 + u1
    return t, x, z


@app.cell
def _(plt, t, x, z):
    def plot3d(): 
        fig = plt.figure(figsize=(6, 8))
        ax = fig.add_subplot(1, 1, 1)
    
        p = ax.pcolormesh(t,x, z, shading='auto', cmap='Blues')
        ax.set_xlabel("time [s]")
        ax.set_ylabel("distance [km]")
        fig.colorbar(p)

        return fig

    return (plot3d,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    時空間プロット
    """)
    return


@app.cell
def _(plot3d):
    plot3d()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
