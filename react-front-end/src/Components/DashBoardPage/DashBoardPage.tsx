import {useState} from 'react';
import {BsMoon, BsSun} from 'react-icons/bs';
import {VscAccount} from 'react-icons/vsc';
import {Line} from 'react-chartjs-2';







function DashBoardPage() {
    // keep track of display mode 
    const [isLightMode, toggleMode] = useState<boolean>(false);
    const graphState = {
        labels: ['Line1', 'Line2', 'Line3'],
        
        datasets: [
          {
            label: 'Line1',
            fill: false,
            lineTension: 0.5,
            backgroundColor: 'blue',
            borderColor: 'blue',
            borderWidth: 2,
            data: [0, 10, 2, 4, 5]
          }, 
  
          {
            label: 'Line2',
            fill: false,
            lineTension: 0.4,
            backgroundColor: 'red',
            borderColor: 'red',
            borderWidth: 2,
            data: [10, 2, 3, 6, 5]
          }, 
  
          {
            label: 'Line3',
            fill: false,
            lineTension: 0.5,
            backgroundColor: 'white',
            borderColor: 'white',
            borderWidth: 2,
            data: [50, 2, 3, 2, 1]
          }
        ]
      }

    const graphOptions = {
                            title: {
                                display: true,
                                text: 'Statistics',
                                fontSize: 20
                            },
                            legend: {
                                display:true,
                                position:'right'
                            }, 
                            maintainAspectRatio: false
                        }


    // style variables 
    const textColor: string = isLightMode ? 'black' : 'white';
    const backgroundColor: string = isLightMode ? 'white' : 'black';

    return (
        <div style = {{background : backgroundColor, minHeight: '100vh'}}>
            <div style = {{display: 'flex', justifyContent: 'right'}}>
                <button className = 'small-button' 
                        style = {{color: isLightMode ? 'orange' : 'yellow'}}
                        onClick = {() => toggleMode(!isLightMode)} >
                    {isLightMode ? <BsSun /> : <BsMoon />}
                </button>

                <button className = 'small-button pl-4 pr-4'
                        style = {{color: textColor, fontSize: '2rem'}}>
                    <VscAccount />
                </button>

            </div>

            <div>
                <Line data = {graphState} 
                      options = {graphOptions}
                />
            </div>
        </div>
    );
}

export default DashBoardPage;