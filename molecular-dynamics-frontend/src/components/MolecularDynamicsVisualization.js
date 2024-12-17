import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import { Atom } from 'lucide-react';

const MolecularDynamicsVisualization = ({ simulationResult }) => {
    const [activeView, setActiveView] = useState('energy');

    const renderEnergyChart = () => (
        <div className="bg-white p-4 rounded shadow">
            <h3 className="text-xl font-bold mb-4">Total Energy Over Simulation Steps</h3>
            <LineChart width={600} height={300} data={simulationResult.total_energy.map((energy, index) => ({ step: index, energy }))}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="step" label={{ value: 'Simulation Steps', position: 'insideBottom', offset: -5 }} />
                <YAxis label={{ value: 'Energy', angle: -90, position: 'insideLeft' }} />
                <Tooltip />
                <Line type="monotone" dataKey="energy" stroke="#8884d8" />
            </LineChart>
        </div>
    );

    const renderTemperatureChart = () => (
        <div className="bg-white p-4 rounded shadow">
            <h3 className="text-xl font-bold mb-4">Temperature Variation</h3>
            <LineChart width={600} height={300} data={simulationResult.temperature.map((temp, index) => ({ step: index, temperature: temp }))}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="step" label={{ value: 'Simulation Steps', position: 'insideBottom', offset: -5 }} />
                <YAxis label={{ value: 'Temperature (K)', angle: -90, position: 'insideLeft' }} />
                <Tooltip />
                <Line type="monotone" dataKey="temperature" stroke="#82ca9d" />
            </LineChart>
        </div>
    );

    const renderParticleDistribution = () => {
        const particles = simulationResult.final_particle_states;
        return (
            <div className="bg-white p-4 rounded shadow">
                <h3 className="text-xl font-bold mb-4">Final Particle Distribution</h3>
                <div className="flex justify-between">
                    <p>Total Particles: {particles.length}</p>
                    <p>Average Mass: {(particles.reduce((sum, p) => sum + p.mass, 0) / particles.length).toFixed(2)}</p>
                </div>
            </div>
        );
    };

    return (
        <div className="p-6">
            <div className="flex items-center mb-4">
                <Atom className="mr-2" />
                <h2 className="text-2xl font-bold">Molecular Dynamics Simulation Results</h2>
            </div>
            
            <div className="flex space-x-4 mb-4">
                <button 
                    className={`px-4 py-2 rounded ${activeView === 'energy' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
                    onClick={() => setActiveView('energy')}
                >
                    Energy
                </button>
                <button 
                    className={`px-4 py-2 rounded ${activeView === 'temperature' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
                    onClick={() => setActiveView('temperature')}
                >
                    Temperature
                </button>
                <button 
                    className={`px-4 py-2 rounded ${activeView === 'particles' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
                    onClick={() => setActiveView('particles')}
                >
                    Particle Distribution
                </button>
            </div>

            {activeView === 'energy' && renderEnergyChart()}
            {activeView === 'temperature' && renderTemperatureChart()}
            {activeView === 'particles' && renderParticleDistribution()}
        </div>
    );
};

export default MolecularDynamicsVisualization;