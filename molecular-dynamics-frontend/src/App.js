import React, { useState, useEffect } from 'react';
import axios from 'axios';
import MolecularDynamicsVisualization from './components/MolecularDynamicsVisualization';
import JobSubmissionForm from './components/JobSubmissionForm';
import './App.css';
import './index.css';

function App() {
  const [jobs, setJobs] = useState([]);
  const [selectedJob, setSelectedJob] = useState(null);

  // Development backend URL
  const API_BASE_URL = process.env.NODE_ENV === 'production' 
    ? 'https://your-production-backend.com' 
    : 'http://localhost:8000';

  const submitJob = async (jobParameters) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/jobs`, {
        type: 'molecular_dynamics',
        simulation_parameters: jobParameters
      });
      
      // Fetch updated job list
      fetchJobs();
    } catch (error) {
      console.error('Job submission error:', error);
    }
  };

  const fetchJobs = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/jobs`);
      setJobs(response.data);
    } catch (error) {
      console.error('Fetching jobs error:', error);
    }
  };

  useEffect(() => {
    fetchJobs();
    // Poll for job updates every 5 seconds
    const interval = setInterval(fetchJobs, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Molecular Dynamics Job Scheduler</h1>
      
      <JobSubmissionForm onSubmit={submitJob} />
      
      <div className="mt-6">
        <h2 className="text-2xl font-semibold mb-4">Recent Jobs</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {jobs.map(job => (
            <div 
              key={job.id} 
              className="bg-white shadow rounded p-4 cursor-pointer"
              onClick={() => setSelectedJob(job)}
            >
              <h3 className="font-bold">Job {job.id}</h3>
              <p>Status: {job.status}</p>
              <p>Submitted: {new Date(job.submitted_at * 1000).toLocaleString()}</p>
            </div>
          ))}
        </div>
      </div>

      {selectedJob && selectedJob.type === 'molecular_dynamics' && (
        <MolecularDynamicsVisualization 
          simulationResult={selectedJob.simulation_result} 
        />
      )}
    </div>
  );
}

export default App;