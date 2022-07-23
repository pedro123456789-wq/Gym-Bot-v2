function LoadingIndicator() {
    return (
        <div style = {{minHeight: '100vh'}}>
            <div className = 'lds-ellipsis'><div></div><div></div><div></div><div></div></div>
        </div>
    );
}

export default LoadingIndicator;