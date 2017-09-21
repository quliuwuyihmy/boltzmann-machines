from copy import deepcopy

from hdm.utils import RNG


class SeedMixin(object):
    def __init__(self, random_seed=None):
        self.random_seed = random_seed
        self._rng = RNG(seed=self.random_seed)

    def make_random_seed(self):
        return self._rng.randint(2 ** 31 - 1)


def is_param_name(name):
    return not name.startswith('_') and not name.endswith('_')


class BaseModel(SeedMixin):
    def __init__(self, random_seed=None, *args, **kwargs):
        super(BaseModel, self).__init__(random_seed=random_seed)

    def get_params(self, deep=True):
        """Get parameters of the model.

        Parameters
        ----------
        deep : bool, optional
            Whether to deepcopy all the parameters.

        Returns
        -------
        params : dict
            Parameters of the model.
        """
        params = vars(self)
        params = {key: params[key] for key in params if is_param_name(key)}
        if deep:
            params = deepcopy(params)
        return params

    def set_params(self, **params):
        """Set parameters of the model.

        Parameters
        ----------
        params : kwargs
            Parameters names and their new values.

        Returns
        -------
        self
        """
        for key, value in params.items():
            if is_param_name(key) and hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError("invalid param name '{0}'".format(key))
        return self