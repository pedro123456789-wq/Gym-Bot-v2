import SideBar from "../SideBar/SideBar";
import { useState } from 'react';
import NutritionMenu from "./NutritionMenu";
import ManualAddPage from "./ManualAddPage";
import AddByName from "./AddByName";


function NutritionPage() {
    const [currentMode, toggleMode] = useState('menu');

    return (
        <div>
            <SideBar />

            <div>
                {
                    currentMode === 'menu' ?
                        <NutritionMenu toggleMode={toggleMode} />
                        : currentMode === 'manualAdd' ?
                            <ManualAddPage toggleMode={toggleMode} />
                            : currentMode === 'nameAdd' ? 
                                <AddByName toggleMode={toggleMode} />
                                : ''
                }
            </div>
        </div>

    );
}

export default NutritionPage;