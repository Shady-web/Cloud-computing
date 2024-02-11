import random

class CloudResource:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity

class Individual:
    def __init__(self, chromosome):
        self.chromosome = chromosome

    def calculate_fitness(self, resources, tasks):
        fitness = 0.0
        for i in range(len(self.chromosome)):
            resource_id = self.chromosome[i]
            task_requirement = tasks[i]
            resource_capacity = resources[resource_id].capacity
            fitness += task_requirement / resource_capacity
        return fitness

def initialize_population(population_size, task_count, resource_count):
    population = []
    for _ in range(population_size):
        chromosome = [random.randint(0, resource_count - 1) for _ in range(task_count)]
        individual = Individual(chromosome)
        population.append(individual)
    return population

def evolve(population, resources, tasks, mutation_rate=0.05, generations=100):
    for generation in range(generations):
        evaluate_fitness(population, resources, tasks)
        parents = select_parents(population)
        offspring = crossover(parents)
        mutate(offspring, mutation_rate)
        population = offspring

        # Add debugging information
        if population:
            best_individual = max(population, key=lambda ind: ind.calculate_fitness(resources, tasks))
            print(f"Generation {generation + 1}, Best Fitness: {best_individual.calculate_fitness(resources, tasks)}")
        else:
            print(f"Generation {generation + 1}, Population is empty!")

    if population:
        best_individual = max(population, key=lambda ind: ind.calculate_fitness(resources, tasks))
        return best_individual
    else:
        return None

def evaluate_fitness(population, resources, tasks):
    for individual in population:
        individual.calculate_fitness(resources, tasks)

def select_parents(population):
    # For simplicity, select parents based on their fitness (top 50%)
    sorted_population = sorted(population, key=lambda ind: ind.calculate_fitness(resources, tasks), reverse=True)
    selection_size = len(sorted_population) // 2
    return sorted_population[:selection_size]

def crossover(parents):
    offspring = []
    for _ in range(len(parents)):
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)
        crossover_point = random.randint(0, len(parent1.chromosome) - 1)
        child_chromosome = parent1.chromosome[:crossover_point] + parent2.chromosome[crossover_point:]
        offspring.append(Individual(child_chromosome))
    return offspring

def mutate(population, mutation_rate):
    for individual in population:
        if random.random() < mutation_rate:
            # For simplicity, swap two random genes
            gene1 = random.randint(0, len(individual.chromosome) - 1)
            gene2 = random.randint(0, len(individual.chromosome) - 1)
            individual.chromosome[gene1], individual.chromosome[gene2] = individual.chromosome[gene2], individual.chromosome[gene1]

if __name__ == "__main__":
    # Example usage
    resources = [CloudResource(0, 100.0), CloudResource(1, 150.0), CloudResource(2, 200.0)]
    tasks = [50.0, 75.0, 100.0]

    population_size = 50
    task_count = len(tasks)
    resource_count = len(resources)

    population = initialize_population(population_size, task_count, resource_count)
    best_individual = evolve(population, resources, tasks, mutation_rate=0.05, generations=100)

    if best_individual:
        # Display the best individual's resource allocation
        print("Best Resource Allocation:")
        for i, resource_id in enumerate(best_individual.chromosome):
            print(f"Task {i + 1} -> Resource {resource_id}")
    else:
        print("No valid solution found.")
