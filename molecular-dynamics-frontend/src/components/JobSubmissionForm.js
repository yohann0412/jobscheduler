import React, { useState } from 'react';

const JobSubmissionForm = ({ onSubmit }) => {
  const [formData, setFormData] = useState({
    num_particles: 1000,
    simulation_steps: 1000,
    box_dimensions: [100, 100, 100]
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'box_dimensions' 
        ? value.split(',').map(Number) 
        : Number(value)
    }));
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white shadow rounded p-6">
      <div className="mb-4">
        <label className="block mb-2">Number of Particles</label>
        <input
          type="number"
          name="num_particles"
          value={formData.num_particles}
          onChange={handleChange}
          className="w-full p-2 border rounded"
        />
      </div>
      <div className="mb-4">
        <label className="block mb-2">Simulation Steps</label>
        <input
          type="number"
          name="simulation_steps"
          value={formData.simulation_steps}
          onChange={handleChange}
          className="w-full p-2 border rounded"
        />
      </div>
      <div className="mb-4">
        <label className="block mb-2">Box Dimensions (x,y,z)</label>
        <input
          type="text"
          name="box_dimensions"
          value={formData.box_dimensions.join(',')}
          onChange={handleChange}
          className="w-full p-2 border rounded"
        />
      </div>
      <button 
        type="submit" 
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Submit Molecular Dynamics Job
      </button>
    </form>
  );
};

export default JobSubmissionForm;