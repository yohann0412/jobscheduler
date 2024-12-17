import numpy as np
import time
from typing import Dict, Any, List
from dataclasses import dataclass, field

@dataclass
class Particle:
    """
    Represents a single particle in molecular dynamics simulation
    """
    position: np.ndarray = field(default_factory=lambda: np.zeros(3))
    velocity: np.ndarray = field(default_factory=lambda: np.zeros(3))
    mass: float = 1.0
    charge: float = 0.0

class MolecularDynamicsSimulation:
    """
    Parallel molecular dynamics simulation implementation
    """
    def __init__(self, num_particles: int = 1000, box_dimensions: List[float] = None):
        self.num_particles = num_particles
        self.box_dimensions = box_dimensions or [100, 100, 100]
        self.particles = self._initialize_particles()
    
    def _initialize_particles(self) -> List[Particle]:
        """
        Randomly initialize particle positions and velocities
        """
        particles = []
        for _ in range(self.num_particles):
            particle = Particle(
                position=np.random.uniform(0, self.box_dimensions, 3),
                velocity=np.random.normal(0, 1, 3),
                mass=np.random.uniform(1.0, 2.0),
                charge=np.random.choice([-1, 1]) * np.random.uniform(0.1, 1.0)
            )
            particles.append(particle)
        return particles
    
    def lennard_jones_potential(self, r: float, epsilon: float = 1.0, sigma: float = 1.0) -> float:
        """
        Calculate Lennard-Jones potential between two particles
        """
        return 4 * epsilon * ((sigma/r)**12 - (sigma/r)**6)
    
    def compute_forces(self) -> np.ndarray:
        """
        Compute inter-particle forces using Lennard-Jones potential
        """
        forces = np.zeros((self.num_particles, 3))
        
        for i in range(self.num_particles):
            for j in range(i+1, self.num_particles):
                r_vec = self.particles[i].position - self.particles[j].position
                r_magnitude = np.linalg.norm(r_vec)
                
                # Apply periodic boundary conditions
                r_vec = np.mod(r_vec, self.box_dimensions)
                
                force_magnitude = -self.lennard_jones_potential(r_magnitude)
                force = force_magnitude * r_vec / r_magnitude
                
                forces[i] += force
                forces[j] -= force
        
        return forces
    
    def update_particles(self, forces: np.ndarray, dt: float = 0.01):
        """
        Update particle positions and velocities using Verlet integration
        """
        for i in range(self.num_particles):
            acceleration = forces[i] / self.particles[i].mass
            
            # Update position
            self.particles[i].position += (
                self.particles[i].velocity * dt + 
                0.5 * acceleration * dt**2
            )
            
            # Update velocity
            self.particles[i].velocity += acceleration * dt
            
            # Apply periodic boundary conditions
            self.particles[i].position %= self.box_dimensions
    
    def run_simulation(self, steps: int = 1000) -> Dict[str, Any]:
        """
        Run complete molecular dynamics simulation
        """
        simulation_data = {
            'total_energy': [],
            'temperature': [],
            'final_particle_states': []
        }
        
        for _ in range(steps):
            forces = self.compute_forces()
            self.update_particles(forces)
            
            # Optional: collect simulation metrics
            total_kinetic_energy = sum(
                0.5 * p.mass * np.linalg.norm(p.velocity)**2 
                for p in self.particles
            )
            simulation_data['total_energy'].append(total_kinetic_energy)
            
            # Compute instantaneous temperature
            temperature = total_kinetic_energy / (1.5 * self.num_particles)
            simulation_data['temperature'].append(temperature)
        
        # Store final particle states
        simulation_data['final_particle_states'] = [
            {
                'position': p.position.tolist(),
                'velocity': p.velocity.tolist(),
                'mass': p.mass,
                'charge': p.charge
            } for p in self.particles
        ]
        
        return simulation_data

def run_molecular_dynamics_job(job: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entry point for molecular dynamics job processing
    """
    simulation_params = job.get('simulation_parameters', {})
    
    simulation = MolecularDynamicsSimulation(
        num_particles=simulation_params.get('num_particles', 1000),
        box_dimensions=simulation_params.get('box_dimensions', [100, 100, 100])
    )
    
    start_time = time.time()
    result = simulation.run_simulation(
        steps=simulation_params.get('simulation_steps', 1000)
    )
    end_time = time.time()
    
    return {
        'job_id': job['id'],
        'simulation_result': result,
        'execution_time': end_time - start_time,
        'status': 'COMPLETED'
    }