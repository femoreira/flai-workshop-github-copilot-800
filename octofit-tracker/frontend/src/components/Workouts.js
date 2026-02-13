import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/workouts/`;
    console.log('Workouts API Endpoint:', apiUrl);

    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Workouts - Fetched data:', data);
        // Handle both paginated (.results) and plain array responses
        const workoutsData = data.results || data;
        console.log('Workouts - Processed data:', workoutsData);
        setWorkouts(Array.isArray(workoutsData) ? workoutsData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Workouts - Error fetching data:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  const getDifficultyBadge = (difficulty) => {
    const classes = {
      'beginner': 'badge-custom difficulty-beginner',
      'intermediate': 'badge-custom difficulty-intermediate',
      'advanced': 'badge-custom difficulty-advanced'
    };
    return classes[difficulty?.toLowerCase()] || 'badge bg-secondary badge-custom';
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
            <h4 className="alert-heading">Error Loading Workouts</h4>
            <p>{error}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <div className="page-header">
        <h2>Workouts</h2>
      </div>
      
      <div className="row">
        {workouts.length > 0 ? (
          workouts.map((workout, index) => (
            <div key={workout._id || `workout-${index}`} className="col-md-6 col-lg-4 mb-4">
              <div className="card custom-card">
                <div className="card-header">
                  💪 {workout.name || workout.title}
                </div>
                <div className="card-body">
                  <p className="card-text">{workout.description || 'No description available'}</p>
                  <ul className="list-group list-group-flush mt-3">
                    <li className="list-group-item">
                      <strong>Category:</strong>
                      <span className="badge bg-primary ms-2">
                        {workout.category || workout.workout_type || workout.type || 'N/A'}
                      </span>
                    </li>
                    <li className="list-group-item">
                      <strong>Duration:</strong>
                      <span className="ms-2">{workout.duration} minutes</span>
                    </li>
                    <li className="list-group-item">
                      <strong>Difficulty:</strong>
                      <span className={`ms-2 ${getDifficultyBadge(workout.difficulty)}`}>
                        {workout.difficulty || 'N/A'}
                      </span>
                    </li>
                    {workout.exercises && workout.exercises.length > 0 && (
                      <li className="list-group-item">
                        <strong>Exercises:</strong>
                        <span className="badge bg-info ms-2">
                          {workout.exercises.length} exercises
                        </span>
                        <div className="mt-2">
                          <ol className="mb-0" style={{fontSize: '0.875rem'}}>
                            {workout.exercises.map((exercise, idx) => (
                              <li key={idx} className="mb-1">
                                <strong>{exercise.name}</strong>
                                {exercise.sets && ` - ${exercise.sets} sets`}
                                {exercise.reps && ` × ${exercise.reps} reps`}
                                {exercise.duration && ` - ${exercise.duration}`}
                                {exercise.distance && ` - ${exercise.distance}`}
                              </li>
                            ))}
                          </ol>
                        </div>
                      </li>
                    )}
                  </ul>
                </div>
                <div className="card-footer bg-transparent border-0">
                  <button className="btn btn-sm btn-outline-primary w-100">Start Workout</button>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="col-12">
            <div className="text-center text-muted py-5">
              <i className="bi bi-lightning" style={{fontSize: '3rem'}}></i>
              <p className="mt-3">No workouts found</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Workouts;
