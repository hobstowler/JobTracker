export const getJobsForUser = (user_uuid) => (dispatch, state, _) => {
  dispatch({type: 'JOB_FETCH'})

  fetch(`/job?uuid=${user_uuid}`)
    .then(async response => {
      const hasJson = response.headers.get('content-type')?.includes('application/json')
      const json = hasJson ? await response.json() : null

      if (!response.ok) {
        let error = (json && json.error) || response.status
        dispatch({type: 'JOB_FETCH_ERROR', error: error})
        return
      }

      dispatch({type: 'JOB_RETURN', jobs: json.jobs})
    })
}