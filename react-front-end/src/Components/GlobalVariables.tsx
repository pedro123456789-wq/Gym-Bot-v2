export const apiUrl = 'http://localhost:8080/api/'


export function cammelCaseToText(input: string): string{
    // converts cammelCase variable name to text where all words start with upper case
    let outputString = input.charAt(0).toUpperCase();

    for (let i = 1; i < input.length; i ++){
        const currentChar = input.charAt(i);
        // check if character is an upper case letter 
        if (currentChar.toUpperCase() === currentChar && !Number.isInteger(Number(currentChar))){
            outputString += ' ';
        }

        outputString += currentChar;
    }

    return outputString;
}