import React, { useState, useEffect } from 'react';

function Teams() {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/teams/`;
    console.log('Teams API Endpoint:', apiUrl);

    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Teams - Fetched data:', data);
        // Handle both paginated (.results) and plain array responses
        const teamsData = data.results || data;
        console.log('Teams - Processed data:', teamsData);
        // Log individual team data for debugging
        if (Array.isArray(teamsData)) {
          teamsData.forEach((team, index) => {
            console.log(`Team ${index + 1} - Name: ${team.name}, Member Count: ${team.member_count}`);
          });
        }
        setTeams(Array.isArray(teamsData) ? teamsData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Teams - Error fetching data:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="container mt-4">
        <div className="loading-container">
          <div className="loading-spinner"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mt-4">
        <div className="error-container">
          <div className="alert alert-danger" role="alert">
            <h4 className="alert-heading">Error Loading Teams</h4>
            <p>{error}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <div className="page-header">
        <h2>Teams</h2>
      </div>
      
      <div className="row">
        {teams.length > 0 ? (
          teams.map(team => (
            <div key={team.id || team._id} className="col-md-6 col-lg-4 mb-4">
              <div className="card custom-card">
                <div className="card-header">
                  👥 {team.name}
                </div>
                <div className="card-body">
                  <p className="card-text">{team.description || 'No description available'}</p>
                  <ul className="list-group list-group-flush">
                    <li className="list-group-item">
                      <strong>Members:</strong>
                      <span className="badge bg-primary ms-2">
                        {typeof team.member_count !== 'undefined' ? team.member_count : (team.members?.length || 0)}
                      </span>
                    </li>
                    <li className="list-group-item">
                      <strong>Team ID:</strong>
                      <span className="ms-2 text-muted">{team._id || team.id || 'N/A'}</span>
                    </li>
                    <li className="list-group-item">
                      <strong>Created:</strong>
                      <span className="ms-2">{new Date(team.created_at).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })}</span>
                    </li>
                  </ul>
                </div>
                <div className="card-footer bg-transparent border-0">
                  <button className="btn btn-sm btn-outline-primary w-100">View Details</button>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="col-12">
            <div className="text-center text-muted py-5">
              <i className="bi bi-people" style={{fontSize: '3rem'}}></i>
              <p className="mt-3">No teams found</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Teams;
