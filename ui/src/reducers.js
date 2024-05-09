import {combineReducers} from "@reduxjs/toolkit";

import {default as jobReducer} from './job/reducer';

const rootReducer = combineReducers({
  job: jobReducer
})

export default rootReducer;