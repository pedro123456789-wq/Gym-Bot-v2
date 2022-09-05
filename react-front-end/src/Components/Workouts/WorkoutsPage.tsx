import SideBar from "../SideBar/SideBar";
import React, { useState } from 'react';
import WorkoutMenu from "./WorkoutMenu";
import AddRunPage from "./AddRunPage";
import AddWorkoutPage from "./AddWorkoutPage";
import LiveWorkoutPage from "./LiveWorkoutPage";



function WorkoutsPage() {
    const [pageMode, toggleMode] = useState('menu');


    return (
        <div>
            <SideBar />

            {pageMode === 'menu' ?
                <WorkoutMenu toggleMode={toggleMode} />
                : pageMode === 'run' ?
                    <AddRunPage toggleMode={toggleMode} />
                    : pageMode === 'addWorkout' ?
                        <AddWorkoutPage toggleMode={toggleMode} />
                        : pageMode === 'liveWorkout' &&
                            <LiveWorkoutPage toggleMode={toggleMode} />
            }
        </div>
    );
}

export default WorkoutsPage;