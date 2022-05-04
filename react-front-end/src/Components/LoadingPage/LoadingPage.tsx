import LoadingIndicator from "../LoadingIndicator/LoadingIndicator";

type loadingProps = {
    backgroundColor: string
};


function LoadingPage({backgroundColor} : loadingProps) {
    return (
        <div className = 'text-center mt-5 pt-5' style = {{background: backgroundColor}}>
            <LoadingIndicator />
        </div>
    );
}

export default LoadingPage;