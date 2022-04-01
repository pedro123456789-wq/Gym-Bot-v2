type alertProps = {
    message: string, 
    isSuccess: boolean
}


function Alert({message, isSuccess} : alertProps): JSX.Element {
    return (
        <div style = {{background: isSuccess ? 'green' : 'red', 
                       borderRadius: '1rem'}}>
            <p className = 'text-center display-5 pt-3 pb-3 mb-5'
               style = {{color: 'white'}}>
                {message} 
            </p>
        </div>
    );
}

export default Alert;