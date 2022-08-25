import useStyles from './styles';
import { menuProps } from './Nutrition';
import BarcodeScannerComponent from 'react-qr-barcode-scanner';


function ScanBarcode({toggleMode}: menuProps) {
    const classes = useStyles();


    return (
        <div className={classes.content}>
            <h3 className = 'text-center'>Scan Barcode</h3>

            <div className = 'text-center'>
                <BarcodeScannerComponent
                    width = {500}
                    height = {500}
                    onUpdate = {(err, result) => {
                        if (result){
                            alert(result.getText());
                        }else{
                            console.log('not found');
                        }
                    }}
                />
            </div>
        </div>
    );
}

export default ScanBarcode;