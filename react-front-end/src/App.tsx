import {
  BrowserRouter,
  Route,
  Routes,
} from "react-router-dom";
import DashBoard from "./Components/DashBoardPage/DashBoard";
import EmailConfirmationPage from "./Components/EmailConfirmationPage/EmailConfirmationPage";
import FeaturesPage from "./Components/FeaturesPage/FeaturesPage";
import LandingPage from './Components/LandingPage/LandingPage';
import LoginPage from "./Components/LoginPage/LoginPage";
import SignUpPage from "./Components/SignUpPage/SignUpPage";
import ProfileCreation from "./Components/ProfileCreation/ProfileCreation";
import Targets from "./Components/Targets/Targets";
import Workouts from "./Components/Workouts/Workouts";
import Nutrition from "./Components/Nutrition/Nutrition";
import Profile from "./Components/Profile/Profile";


// TODO:
// Add password change functionality to profile page
// Add option to add profile photo to profile page
// Add different inputs for email confirmation input

// Make login and sign in page use material ui instead of bootstrap 
// Work on dashboard page:
  // Fetch data from database to fetch real daily data and display it on dashboard

//Work on workout page:
  // Add workout functionality similar to strength training in garmin watch


//Implement add by name functionality in add food page
//Implement scan barcode functionality
//Implement start workout functionality
//Implement calorie prediction functionality


  

function App(): JSX.Element {
  return (
    <BrowserRouter>
      <div className="App">
        <Routes>
          <Route path='/' element={<LandingPage />} />
          <Route path='/log-in' element={<LoginPage />} />
          <Route path='/sign-up' element={<SignUpPage />} />
          <Route path='/features' element={<FeaturesPage />} />
          <Route path='/confirm-email' element={<EmailConfirmationPage />} />
          <Route path='/dashboard' element={<DashBoard />} />
          <Route path='/profile' element={<ProfileCreation />} />
          <Route path='/targets' element={<Targets />} />
          <Route path='/workouts' element={<Workouts />} />
          <Route path='/nutrition' element={<Nutrition />} />
          <Route path='/user-profile' element = {<Profile />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
