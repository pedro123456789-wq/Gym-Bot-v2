import Navbar from "../NavBar/Navbar";

const video = require('../../Assets/landing_page_video.mp4');



function LandingPage() : JSX.Element{
    return (
        <div>
            <video autoPlay muted loop className = 'main-video'>
                <source src = {video} type = 'video/mp4' />
            </video>

            <div>
                <Navbar />
                
                <h1 className = 'main-text display-3'>
                    Gym Bot
                </h1>

                <p className = 'main-text display-5 mt-5 pt-5 ml-3'>
                    Your AI personal trainer
                </p>
            </div>

        </div>
    );
}

export default LandingPage;