import {useState} from 'react';
import Navbar from '../NavBar/Navbar';

function EmailConfirmationPage() {
    const [confirmationCode, setConfirmationCode] = useState<number>(0)
    
    return (
        <div>
            <Navbar />

            <h1 className = 'text-center display-4 mt-5'>
                Confirm Email
            </h1>


            <form>
                <div className = 'form-group text-center mt-5 pt-5'>
                    <label htmlFor = 'email-confirmation' className = 'text-center'>Confirmation Code</label>

                    <div className = 'mt-5 mb-5 pb-5'>
                        <input type = 'number'
                               id = 'email-cofirmation'
                               className = 'form-control text-center'
                               placeholder = 'Enter Confirmation Code'
                               onChange = {event => setConfirmationCode(event.target.value as unknown as number)}
                        />
                    </div>

                    <div>
                        <button className = 'btn btn-primary btn-lg mt-5'>
                            Submit
                        </button>

                    </div>
                </div>
            </form>


        </div>
    );
}

export default EmailConfirmationPage;