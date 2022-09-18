"""collect some samples"""


def generate_sample(sample_number: int, base: float) -> list[float]:
    return [base + sample_number % 3] * 5


def collect_training_samples(n_samples: int) -> list[list[float]]:
    return collect_samples(n_samples, 1)


def collect_testing_samples(n_samples: int) -> list[list[float]]:
    return collect_samples(n_samples, 0.5)


def collect_samples(n_samples: int, base: float) -> list[list[float]]:
    return [generate_sample(i, base) for i in range(n_samples)]
