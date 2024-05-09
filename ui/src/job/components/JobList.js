import {useEffect, useState} from "react";
import {useDispatch, useSelector} from "react-redux";
import {getJobsForUser} from "../actions";
import {Container, List} from "@mui/material";
import JobListItem from "./JobListItem";

const JobList = () => {
  const jobs = useSelector(({job}) => job?.jobs)
  const [selectedJobs, setSelectedJobs] = useState([])

  const dispatch = useDispatch()

  useEffect(() => {
    dispatch(getJobsForUser('907b4a5d-f767-4333-9846-42db46250a3a'))
  }, [dispatch])

  const selectJob = (job_uuid) => {
    let idx = selectedJobs.indexOf(job_uuid)
    if (idx === -1) {
      setSelectedJobs([...selectedJobs, job_uuid])
    }
  }

  const deselectJob = (job_uuid) => {
    let idx = selectedJobs.indexOf(job_uuid)
    if (idx !== -1) {
      setSelectedJobs(selectedJobs.filter((uuid) => uuid !== job_uuid))
    }
  }

  return (
    <Container>
      <List dense>
        {
          jobs.map((job, i) => {
            return (
              <JobListItem
                key={i}
                job={job}
                selected={selectedJobs.indexOf(job.uuid) !== -1}
                selectJob={selectJob}
                deselectJob={deselectJob}
              />
            )
          })
        }

      </List>
    </Container>
  )

}

export default JobList