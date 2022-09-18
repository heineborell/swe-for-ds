"""collect some samples"""


def collect_training_samples(n_samples):
    """get n training samples"""

    samples = []
    for i in range(n_samples):
        if i % 3 == 0:
            samples.append([1, 1, 1, 1])
        elif i % 3 == 1:
            samples.append([2, 2, 2, 2])
        elif i % 3 == 2:
            samples.append([3, 3, 3, 3])

    return samples


def collect_testing_samples(n_samples):
    """get n testing samples"""
    samples = []

    for i in range(n_samples):
        if i % 3 == 0:
            samples.append([0.5, 0.5, 0.5, 0.5])
        elif i % 3 == 1:
            samples.append([1.5, 1.5, 1.5, 1.5])
        elif i % 3 == 2:
            samples.append([2.5, 2.5, 2.5, 2.5])

    return samples


# REFACTOR 1
"""
def collect_training_samples(n_samples):
    samples = []
    for i in range(n_samples):
        samples.append([1 + i % 3]*4)
"""


# REFACTOR 2
"""
def collect_samples(n_samples, base):
    samples = []
    for i in range(n_samples):
        samples.append([base + i % 3]*4)

def collect_training_samples(n_samples):
    return collect_samples(n_samples, 1)

def collect_testing_samples(n_samples):
    return collect_samples(n_samples, 0.5)
"""


# REFACTOR 3
"""
def generate_sample(sample_number, base):
    return [base + sample_number % 3]*4


def collect_samples(n_samples, base):
    samples = []
    for i in range(n_samples):
        samples.append(generate_sample(i, base))

def collect_training_samples(n_samples):
    return collect_samples(n_samples, 1)

def collect_testing_samples(n_samples):
    return collect_samples(n_samples, 0.5)
"""

# REFACTOR 4
"""
def collect_samples(n_samples, base):
    return [generate_sample(i, base) for i in range(n_samples)]
"""
