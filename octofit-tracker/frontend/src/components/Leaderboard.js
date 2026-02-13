import React, { useState, useEffect } from 'react';

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/leaderboard/`;
    console.log('Leaderboard API Endpoint:', apiUrl);

    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Leaderboard - Fetched data:', data);
        // Handle both paginated (.results) and plain array responses
        const leaderboardData = data.results || data;
        console.log('Leaderboard - Processed data:', leaderboardData);
        setLeaderboard(Array.isArray(leaderboardData) ? leaderboardData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Leaderboard - Error fetching data:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  const getRankBadgeClass = (index) => {
    if (index === 0) return 'rank-badge rank-1';
    if (index === 1) return 'rank-badge rank-2';
    if (index === 2) return 'rank-badge rank-3';
    return 'rank-badge rank-other';
  };

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
            <h4 className="alert-heading">Error Loading Leaderboard</h4>
            <p>{error}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <div className="page-header">
        <h2>Leaderboard</h2>
      </div>
      
      <div className="table-container">
        <div className="d-flex justify-content-between align-items-center mb-3">
          <p className="text-muted mb-0">Compete with <strong>{leaderboard.length}</strong> athletes</p>
        </div>
        
        <div className="table-responsive">
          <table className="table table-hover align-middle">
            <thead>
              <tr>
                <th style={{width: '80px'}}>Rank</th>
                <th>User</th>
                <th>Team</th>
                <th className="text-center">Total Points</th>
                <th className="text-center">Total Activities</th>
              </tr>
            </thead>
            <tbody>
              {leaderboard.length > 0 ? (
                leaderboard.map((entry, index) => (
                  <tr key={entry._id || index}>
                    <td>
                      <div className={getRankBadgeClass(index)}>
                        {index + 1}
                      </div>
                    </td>
                    <td>
                      <strong>{entry.user_name || entry.user}</strong>
                    </td>
                    <td>
                      <span className="badge bg-info badge-custom">
                        👥 {entry.team_id === 'team_marvel' ? 'Team Marvel' : entry.team_id === 'team_dc' ? 'Team DC' : entry.team_id || 'N/A'}
                      </span>
                    </td>
                    <td className="text-center">
                      <span className="badge bg-danger badge-custom">
                        🏆 {entry.total_points || 0}
                      </span>
                    </td>
                    <td className="text-center">
                      <span className="badge bg-primary badge-custom">
                        📊 {entry.activities_count || entry.total_activities || 0}
                      </span>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="5" className="text-center text-muted py-5">
                    <div>
                      <i className="bi bi-trophy" style={{fontSize: '3rem'}}></i>
                      <p className="mt-3">No leaderboard data found</p>
                    </div>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Leaderboard;
