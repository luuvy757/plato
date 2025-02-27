"""
The registry for algorithms that contains framework-specific implementations.

Having a registry of all available classes is convenient for retrieving an instance
based on a configuration at run-time.
"""
import logging

from plato.config import Config

if hasattr(Config().trainer, "use_mindspore"):
    from plato.algorithms.mindspore import (
        fedavg as fedavg_mindspore,
        mistnet as mistnet_mindspore,
    )

    registered_algorithms = {
        "fedavg": fedavg_mindspore.Algorithm,
        "mistnet": mistnet_mindspore.Algorithm,
    }

elif hasattr(Config().trainer, "use_tensorflow"):
    from plato.algorithms.tensorflow import fedavg as fedavg_tensorflow

    registered_algorithms = {"fedavg": fedavg_tensorflow.Algorithm}
else:
    from plato.algorithms import fedavg, mistnet, fedavg_gan, split_learning

    registered_algorithms = {
        "fedavg": fedavg.Algorithm,
        "mistnet": mistnet.Algorithm,
        "fedavg_gan": fedavg_gan.Algorithm,
        "split_learning": split_learning.Algorithm,
    }


def get(trainer=None):
    """Get the algorithm with the provided type."""
    algorithm_type = Config().algorithm.type

    if algorithm_type in registered_algorithms:
        logging.info("Algorithm: %s", algorithm_type)
        registered_alg = registered_algorithms[algorithm_type](trainer)
        return registered_alg
    else:
        raise ValueError(f"No such algorithm: {algorithm_type}")
