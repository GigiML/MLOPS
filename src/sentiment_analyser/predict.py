import click
import pandas as pd
from sentiment_analyser.model_manager import ModelManager


@click.command()
@click.option('--input_file', help='csv file with message to classify')
@click.option('--output_file',help='csv output file')
@click.option('--text', help='alternative to input_file, takes a single text directly from the command line, calculates its polarity and displays it on standard output.')
@click.option('--model_name', required=True,  help='Name of the model in MLFlow.')
@click.option('--model_version', required=True, help='Version of the model in MLFlow.')
@click.option('--mlflow_url', default='http://localhost:5000', type=str, help='MLFlow server URL.')

def main(input_file, output_file, text, model_name, model_version, mlflow_url):
    """ Predict from the input file or the text the polarity of the message
    if the output file is specified the prediction will be written in. """
    if not (input_file or text):
        raise click.BadParameter("Exactly one of --input_file or --text must be provided.")
    manager = ModelManager(model_name=model_name, model_version=model_version, mlflow_url=mlflow_url)

    if input_file:
        predictions = manager.predict_from_file(input_file)
        if output_file:
            pd.DataFrame(predictions).to_csv(output_file, index=False)
            click.echo(f'Predictions saved to {output_file}.')
        else:
            click.echo(predictions)
    
    if text:
        df = pd.DataFrame(data={"review": [text]})
        prediction = manager.predict(df)
        click.echo(f'Prediction for provided text: {prediction[0]}')

if __name__ == '__main__':
    main()
    
