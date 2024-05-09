import {Box, Checkbox, IconButton, ListItem, ListItemIcon, ListItemText} from "@mui/material";
import ExpandLessIcon from "@mui/icons-material/ExpandLess";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import LinkIcon from "@mui/icons-material/Link";
import AutoFixHighIcon from "@mui/icons-material/AutoFixHigh";
import UploadIcon from "@mui/icons-material/Upload";
import {useState} from "react";

const JobListItem = ({job, selected, selectJob, deselectJob}) => {
  const [expand, setExpand] = useState(false)

  const handleExpand = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setExpand(!expand)
  }

  const handleCheck = (e) => {
    if (e.target.checked)
      selectJob(job.uuid)
    else
      deselectJob(job.uuid)
  }

  return (
    <>
      <ListItem sx={{display: 'flex', justifyContent: 'space-between'}}>
        <Box sx={{display: 'flex', alignItems: 'center'}}>
          <ListItemIcon><IconButton onClick={handleExpand}>{expand ? <ExpandLessIcon /> : <ChevronRightIcon />}</IconButton></ListItemIcon>
          <ListItemIcon><Checkbox onChange={handleCheck} checked={selected} size='small'/></ListItemIcon>
          <ListItemText primary={job.title} secondary={job.company.name} />
        </Box>
        <Box sx={{display: 'flex'}}>
          {expand && <ListItemIcon><IconButton><LinkIcon /></IconButton></ListItemIcon>}
          <ListItemIcon><IconButton><AutoFixHighIcon /></IconButton></ListItemIcon>
          <ListItemIcon><IconButton><UploadIcon /></IconButton></ListItemIcon>
        </Box>
      </ListItem>
    </>
  )
}

export default JobListItem