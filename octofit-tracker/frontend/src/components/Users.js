import React, { useState, useEffect } from 'react';

function Users() {
  const [users, setUsers] = useState([]);
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showEditModal, setShowEditModal] = useState(false);
  const [editingUser, setEditingUser] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    team_id: '',
    role: ''
  });
  const [saveError, setSaveError] = useState(null);
  const [saveSuccess, setSaveSuccess] = useState(false);

  useEffect(() => {
    fetchUsers();
    fetchTeams();
  }, []);

  const fetchUsers = () => {
    const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/users/`;
    console.log('Users API Endpoint:', apiUrl);

    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Users - Fetched data:', data);
        const usersData = data.results || data;
        console.log('Users - Processed data:', usersData);
        setUsers(Array.isArray(usersData) ? usersData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Users - Error fetching data:', error);
        setError(error.message);
        setLoading(false);
      });
  };

  const fetchTeams = () => {
    const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/teams/`;
    fetch(apiUrl)
      .then(response => response.json())
      .then(data => {
        const teamsData = data.results || data;
        setTeams(Array.isArray(teamsData) ? teamsData : []);
      })
      .catch(error => {
        console.error('Error fetching teams:', error);
      });
  };

  const handleEditClick = (user) => {
    setEditingUser(user);
    setFormData({
      name: user.name || '',
      email: user.email || '',
      team_id: user.team_id || '',
      role: user.role || 'member'
    });
    setSaveError(null);
    setSaveSuccess(false);
    setShowEditModal(true);
  };

  const handleCloseModal = () => {
    setShowEditModal(false);
    setEditingUser(null);
    setSaveError(null);
    setSaveSuccess(false);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSaveUser = async (e) => {
    e.preventDefault();
    setSaveError(null);
    setSaveSuccess(false);

    const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/users/${editingUser._id}/`;
    
    try {
      const response = await fetch(apiUrl, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const updatedUser = await response.json();
      console.log('Updated user:', updatedUser);

      // Update the users list
      setUsers(users.map(user => 
        user._id === editingUser._id ? { ...user, ...updatedUser } : user
      ));

      setSaveSuccess(true);
      setTimeout(() => {
        handleCloseModal();
        fetchUsers(); // Refresh the list
      }, 1000);
    } catch (error) {
      console.error('Error saving user:', error);
      setSaveError(error.message);
    }
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
            <h4 className="alert-heading">Error Loading Users</h4>
            <p>{error}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <div className="page-header">
        <h2>Users</h2>
      </div>
      
      <div className="row">
        {users.length > 0 ? (
          users.map((user, index) => (
            <div key={user._id || index} className="col-md-6 col-lg-4 mb-4">
              <div className="card custom-card">
                <div className="card-header">
                  👤 {user.name || user.username || 'Unknown User'}
                </div>
                <div className="card-body">
                  <ul className="list-group list-group-flush">
                    <li className="list-group-item">
                      <strong>Name:</strong>
                      <span className="ms-2">{user.name || user.username || 'N/A'}</span>
                    </li>
                    <li className="list-group-item">
                      <strong>Username:</strong>
                      <span className="ms-2">{user.username || user.email?.split('@')[0] || 'N/A'}</span>
                    </li>
                    <li className="list-group-item">
                      <strong>Email:</strong>
                      <span className="ms-2">{user.email || 'N/A'}</span>
                    </li>
                    <li className="list-group-item">
                      <strong>Role:</strong>
                      <span className="badge bg-secondary ms-2">
                        {user.role || 'member'}
                      </span>
                    </li>
                    <li className="list-group-item">
                      <strong>Team:</strong>
                      <span className="badge bg-info ms-2">
                        {user.team_name || user.team_id || user.team || 'No team'}
                      </span>
                    </li>
                    <li className="list-group-item">
                      <strong>Points:</strong>
                      <span className="badge bg-warning ms-2">
                        {user.total_points || 0}
                      </span>
                    </li>
                    <li className="list-group-item">
                      <strong>Joined:</strong>
                      <span className="ms-2">
                        {new Date(user.date_joined || user.created_at).toLocaleDateString()}
                      </span>
                    </li>
                  </ul>
                </div>
                <div className="card-footer bg-transparent border-0">
                  <button 
                    className="btn btn-sm btn-primary w-100"
                    onClick={() => handleEditClick(user)}
                  >
                    ✏️ Edit User
                  </button>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="col-12">
            <div className="text-center text-muted py-5">
              <i className="bi bi-person" style={{fontSize: '3rem'}}></i>
              <p className="mt-3">No users found</p>
            </div>
          </div>
        )}
      </div>

      {/* Edit User Modal */}
      {showEditModal && (
        <div className="modal show d-block" style={{backgroundColor: 'rgba(0,0,0,0.5)'}}>
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Edit User Details</h5>
                <button 
                  type="button" 
                  className="btn-close" 
                  onClick={handleCloseModal}
                ></button>
              </div>
              <form onSubmit={handleSaveUser}>
                <div className="modal-body">
                  {saveError && (
                    <div className="alert alert-danger" role="alert">
                      {saveError}
                    </div>
                  )}
                  {saveSuccess && (
                    <div className="alert alert-success" role="alert">
                      User updated successfully!
                    </div>
                  )}
                  
                  <div className="mb-3">
                    <label htmlFor="name" className="form-label">Name</label>
                    <input
                      type="text"
                      className="form-control"
                      id="name"
                      name="name"
                      value={formData.name}
                      onChange={handleInputChange}
                      required
                    />
                  </div>

                  <div className="mb-3">
                    <label htmlFor="email" className="form-label">Email</label>
                    <input
                      type="email"
                      className="form-control"
                      id="email"
                      name="email"
                      value={formData.email}
                      onChange={handleInputChange}
                      required
                    />
                  </div>

                  <div className="mb-3">
                    <label htmlFor="team_id" className="form-label">Team</label>
                    <select
                      className="form-select"
                      id="team_id"
                      name="team_id"
                      value={formData.team_id}
                      onChange={handleInputChange}
                      required
                    >
                      <option value="">Select a team</option>
                      {teams.map(team => (
                        <option key={team._id} value={team._id}>
                          {team.name}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="mb-3">
                    <label htmlFor="role" className="form-label">Role</label>
                    <select
                      className="form-select"
                      id="role"
                      name="role"
                      value={formData.role}
                      onChange={handleInputChange}
                      required
                    >
                      <option value="member">Member</option>
                      <option value="leader">Leader</option>
                      <option value="admin">Admin</option>
                    </select>
                  </div>
                </div>
                <div className="modal-footer">
                  <button 
                    type="button" 
                    className="btn btn-secondary" 
                    onClick={handleCloseModal}
                  >
                    Cancel
                  </button>
                  <button 
                    type="submit" 
                    className="btn btn-primary"
                    disabled={saveSuccess}
                  >
                    {saveSuccess ? 'Saved!' : 'Save Changes'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Users;
