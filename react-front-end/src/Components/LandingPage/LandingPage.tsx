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
                
                <div style = {{display: 'flex'}}>
                    <h1 className = 'main-text display-3' style = {{marginTop: '10rem'}}>
                        Gym Bot
                    </h1>

                    <p className = 'main-text display-5 ml-3' style = {{marginTop: '16rem'}}>
                        Your AI personal trainer
                    </p>
                </div>
            </div>

        </div>
    );
}

export default LandingPage;