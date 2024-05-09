const initialState = {
  loading: false,
  error: {},
  jobs: []
}

const reducer = (state = initialState, action) => {
  switch (action.type) {
    case 'JOB_FETCH':
      return {
        ...state,
        loading: true
      }
    case 'JOB_FETCH_ERROR':
      return {
        ...state,
        loading: false,
        error: action.error
      }
    case 'JOB_RETURN':
      return {
        ...state,
        loading: false,
        jobs: action.jobs
      }
    default:
      return state
  }
}

export default reducer;