# -*- coding: utf-8 -*-
#

# Imports
import torch
import numpy as np
# from echotorch.nn.conceptors import Conceptor
import matplotlib.pyplot as plt


# Show singular values increasing aperture
def show_sv_for_increasing_aperture(conceptor, factor, title):
    """
    Show singular values for increasing aperture
    :param conceptors:
    :param factor:
    :param title:
    :return:
    """
    # Fig
    fig = plt.figure()
    ax = fig.gca()
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 1.5)
    ax.grid(True)

    # For each aperture multiplication
    for i in range(5):
        # Compute SVD
        _, S, _ = torch.svd(conceptor.get_C())

        # Plot
        ax.plot(S.numpy(), '--')

        # Multiply all conceptor's aperture by 10
        conceptor.multiply_aperture(factor)
    # end for

    # Show
    ax.set_xlabel(u"Singular values")
    ax.set_title(title)
    plt.show()
    plt.close()
# end show_sv_for_increasing_aperture


# Show similarity matrix
def show_similarity_matrix(sim_matrix, title):
    """
    Show similarity matrix
    :param sim_matrix:
    :return:
    """
    # Show similarity matrices
    fig, ax = plt.subplots(figsize=(8, 8))
    cax = ax.matshow(sim_matrix, interpolation='nearest', cmap='Greys_r')
    plt.title(title)
    fig.colorbar(cax, ticks=np.arange(0.1, 1.1, 0.1))
    for (i, j), z in np.ndenumerate(sim_matrix):
        if (i < 2 and j < 2) or (i > 1 and j > 1):
            plt.text(j, i, '{:0.2f}'.format(z), ha='center', va='center')
        else:
            plt.text(j, i, '{:0.2f}'.format(z), ha='center', va='center', color='white')
        # end if
    # end for
    plt.show()
# end show_similarity_matrix


# Plot singular values
def plot_singular_values(stats, title, xmin, xmax, ymin, ymax, log=False):
    """
    Plot singular values
    :param stats:
    :param title:
    :param timestep:
    :param start:
    :return:
    """
    # Compute R (correlation matrix)
    R = stats.t().mm(stats) / stats.shape[0]

    # Compute singular values
    U, S, V = torch.svd(R)
    singular_values = S

    # Compute singular values
    if log:
        singular_values = np.log10(singular_values)
    # end if

    # Fig
    fig = plt.figure()
    ax = fig.gca()
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.grid(True)

    # For each plot
    ax.plot(singular_values.numpy(), '--o')

    ax.set_xlabel("Timesteps")
    ax.set_title(title)
    plt.show()
    plt.close()

    return singular_values, U
# end plot_singular_values


# Display neurons activities on a 3D plot
def neurons_activities_3d(stats, neurons, title, timesteps=-1, start=0):
    """
    Display neurons activities on a 3D plot
    :param stats:
    :param neurons:
    :param title:
    :param timesteps:
    :param start:
    :return:
    """
    # Fig
    ax = plt.axes(projection='3d')

    # Two by two
    n_neurons = neurons.shape[0]
    stats = stats[:, neurons].view(-1, n_neurons // 3, 3)

    # Plot
    if timesteps == -1:
        time_length = stats.shape[0]
        ax.plot3D(stats[:, :, 0].view(time_length).numpy(), stats[:, :, 1].view(time_length).numpy(), stats[:, :, 2].view(time_length).numpy(), 'o')
    else:
        ax.plot3D(stats[start:start + timesteps, :, 0].numpy(), stats[start:start + timesteps, :, 1].numpy(), stats[start:start + timesteps, :, 2].numpy(), 'o', lw=0.5)
    # end if
    ax.set_xlabel("X Axis")
    ax.set_ylabel("Y Axis")
    ax.set_zlabel("Z Axis")
    ax.set_title(title)
    plt.show()
    plt.close()
# end neurons_activities_3d


# Display neurons activities on a 2D plot
def neurons_activities_2d(stats, neurons, title, colors, timesteps=-1, start=0):
    """
    Display neurons activities on a 2D plot
    :param stats:
    :param neurons:
    :param title:
    :param timesteps:
    :param start:
    :return:
    """
    # Fig
    fig = plt.figure()
    ax = fig.gca()

    # Two by two
    n_neurons = neurons.shape[0]

    # For each plot
    for i, stat in enumerate(stats):
        # Stats
        stat = stat[:, neurons].view(-1, n_neurons // 2, 2)

        # Plot
        if timesteps == -1:
            ax.plot(stat[:, :, 0].numpy(), stat[:, :, 1].numpy(), colors[i])
        else:
            ax.plot(stat[start:start + timesteps, :, 0].numpy(), stat[start:start + timesteps, :, 1].numpy(), colors[i])
        # end if
    # end for
    ax.set_xlabel("X Axis")
    ax.set_ylabel("Y Axis")
    ax.set_title(title)
    plt.show()
    plt.close()
# end neurons_activities_2d


# Display neurons activities
def neurons_activities_1d(stats, neurons, title, colors, xmin, xmax, ymin, ymax, timesteps=-1, start=0):
    """
    Display neurons activities
    :param stats:
    :param neurons:
    :return:
    """
    # Fig
    fig = plt.figure()
    ax = fig.gca()
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.grid(True)

    # For each neurons
    for i, n in enumerate(neurons):
        if timesteps == -1:
            ax.plot(stats[:, n].numpy(), colors[i])
        else:
            ax.plot(stats[start:start + timesteps, n].numpy(), colors[i])
        # end if
    # end for

    ax.set_xlabel("Timesteps")
    ax.set_title(title)
    plt.show()
    plt.close()
# end neurons_activities_1d


# Show 3D time series
def show_3d_timeseries(ts, title):
    """
    Show 3D timeseries
    :param axis:
    :param title:
    :return:
    """
    # Fig
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    ax.plot(ts[:, 0].numpy(), ts[:, 1].numpy(), ts[:, 2].numpy(), lw=0.5)
    ax.set_xlabel("X Axis")
    ax.set_ylabel("Y Axis")
    ax.set_zlabel("Z Axis")
    ax.set_title(title)
    plt.show()
    plt.close()
# end show_3d_timeseries


# Show 2D time series
def show_2d_timeseries(ts, title):
    """
    Show 2D timeseries
    :param ts:
    :param title:
    :return:
    """
    # Fig
    fig = plt.figure()
    ax = fig.gca()

    ax.plot(ts[:, 0].numpy(), ts[:, 1].numpy(), lw=0.5)
    ax.set_xlabel("X Axis")
    ax.set_ylabel("Y Axis")
    ax.set_title(title)
    plt.show()
    plt.close()
# end show_2d_timeseries


# Show 1D time series
def show_1d_timeseries(ts, title, xmin, xmax, ymin, ymax, start=0, timesteps=-1):
    """
    Show 1D time series
    :param ts:
    :param title:
    :return:
    """
    # Fig
    fig = plt.figure()
    ax = fig.gca()
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.grid(True)

    if timesteps == -1:
        ax.plot(ts[:, 0].numpy())
    else:
        ax.plot(ts[start:start+timesteps, 0].numpy())
    # end if
    ax.set_xlabel("X Axis")
    ax.set_title(title)
    plt.show()
    plt.close()
# end show_1d_timeseries
