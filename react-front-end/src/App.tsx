import {
  BrowserRouter,
  Route,
  Routes,
  Outlet
} from "react-router-dom";
import DashBoard from "./Components/DashBoardPage/DashBoard";
import EmailConfirmationPage from "./Components/EmailConfirmationPage/EmailConfirmationPage";
import FeaturesPage from "./Components/FeaturesPage/FeaturesPage";
import LandingPage from './Components/LandingPage/LandingPage';
import LoginPage from "./Components/LoginPage/LoginPage";
import SignUpPage from "./Components/SignUpPage/SignUpPage";
import ProfilePage from "./Components/ProfilePage/ProfilePage";

// install react ui kit: https://www.npmjs.com/package/material-kit-react


function App(): JSX.Element {
  return (
    <BrowserRouter>
      <div className="App">
        <Routes>
          <Route path = '/' element = {<LandingPage />} />
          <Route path = '/log-in' element = {<LoginPage />} />
          <Route path = '/sign-up' element = {<SignUpPage />} />
          <Route path = '/features' element = {<FeaturesPage />} />
          <Route path = '/confirm-email' element = {<EmailConfirmationPage />} />
          <Route path = '/dashboard' element = {<DashBoard />} />
          <Route path = '/profile' element = {<ProfilePage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
