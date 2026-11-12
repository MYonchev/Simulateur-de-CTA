import psychrolib
import matplotlib.pyplot as plt
import numpy as np

psychrolib.SetUnitSystem(psychrolib.SI)

pressure = 101325

t_array = np.arange(5, 45, 0.1)
rh_array = np.arange(0, 1.1, 0.1)
twb_array = np.arange(-10, 45, 5)


def draw_diagram(ax):
    """Trace le fond du diagramme psychrométrique."""
    # Courbes d'humidité relative constante
    for rh in rh_array:
        hr_array = [psychrolib.GetHumRatioFromRelHum(t, rh, pressure) for t in t_array]
        ax.plot(t_array, hr_array, 'k', linewidth=0.8)

    # Courbes de température humide constante
    for twb in twb_array:
        t_plot_array = [t for t in t_array if twb <= t]
        hr_array = [psychrolib.GetHumRatioFromTWetBulb(t, twb, pressure) for t in t_plot_array]
        ax.plot(t_plot_array, hr_array, 'b', linewidth=0.8)

    ax.set(
        ylim=(0, 0.025),
        xlim=(10, 40),
        ylabel=r"Humidité [$kg_{Eau}/kg_{airSec}$]",
        xlabel="Température sèche [°C]",
    )
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position("right")


def plot_point(ax, t_dry, rh=None, t_wet=None, label=None, color='r'):
    """
    Place un point sur le diagramme.

    - t_dry : température sèche [°C]
    - rh    : humidité relative (0 à 1)       -> l'un des deux
    - t_wet : température humide [°C]          -> ou l'autre
    """
    if rh is not None:
        hr = psychrolib.GetHumRatioFromRelHum(t_dry, rh, pressure)
    elif t_wet is not None:
        hr = psychrolib.GetHumRatioFromTWetBulb(t_dry, t_wet, pressure)
    else:
        raise ValueError("Il faut fournir rh ou t_wet.")

    ax.plot(t_dry, hr, 'o', color=color, markersize=8, zorder=5)

    if label:
        ax.annotate(
            label,
            xy=(t_dry, hr),
            xytext=(8, 8),
            textcoords='offset points',
            color=color,
            fontweight='bold',
        )
    return hr


if __name__ == "__main__":
    f, ax = plt.subplots()
    draw_diagram(ax)

    # Exemples d'utilisation
    plot_point(ax, 20, rh=0.1, label="Point A (20°C, 10%)")

    plt.tight_layout()
    plt.show()


""" pour la docu " pip freeze > requirements.txt "
    et apres "pip install -r requirements.txt" """
